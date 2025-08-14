from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question, Option


class Command(BaseCommand):
    help = "Seed the database with an initial quiz and questions if none exist. Safe to run multiple times."

    def handle(self, *args, **options):
        if Quiz.objects.exists():
            self.stdout.write(self.style.WARNING("Quizzes already exist. Skipping seeding."))
            return

        quiz = Quiz.objects.create(
            title="General Knowledge Basics",
            description="A short general knowledge quiz for demonstration.",
            duration=10,
        )

        # Question 1
        q1 = Question.objects.create(
            quiz=quiz,
            question_text="What is the capital of France?",
            question_type="MCQ",
        )
        Option.objects.bulk_create([
            Option(question=q1, text="Paris", is_correct=True),
            Option(question=q1, text="Berlin", is_correct=False),
            Option(question=q1, text="Madrid", is_correct=False),
            Option(question=q1, text="Rome", is_correct=False),
        ])

        # Question 2
        q2 = Question.objects.create(
            quiz=quiz,
            question_text="2 + 2 equals?",
            question_type="MCQ",
        )
        Option.objects.bulk_create([
            Option(question=q2, text="3", is_correct=False),
            Option(question=q2, text="4", is_correct=True),
            Option(question=q2, text="5", is_correct=False),
            Option(question=q2, text="22", is_correct=False),
        ])

        # Question 3
        q3 = Question.objects.create(
            quiz=quiz,
            question_text="Select the primary color.",
            question_type="MCQ",
        )
        Option.objects.bulk_create([
            Option(question=q3, text="Green", is_correct=False),
            Option(question=q3, text="Red", is_correct=True),
            Option(question=q3, text="Purple", is_correct=False),
            Option(question=q3, text="Brown", is_correct=False),
        ])

        self.stdout.write(self.style.SUCCESS("Seeded database with sample quiz and questions."))


