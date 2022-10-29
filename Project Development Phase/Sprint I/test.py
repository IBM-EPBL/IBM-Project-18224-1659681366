from flask import Flask, request, render_template, url_for

import sendgrid
import os
from sendgrid.helpers.mail import *

from_email = Email("2k19cse038@kiot.ac.in", "CUSTOMER CARE")
to_email = To("2k19cse041@kiot.ac.in")
subject = "Verify Your Email!"
content = Content("text/plain", "otp:54156")
mail = Mail(from_email, to_email, subject, content)
# mail.template_id = 'd-8f5d09ba69c2492bbdfde27274bf2160'
sg = sendgrid.SendGridAPIClient(
    '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')
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
