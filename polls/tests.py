import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def  testing_was_published_recently_with_fufture_posts(self):
        ''' testing whether the was_published_recently() returns false
            for future dates '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def testing_was_published_recently_with_recent_question(self):
        ''' testing whether the was_published_recently() returns true
            for recently published questions '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(pub_date=time)
        self.assertIs(question.was_published_recently(), True)

    def testing_was_published_recently_with_old_question(self):
        ''' testing whether the was_published_recently() returns false
            for old questions '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=time)
        self.assertIs(question.was_published_recently(), False)


def create_question_and_choice(question_text, days,choice_text=None):
    '''
    for creating questons in db testing purposes
    question_text is the body of the question to be inserted to DB
    days is off set of how many days older or from furture the pub_date needs to be
    +ve value for futre posts and  -ve value for older ones 
    '''

    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    if choice_text:
        question.choices.create(choice_text=choice_text, votes = 0)
    return question


class IndexViewTests(TestCase):

    def testing_no_question(self):
        '''
        If no questions exist, message is diplayed
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are avilable")
        self.assertQuerysetEqual(response.context['question_list'],[])


    
    def testing_future_question(self):
        ''' 
        testing whether the indexview ommits the future pub_date questions 
        '''
        create_question_and_choice(question_text="Future question.", days=30,choice_text="Future choice")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No Polls are avilable")
        self.assertQuerysetEqual(response.context['question_list'],[])

    def testing_past_question(self):
        ''' 
        testing whether the indexview shows the older pub_date questions 
        '''
        create_question_and_choice("past question", -30,"past answer")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],['<Question: past question>'])

    def testing_past_and_future_question(self):
        ''' 
        testing whether the indexview ommits the future pub_date questions 
        and only shwos the older posts
        '''
        create_question_and_choice("past question", -30,"past answer")
        create_question_and_choice(question_text="Future question.", days=30, choice_text="future answer")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],['<Question: past question>'])

    def testing_two_past_questions(self):
        '''
        testing whether the Invedview shows 2 or more old polls
        '''
        create_question_and_choice("past question 1", -30,"past answer1")
        create_question_and_choice("past question 2", -5,"past answer2")
        create_question_and_choice("past question 3", -5,"past answer3")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: past question 3>', '<Question: past question 2>', '<Question: past question 1>'])

    def testing_past_question_choices(self):
        '''
        testing whether the INdexView ommits questions that has zero choices 
        also whether it shows questions that has at least 1 choice
        '''
        create_question_and_choice("past question 1", -30) # has no choice
        create_question_and_choice("past question 2", -5,"past answer2")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: past question 2>'])


class DetailViewTests(TestCase):
    def testing_future_question(self):
        '''
        Testing whether future questons gets ommited in DetailView.Also 404 status code comes or not
        ''' 
        future_question = create_question_and_choice('Future question.', 5,"future answer")
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        The detail view of a question with a pub_date in the past displays the question's text.
        '''
        past_question = create_question_and_choice('past Question.', -5, "past answer")
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def testing_past_question_with_no_choices(self):
        '''
        testing whether the DetailView ommits questions that has zero choices
        '''
        question = create_question_and_choice("past question 1", -30) # has no choice
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class Results4ViewTests(TestCase):
    def testing_future_question(self):
        '''
        Testing whether future questons gets ommited in DetailView.Also 404 status code comes or not
        '''
        future_question = create_question_and_choice('Future question.', 5, "Future answer")
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        The detail view of a question with a pub_date in the past displays the question's text.
        '''
        past_question = create_question_and_choice('past Question.', -5, "past answer")
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def testing_past_question_with_no_choices(self):
        '''
        testing whether the ResultslView ommits questions that has zero choices
        '''
        question = create_question_and_choice("past question 1", -30) # has no choice
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
