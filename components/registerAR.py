import requests, json
from meya import Component


class register(Component):

    def start(self):
        
        first_name = self.db.flow.get('first_name')
        last_name = self.db.flow.get('last_name')
        phone = self.db.flow.get('phone')
        email = self.db.flow.get('email')
        address = self.db.flow.get('address')
        
        if phone == "إلغاء":
            text = "تم إلغاء التسجيل."
            message = self.create_message(text=text)
            return self.respond(message=message, action="next")
        
        API_ENDPOINT = "http://dev.ionoview.com/api/session?for_register=1"
        
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
            if r.status_code == 409:
                text = "رقم الهاتف هذا مسجل سابقا"
            else:
                text = json.loads(r.text)['message'][0]
            message = self.create_message(text=text)
            return self.respond(message=message, action="retry")
            
        print "successfully sent sms"
        
        API_ENDPOINT = "http://dev.ionoview.com/api/customer"
        
        data = {
            "firstname" : first_name,
            "lastname" : last_name,
            "phone" : phone,
            "device_id" : phone,
            "email" : email,
            "code" : "5555",
            "method" : "sms"
        }
        
        data = json.dumps(data)
        
        headers = {'Content-Type':'application/json',
                'api_version': '1',
                'app_id':'ad16d138-d985-48f3-8bf9-c4b56204fed9',
                'app_secret':'4e03ab88-919a-446b-9944-2cfb2ae18efa'}
        
        r = requests.post(url = API_ENDPOINT, data = data, headers = headers)
        
        if r.status_code != 200:
            text = "عذرًا ، حدث خطأ أثناء تسجيلك. حاول مرة اخرى."
            message = self.create_message(text=text)
            return self.respond(message=message, action="retry")

        API_ENDPOINT = 'http://52.28.245.105/IonoBot/public/api/customers'
        
        data = {
            "first_name" : first_name,
            "last_name" : last_name,
            "phone" : phone,
            "email" : email,
            "address" : address
        }
        
        data = json.dumps(data)
        
        headers = {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC81Mi4yOC4yNDUuMTA1XC9Jb25vQm90XC9wdWJsaWNcL2FwaVwvbG9naW4iLCJpYXQiOjE1MzkyNDcxNDIsImV4cCI6MjEzOTI0NzE0MiwibmJmIjoxNTM5MjQ3MTQyLCJqdGkiOiJOUjBDMGRhek9vZFdERFhkIiwic3ViIjoxLCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.ek-AiOv4Yq4_vW3sD84x954t51tSOfxx6FAZeRc7Ey0'
        }
        
        r = requests.post(url = API_ENDPOINT, data = data, headers = headers)
        print r.status_code
        print "\n"
        print r.text
        text = "" 
        if r.status_code == 201:
            print r.text
            text = "تمت عملية التسجيل بنجاح."
        elif r.status_code == 400:
            if json.loads(r.text)['errors'].has_key('phone'):
                text += "رقم الهاتف هذا مسجل سابقا"
                text += "\n"
            if json.loads(r.text)['errors'].has_key('email'):
                text += "عنوان البريد الإلكتروني موجود بالفعل ، أو غير صالح."
                text += "\n"
            text += "عذرًا ، حدث خطأ أثناء تسجيلك. حاول مرة اخرى."
        message = self.create_message(text=text)
        return self.respond(message=message, action="next")
