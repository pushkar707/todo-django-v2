from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from todo.models import Todo, BanWords
from django.db.models import Count
from todo.stores import TodoStore
import difflib


@receiver(pre_save, sender=BanWords)
def lowercase_word(sender, instance, **kwargs):
    '''
    Normalize banned word by converting them to lowercase
    '''
    if instance.word:
        instance.word = instance.word.lower()

@receiver(pre_delete, sender=Todo)
def delete_logs(sender, instance, **kwargs):
    '''
    Delete logs of a todo when todo deleted
    '''
    instance.logs.clear()


def match_string(prev: str, new: str):
    diff = list(difflib.ndiff(prev.split(), new.split()))
    print(diff)
    changes = {
        "added": '',
        "removed": ''
    }

    for item in diff:
        code = item[:2]
        word = item[2:]

        if code == "- ":  # Removed word
            changes['removed'] += f' {word}'
        elif code == "+ ":  # Added word
            changes["added"] += f' {word}'
    return changes


@receiver(post_save, sender=Todo)
def check_todo(sender, instance, created, **kwargs):
    '''
    Check if todo description or heading contains any banned words
    Ban the user if user has used banned words more than 15 times
    '''

    if not instance.auto_created:
        heading = instance.heading.lower()
        description = instance.description.lower()
        if not created:
            prev_todo = TodoStore.getTodoById(instance.id)
            prev_heading = prev_todo.get('heading')
            prev_description = prev_todo.get('description')
            heading_changes = match_string(prev_heading, heading)
            description_changes = match_string(prev_description, description)

            banned_words_added = BanWords.objects.extra(
                where=["%s LIKE '%%' || word || '%%' OR %s LIKE '%%' || word || '%%'"], params=[heading_changes['added'], description_changes['added']])
            banned_words_removed = BanWords.objects.extra(
                where=["%s LIKE '%%' || word || '%%' OR %s LIKE '%%' || word || '%%'"], params=[heading_changes['removed'], description_changes['removed']])
            if banned_words_removed.exists():
                instance.logs.remove(*banned_words_removed)
            if banned_words_added.exists():
                instance.logs.add(*banned_words_added)
        else:
            banned_words = BanWords.objects.extra(
                where=["%s LIKE '%%' || word || '%%' OR %s LIKE '%%' || word || '%%'"], params=[heading, description])
            if banned_words.exists():
                instance.logs.add(*banned_words)

        user = instance.user
        logs = Todo.objects.filter(user=user).aggregate(
            total_logs=Count('logs'))
        print(logs.get('total_logs'))
        if logs.get('total_logs') >= 15:
            user.is_banned = True
            user.save()

    TodoStore.add_todo(instance.id, instance.heading,
                       instance.description, instance.status)
