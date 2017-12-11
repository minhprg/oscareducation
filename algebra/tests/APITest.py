import os
from random import choice
import json

from django.test import Client
from django.core.urlresolvers import reverse

import unittest2 as unittest

import django
django.setup()

class APITest(unittest.TestCase):

    client = Client()
    expression_ids = []

    def __init__(self, test_names):
        pwd = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(pwd, "expressions.json"), "r") as equation_file:
            self.pool = json.loads(equation_file.read())["expressions"]
        unittest.TestCase.__init__(self, test_names)

    def test_post_equation(self):
        expression = choice(self.pool)
        expression["expression"] = expression["string"]
        expression["level"] = 1

        response = self.client.post(
            '/algebra/api/expression',
            json.dumps(expression),
            content_type='application/json'
        )

        print(response)
        self.assertEqual(201, response.status_code)
        expression_ids.append(json.loads(response.body).id)

    def test_get_expression(self):
        for id in self.expression_ids:
            response = self.client.get('/algebra/api/expression/' + id,
                content_type='application/json')
            self.assertEqual(200, response.status_code)

    def test_get_expressions(self):
        response = self.client.get('/algebra/api/expressions',
            content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_get_random_expression(self):
        pass

    def test_update_expression(self):
        pass

    def delete_expression(self):
        pass

if __name__ == "__main__":

    unittest.main()
