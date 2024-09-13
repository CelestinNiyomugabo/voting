import requests
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import os
from dotenv import load_dotenv
load_dotenv() 

def send_whatsapp_message(phone, code):
    token = 'EAAHZCRUM20G4BAPQjY7YLExIAo6Nb6bTg4ZC3GDw6PbuShWBrkdHSLd7VW3pvg4xfbWN94AopGwBOVOvVqmELfRZAfZBsmvyuJtYBHrR3BdXXvLI2orVqKbZAMaFnN4ZCA1S994y3b3pV9D6eyAsebH3BRMhjolI91p7p81fbvI5AMZARe83SNocwghimu5eOJs45UXu1ZCaawZDZD'

    url = 'https://graph.facebook.com/v14.0/106537865538970/messages'

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone,
        "type": "template",
        "template": {
            "name": "vpay_login_otp",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": code
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": code
                        }
                    ]
                }
            ]
        }
    }

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    # Send the POST request
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Check for response status
        if response.status_code == 200:
            return JsonResponse({"status": "success", "response": response.json()})
        else:
            return JsonResponse({"status": "error", "message": response.text})
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"status": "error", "message": str(e)})
