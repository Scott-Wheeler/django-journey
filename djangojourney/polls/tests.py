from django.test import TestCase

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse

# Create your tests here.

from .models import Question, Choice

## helper functions
def create_question(question_text, days):
    """
    Create a Question with the given question_text and published the given number of days offset to timezone.now()
    Negative days publishes in the past and positive days in the future
    """
    pub_date = timezone.now() + timedelta(days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)

def create_choice(question, choice_text):
    """
    Create a choice attached to a question given the question and the text of the choice
    """
    return Choice.objects.create(question=question, choice_text=choice_text)



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
        past_question = create_question("Past question.", days=-30)
        create_choice(past_question, "This is the choice.")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Past question.>"]
        )
        

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page
        """
        future_question = create_question("Future question.", days=30)
        create_choice(future_question, "This is the choice.")
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_and_past_question(self):
        """
        If both past and future questions exist, only past questions are displayed
        """
        past_question = create_question("Past question.", days=-30)
        create_choice(past_question, "This is the choice.")
        future_question = create_question("Future question.", days=30)
        create_choice(future_question, "This is the choice.")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Past question.>"]
        )


    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        past_question = create_question("Past question.", days=-30)
        create_choice(past_question, "This is the choice.")
        another_past_question = create_question("Another past question.", days=-6)
        create_choice(another_past_question, "This is the choice.")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Another past question.>", "<Question: Past question.>"]
        )

    def test_question_with_no_choices(self):
        """
        Questions that do not have any choices should not be shown in the index view
        """
        past_question = create_question("Past question.", days=-5)
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_question_with_a_choice(self):
        """
        Questions that have choices should be shown in the index view
        """
        past_question = create_question("Past question.", days=-5)
        question_choice = create_choice(past_question, "This is the choice.")
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: Past question.>"]
        )
        
        

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404
        """
        future_question = create_question("Future question.", days=5)
        future_choice = create_choice(future_question, "This is a choice")
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past returns the question
        """
        past_question = create_question("Past question.", days=-5)
        past_choice = create_choice(past_question, "This is a choice")
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    def test_question_with_no_choices(self):
        """
        Questions that do not have any choices should not be shown in the detail view
        """
        past_question = create_question("Past question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_question_with_a_choice(self):
        """
        Questions that have choices should be shown in the detail view
        """
        past_question = create_question("Past question.", days=-5)
        question_choice = create_choice(past_question, "This is the choice.")
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, "This is the choice")
        
        
         

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404
        """
        future_question = create_question("Future question.", days=5)
        question_choice = create_choice(future_question, "This is the choice.")
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past returns the question
        """
        past_question = create_question("Past question.", days=-5)
        question_choice = create_choice(past_question, "This is the choice.")
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
        
    def test_question_with_no_choices(self):
        """
        Questions that do not have any choices should not be shown in the results view
        """
        past_question = create_question("Past question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_question_with_a_choice(self):
        """
        Questions that have choices should be shown in the results view
        """
        past_question = create_question("Past question.", days=-5)
        question_choice = create_choice(past_question, "This is the choice.")
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, "This is the choice")
        
        
        
        