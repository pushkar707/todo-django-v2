from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from todo.models import Todo, BanWords
from django.db.models import Q, Count, Value


@receiver(pre_save, sender=BanWords)
def lowercase_email(sender, instance, **kwargs):
    if instance.word:
        instance.word = instance.word.lower()


@receiver(post_save, sender=Todo)
def check_todo(sender, instance, created, **kwargs):
    if created:
        # banned_words = BanWords.objects.filter(Q(word__in=heading.split()) | Q(
        #     word__in=description.split()))  # only handles complete word and not substring
        heading = instance.heading.lower()
        description = instance.description.lower()
        banned_words = BanWords.objects.extra(
            where=["%s LIKE '%%' || word || '%%' OR %s LIKE '%%' || word || '%%'"], params=[heading, description])
        if banned_words.exists():
            instance.logs.add(*banned_words)

            user = instance.user
            logs = Todo.objects.filter(user=user).aggregate(
                total_logs=Count('logs'))
            print(logs.get('total_logs'))
            if logs.get('total_logs') >= 15:
                user.is_active = False
                user.save()
