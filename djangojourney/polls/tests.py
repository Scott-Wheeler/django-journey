from django.test import TestCase

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
    """
    Create a Question with the given question_text and published the given number of days offset to timezone.now()
    Negative days publishes in the past and positive days in the future
    """
    pub_date = timezone.now() + timedelta(days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no Questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        create_question("Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Past question.>"]
        )
        

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page
        """
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_and_past_question(self):
        """
        If both past and future questions exist, only past questions are displayed
        """
        create_question("Past question.", days=-30)
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Past question.>"]
        )


    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        create_question("Past question.", days=-30)
        create_question("Another past question.", days=-6)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Another past question.>", "<Question: Past question.>"]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404
        """
        future_question = create_question("Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past returns the question
        """
        past_question = create_question("Past question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
        
        
        
        
        