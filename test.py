from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="timer">Seconds left:</p>', html)
            self.assertIn("<p>High Score:" , html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_vaild_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], ["C", "A", "T", "T", "T"], ["C", "A", "T", "T", "T"], ["C", "A", "T", "T", "T"], ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text= True)

            response = self.client.get('/check-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)

            response = self.client.get('/check-word?word=adjfkjdjfd')
            self.assertEqual(response.json['result'], 'not-word')
            


    

    # TODO -- write tests for every view function / feature!

 