import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os
from dotenv import load_dotenv
load_dotenv()


class MpesaC2bCredential:
    consumer_key = str(os.getenv('CONSUMER_KEY'))
    consumer_secret = str(os.getenv('CONSUMER_SECRET'))
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
     


class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = str(os.getenv('SHORT_CODE'))
    OffSetValue = '0'
    passkey = str(os.getenv('PASSKEY'))
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
    

def get_token():
    consumer_key = str(os.getenv('CONSUMER_KEY'))
    consumer_secret = str(os.getenv('CONSUMER_SECRET'))
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = json.loads(r.text)
    return access_token['access_token']
    

if __name__ == "__main__":
    print(get_token())