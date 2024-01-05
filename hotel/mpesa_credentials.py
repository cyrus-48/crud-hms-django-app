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
    print(r.text)
    if r.status_code == 200:
        try:
            mpesa_access_token = json.loads(r.text)
            validated_mpesa_access_token = mpesa_access_token["access_token"]
            print(validated_mpesa_access_token)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            validated_mpesa_access_token = None
            print("Failed",validated_mpesa_access_token)
    else:
        print(f"Failed to fetch M-Pesa access token. Status code: {r.status_code}")
        validated_mpesa_access_token = None


class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = str(os.getenv('SHORT_CODE'))
    OffSetValue = '0'
    passkey = str(os.getenv('PASSKEY'))
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')