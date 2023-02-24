from django.test import TestCase


# Here we have one dedicated file for all of the test scrpits written to test our functions
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.backend.settings'

from django.contrib.sessions.backends.base import SessionBase
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.test import RequestFactory, TestCase
from unittest.mock import patch, MagicMock ##mock library for testing functions without sending data to database

from ..backend.views import postsign
from ..backend.views import save_choices
from ..backend.views import postcreateleague
from ..backend.views import postjoinleague
from ..backend.views import leaguetable


class PostSignTestCase(TestCase):

    @patch('backend.views.authe.sign_in_with_email_and_password') # to replace the Firebase Authentication API call
    def test_valid_credentials(self, mock_sign_in): # Set the return value of the mock Firebase Authentication API call
        mock_sign_in.return_value = {'idToken': '12345'} # Create a mock POST request to the postsign function with valid credentials
        request = RequestFactory().post('/', {'email': 'test@example.com', 'pass': 'password'}) # Call the postsign function with the mock request
        response = postsign(request) # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200) # Assert that the response contains the email address in the mock request
        self.assertContains(response, 'test@example.com')

    # Decorate the test_invalid_credentials method with the patch decorator
    @patch('backend.views.authe.sign_in_with_email_and_password')
    def test_invalid_credentials(self, mock_sign_in): # Set the side effect of the mock Firebase Authentication API call to raise an Exception with the message "Invalid credentials"
        mock_sign_in.side_effect = Exception('Invalid credentials') # Create a mock POST request to the postsign function with invalid credentials
        request = RequestFactory().post('/', {'email': 'test@example.com', 'pass': 'password'}) # Call the postsign function with the mock request
        response = postsign(request) # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200) # Assert that the response contains the message "Invalid Credentials"
        self.assertContains(response, 'Invalid Credentials')


class SaveChoicesViewTest(TestCase):

    @patch('backend.views.database.child')
    def test_save_choices_view(self, mock_child):
        # Mock session data to simulate a user session
        session_data = {
            'uid': 123,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
        }
        # update and save session
        self.client.session.update(session_data)
        self.client.session.save()

        # Make a POST request to the view to save fighter choices
        url = reverse('save_choices')
        data = {
            'andradre-blanchfield': 'fighter1',
            'wright-pauga': 'fighter2',
            'parisian-pogues': 'fighter3',
            'knight-prachnio': 'fighter4',
            'miller-hernandez': 'fighter5',
            'sadykhov-elder': 'fighter6',
            'lansberg-silva': 'fighter7',
            'emmers-askhabov': 'fighter8',
            'preux-lins': 'fighter9',
            'fletcher-gorimbo': 'fighter10',
            'carpenter-ronderos': 'fighter11',
        }
        response = self.client.post(url, data)

        # Check if fighters are saved to the database and data is the same
        encoded_email = session_data['email'].replace('.', ',')
        mock_child.return_value.set.assert_called_once_with({
            'andradre-blanchfield': 'fighter1',
            'wright-pauga': 'fighter2',
            'parisian-pogues': 'fighter3',
            'knight-prachnio': 'fighter4',
            'miller-hernandez': 'fighter5',
            'sadykhov-elder': 'fighter6',
            'lansberg-silva': 'fighter7',
            'emmers-askabov': 'fighter8',
            'preux-lins': 'fighter9',
            'fletcher-gorimbo': 'fighter10',
            'carpenter-ronderos': 'fighter11',
        })



class PostCreateLeagueViewTest(TestCase):

    # Test the success case for creating a league
    @patch('myapp.views.database.child')
    def test_post_create_league_success(self, mock_child): # create a POST request with the necessary data
        request = RequestFactory().post('/createleague', {'leaguename': 'My League', 'uniquecode': 'ABC123'}) # add session data to simulate a logged-in user
        request.session = {'uid': 'user_id', 'email': 'user@example.com'}
        request.session.save() # call the view function being tested and get the response
        response = postcreateleague(request) # assert that the response is a redirect and goes to the correct URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/choosefighters') # assert that the database child function was called correctly
        mock_child.assert_called_once_with('leagues/My League')
        mock_child.return_value.set.assert_called_once_with({
            'leaguename': 'My League',
            'owner': 'user@example.com',
            'members': ['user@example.com'],
            'uniquecode': 'ABC123'
        })

    # Test the case where the user is not logged in
    def test_post_create_league_not_logged_in(self): # create a POST request with the necessary data
        request = RequestFactory().post('/createleague', {'leaguename': 'My League', 'uniquecode': 'ABC123'}) # set an empty session to simulate a logged-out user
        request.session = {} # call the view function being tested and get the response
        response = postcreateleague(request) # assert that the response is a success and contains the correct error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are logged out, to continue log back in!')
        self.assertTemplateUsed(response, 'signIn.html')

    # Test the case where there is an error in the database call
    def test_post_create_league_error(self): # create a POST request with no data
        request = RequestFactory().post('/createleague') # add session data to simulate a logged-in user
        request.session = {'uid': 'user_id', 'email': 'user@example.com'}
        request.session.save() # patch the database child function to raise an exception
        with patch('myapp.views.database.child') as mock_child:
            mock_child.return_value.set.side_effect = Exception('Database error') # call the view function being tested and get the response
            response = postcreateleague(request) # assert that the response is a success and contains the correct error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unable to create account try again')
        self.assertTemplateUsed(response, 'signup.html')


class JoinLeagueTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('yourapp.views.database')
    def test_postjoinleague(self, mock_db):
        # Set up mock database response
        mock_leagues = {
            'league1': {'uniquecode': '123', 'members': ['user1@example.com']},
            'league2': {'uniquecode': '456', 'members': ['user2@example.com']},
        }
        mock_db.child.return_value.get.return_value.val.return_value = mock_leagues

        # Set up mock session and POST data
        session = {'uid': 'someuid', 'email': 'user1@example.com'}
        post_data = {'uniquecode': '123'}

        # Set up mock request object
        url = reverse('postjoinleague')
        request = self.factory.post(url, post_data)
        request.session = session

        # Call the view function
        response = postjoinleague(request)

        # Check the response
        self.assertRedirects(response, reverse('leaguetable'))
        mock_db.child.return_value.child.assert_called_with('league1')
        mock_db.child.return_value.child.return_value.update.assert_called_once_with({'members': ['user1@example.com',]})



class LeagueTableTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    @patch('yourapp.views.database')
    def test_league_table_authenticated_user(self, mock_db):
        # Set up mock session data
        session = {'uid': 'someuid', 'email': 'test@example.com'}

        # Set up mock database response
        mock_leagues = {
            'league1': {'leaguename': 'League 1', 'members': ['test@example.com', 'other@example.com']},
            'league2': {'leaguename': 'League 2', 'members': ['another@example.com']},
        }
        mock_db.child.return_value.get.return_value.val.return_value = mock_leagues
        
        # Set up mock request object
        url = reverse('leaguetable')
        request = self.factory.get(url)
        request.session = session
        
        # Call the view function
        response = leaguetable(request)
        
        # Check that the response contains the expected data
        self.assertContains(response, 'League 1')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'other@example.com')
        self.assertNotContains(response, 'another@example.com')
        
    def test_league_table_unauthenticated_user(self):
        # Set up mock request object
        url = reverse('leaguetable')
        request = self.factory.get(url)
        
        # Call the view function
        response = leaguetable(request)
        
        # Check that the response contains the expected message
        self.assertContains(response, 'You are logged out, to continue log back in!')



