from django.db import transaction
from django.db.models import Count, Q
from rest_framework import serializers

from .models import Choice, Exam, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]


class ExamSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "title", "created_at", "question_count"]
        read_only_fields = ["created_at"]


class QuestionSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "exam", "text", "choices", "created_at"]
        read_only_fields = ["created_at"]

    def validate_choices(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Una pregunta necesita al menos dos opciones.")
        if sum(1 for choice in value if choice.get("is_correct")) != 1:
            raise serializers.ValidationError("Debe haber exactamente una opción correcta.")
        return value

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            Choice.objects.bulk_create(Choice(question=question, **choice) for choice in choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices", None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if choices is not None:
                instance.choices.all().delete()
                Choice.objects.bulk_create(Choice(question=instance, **choice) for choice in choices)
        return instance


def validate_choice_set(choices, replacement_correct=None):
    totals = choices.aggregate(
        total=Count("id"),
        correct=Count("id", filter=Q(is_correct=True)),
    )
    if replacement_correct is not None:
        totals["total"] += 1
        totals["correct"] += int(replacement_correct)
    if totals["total"] < 2:
        raise serializers.ValidationError(
            {"choices": "Una pregunta necesita al menos dos opciones."}
        )
    if totals["correct"] != 1:
        raise serializers.ValidationError(
            {"choices": "Debe haber exactamente una opción correcta."}
        )


class ChoiceResourceSerializer(ChoiceSerializer):
    class Meta(ChoiceSerializer.Meta):
        fields = ["id", "question", "text", "is_correct"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if self.instance is not None:
            question = attrs.get("question", self.instance.question)
            if question.pk != self.instance.question_id:
                raise serializers.ValidationError(
                    {"question": "No se puede cambiar la pregunta de una opción."}
                )
            choices = question.choices.exclude(pk=self.instance.pk)
            is_correct = attrs.get("is_correct", self.instance.is_correct)
        else:
            question = attrs["question"]
            choices = question.choices.all()
            is_correct = attrs.get("is_correct", False)
        validate_choice_set(choices, is_correct)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        Question.objects.select_for_update().get(pk=validated_data["question"].pk)
        return super().create(self.validate(validated_data))

    @transaction.atomic
    def update(self, instance, validated_data):
        Question.objects.select_for_update().get(pk=instance.question_id)
        return super().update(instance, self.validate(validated_data))
