from django.db.models.signals import post_save
from django.dispatch import receiver
from todo.models import Todo, Log, BanWords


@receiver(post_save, sender=Todo)
def check_todo(sender, instance, created, **kwargs):
    if created:
        heading = instance.heading.lower()
        description = instance.description.lower()

        words = [BanWords[item.upper()].value for item in [label for label in BanWords.labels] if item in heading or item in description]
        if len(words):
            Log.objects.create(todo=instance, words=words)

            
