import unittest
import requests

class ChatbotTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000'

    def test_chatbot(self):
        response = requests.post(f'{self.BASE_URL}/chatbot/', json={'question': 'What is the poverty headcount ratio in Brazil?'})
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('answer', json_response)

    def test_health_check(self):
        response = requests.get(f'{self.BASE_URL}/')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['message'], 'Chatbot API is running.')

if __name__ == '__main__':
    unittest.main()
