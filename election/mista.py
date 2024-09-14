import requests
import json
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

def send_sms(phone, code):
    token = 'EAAHZCRUM20G4BAPQjY7YLExIAo6Nb6bTg4ZC3GDw6PbuShWBrkdHSLd7VW3pvg4xfbWN94AopGwBOVOvVqmELfRZAfZBsmvyuJtYBHrR3BdXXvLI2orVqKbZAMaFnN4ZCA1S994y3b3pV9D6eyAsebH3BRMhjolI91p7p81fbvI5AMZARe83SNocwghimu5eOJs45UXu1ZCaawZDZD'
    message = 'Use ' + code + ' as your AUCA voting OTP'
    url = "https://pay.vonsung.rw/api/send_sms"

    payload = json.dumps({
        "phone": phone,
        "message": message,
        "sender_id": "VONSUNG"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, data=payload, headers=headers)

        # First, attempt to parse the response as JSON
        try:
            response_data = response.json()
            # Return JSON response, so safe=True is fine (which is default behavior)
            return JsonResponse({"status": "success", "response": response_data})

        # If response isn't JSON, handle as plain text or other formats
        except ValueError:
            response_data = response.text
            # When returning non-dict objects, use safe=False
            return JsonResponse({"status": "success", "response": response_data}, safe=False)

    # Handle any exceptions during the request
    except requests.exceptions.RequestException as e:
        return JsonResponse({"status": "error", "message": str(e)}, safe=False)
