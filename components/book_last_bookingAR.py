# -*- coding: utf-8 -*-
import requests, json
from meya import Component


class book_last_booking(Component):

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
            
            booking_type = json.loads(text)['data']['type']
            schedule = json.loads(text)['data']['schedule']
            time = json.loads(text)['data']['time']
            nationality = json.loads(text)['data']['nationality']
            
            self.db.flow.set('booking_type', booking_type)
            self.db.flow.set('schedule', schedule)
            self.db.flow.set('time', time)
            self.db.flow.set('nationality', nationality)
            
            text = "هذه معلومات حجزك:"
            text += "\n"
            
            if booking_type == "package":
                booking_type = "باقة"
            if booking_type == "single":
                booking_type == "زيارة واحدة"
            if time == "morning":
                time = "في الصباح"
            if time == "afternoon":
                time = "بعد الظهر"
            
            text = 'نوع الحجز هو' + booking_type + '\n'
            text += 'عدد الزيارات ' + schedule + '\n'
            text += 'الوقت ' + time + '\n'
            
            
            message = self.create_message(text=text)
            return self.respond(message=message, action="transfer")
        else:
            text = "لا حجوزات سابقة"
            message = self.create_message(text=text)
            return self.respond(message=message, action="next")
