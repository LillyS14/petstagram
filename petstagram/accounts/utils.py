from django.conf import settings
from django.template.loader import render_to_string
from mailjet_rest import Client


def send_welcome_email(email):
    username = email.split("@")[0]
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version="v3.1")
    html_content = render_to_string("accounts/email-greeting.html", {"username": username})

    data = {
        "Messages": [
            {
                "From": {
                    "Email": settings.MAILJET_EMAIL,
                    "Name": "PetstagramTeam"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": username
                    },
                ],
                "Subject": "Welcome to Petstagram!",
                "TextPart": "Greetings from Mailjet!",
                "HTMLPart": html_content
            }
        ]
    }
    result = mailjet.send.create(data=data)

    print(result.status_code, result.json())  # adv. by chat
