from flask import Flask, request, render_template, url_for

import sendgrid
import os
from sendgrid.helpers.mail import *

from_email = Email("2k19cse038@kiot.ac.in", "CUSTOMER CARE")
to_email = To("2k19cse041@kiot.ac.in")
subject = "Verify Your Email!"
content = Content("text/plain", "otp:54156")
mail = Mail(from_email, to_email, subject, content)
sg = sendgrid.SendGridAPIClient('YOUR API KEY')
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
