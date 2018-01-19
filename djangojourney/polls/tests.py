from django.test import TestCase

from datetime import timedelta
from django.utils import timezone

# Create your tests here.

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        .was_published_recently() returns False
        for a question whose pub_date is in the future
        """
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recenty_with_old_question(self):
        """
        .was_published_recently() returns False
        for a question whose pub_date is older than 1 day
        """
        time = timezone.now() - timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
        
    def test_was_published_recently_with_recent_question(self):
        """
        .was_published_recently() returns True
        for a question whose pub_date is within the past day
        """
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

