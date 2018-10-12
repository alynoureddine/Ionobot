# -*- coding: utf-8 -*-
import requests, json
from meya import Component


class login(Component):

    def start(self):
        
        customer_id = self.db.user.get('customer_id')
        
        API_ENDPOINT = 'http://52.28.245.105/IonoBot/public/api/customers/' + `customer_id` + '/lastbooking'

        headers = {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC81Mi4yOC4yNDUuMTA1XC9Jb25vQm90XC9wdWJsaWNcL2FwaVwvbG9naW4iLCJpYXQiOjE1MzkyNDcxNDIsImV4cCI6MjEzOTI0NzE0MiwibmJmIjoxNTM5MjQ3MTQyLCJqdGkiOiJOUjBDMGRhek9vZFdERFhkIiwic3ViIjoxLCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.ek-AiOv4Yq4_vW3sD84x954t51tSOfxx6FAZeRc7Ey0'
        }
        
        r = requests.get(url = API_ENDPOINT, headers = headers)
        text = r.text
        #print text
        
        if r.status_code == 200:
            text = "found a previous booking"
            self.db.flow.set('last_booking', 'exist')
            message = self.create_message(text=text)
            return self.respond(message=None, action="next")
        else:
            text = "no previous bookings"
            message = self.create_message(text=text)
            return self.respond(message=None, action="next")
