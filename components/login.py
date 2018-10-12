import requests, json
from meya import Component


class login(Component):

    def start(self):

        phone = self.db.flow.get('phone')

        API_ENDPOINT = "http://dev.ionoview.com/api/session?for_register=0"

        data = {
            'phone' : phone,
            'device_id' : phone,
            'method' : 'sms'
        }
                
        data = json.dumps(data)
        
        headers = {'Content-Type':'application/json',
                'api_version': '1',
                'app_id':'ad16d138-d985-48f3-8bf9-c4b56204fed9',
                'app_secret':'4e03ab88-919a-446b-9944-2cfb2ae18efa'}
        
        r = requests.post(url = API_ENDPOINT, data = data, headers = headers)
        text = r.text
        status = json.loads(text)['status']

        if r.status_code != 200:
            text = json.loads(r.text)['message'][0]
            message = self.create_message(text=text)
            return self.respond(message=message, action="next")
            
        print "successfully sent sms"


        API_ENDPOINT = "http://dev.ionoview.com/api/session/" + phone
        
        data = {'device_id':phone,
                'code':'5555',
                'method':'sms'} 
        
        headers = {'Content-Type':'application/json',
                'api_version': '1',
                'app_id':'ad16d138-d985-48f3-8bf9-c4b56204fed9',
                'app_secret':'4e03ab88-919a-446b-9944-2cfb2ae18efa'}
                
        data = json.dumps(data)

        r = requests.put(url = API_ENDPOINT, data = data, headers = headers)
        
        if r.status_code != 200:
            text = "failed to sign you in, please try again later or contact support" + `r.status_code`
            print r.text
            message = self.create_message(text=text)
            return self.respond(message=message, action="next")
        print "signed in successfully"
        
        API_ENDPOINT = 'http://52.28.245.105/IonoBot/public/api/customers/byphone/' + phone

        headers = {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC81Mi4yOC4yNDUuMTA1XC9Jb25vQm90XC9wdWJsaWNcL2FwaVwvbG9naW4iLCJpYXQiOjE1MzkyNDcxNDIsImV4cCI6MjEzOTI0NzE0MiwibmJmIjoxNTM5MjQ3MTQyLCJqdGkiOiJOUjBDMGRhek9vZFdERFhkIiwic3ViIjoxLCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.ek-AiOv4Yq4_vW3sD84x954t51tSOfxx6FAZeRc7Ey0'
        }
        
        r = requests.get(url = API_ENDPOINT, headers = headers)
        text = r.text
        print text
        
        if r.status_code == 200:
            text = "logged in successfully"
            text = r.text
            self.db.user.set('first_name', json.loads(text)['data']['first_name'])
            self.db.user.set('last_name', json.loads(text)['data']['last_name'])
            self.db.user.set('phone', json.loads(text)['data']['phone'])
            self.db.user.set('email', json.loads(text)['data']['email'])
            self.db.user.set('address', json.loads(text)['data']['address'])
            self.db.user.set('customer_id', json.loads(text)['data']['id'])
            
            text = "logged in successfully"
            
        else:
            text = "Failed to login.\nPlease make sure you entered"
            text += " a valid phone number."
        
        message = self.create_message(text=text)
        return self.respond(message=message, action="next")
