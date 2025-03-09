from rest_framework import serializers
from todo.models import TodoStatus, Label, Todo
from django.contrib.auth.models import User
from django.utils import timezone


class TodoLabelSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['label']


class Base(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    heading = serializers.CharField()
    description = serializers.CharField(required=False)
    priority = serializers.IntegerField(required=False)
    due_on = serializers.DateTimeField(required=False)
    is_recurring = serializers.BooleanField(required=False)
    labels = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all(), required=False, write_only=True, many=True)
    labels_info = TodoLabelSerailizer(
        source='labels', required=False, read_only=True, many=True)
    status = serializers.ChoiceField(
        choices=[label.lower() for label in TodoStatus.labels], required=False)
    created_on = serializers.DateTimeField(read_only=True)
    started_on = serializers.DateTimeField(read_only=True)
    completed_on = serializers.DateTimeField(read_only=True)


class TodoSerializer(Base):
    def validate_due_on(self, due_on):
        if due_on < timezone.now():
            raise serializers.ValidationError(
                'Please select a future due_on time')
        return due_on

    def create(self, validated_data):
        user = self.context.get('user')
        labels = validated_data.pop('labels', [])
        validated_data.pop('status', None)
        todo = Todo.objects.create(**validated_data, user=user)
        if labels:
            todo.labels.set(labels)
        return todo

    def update(self, instance, validated_data):
        labels = validated_data.pop('labels', [])
        if labels:
            instance.labels.set(labels)
        status = validated_data.pop('status', None)
        if status:
            if instance.status == 1 and status == 'working':
                instance.status = 2
                instance.started_on = timezone.now()
            elif instance.status == 2 and status == 'completed':
                instance.status = 3
                instance.completed_on = timezone.now()
            else:
                raise serializers.ValidationError(
                    'You can only change status from created to working and from working to completed')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = TodoStatus(instance.status).label.lower()
        return data
