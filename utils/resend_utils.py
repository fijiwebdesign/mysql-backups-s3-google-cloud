import os
import resend

def resend_send_email(
  from_email, 
  to_email, 
  subject, 
  body
  ):

  resend.api_key = os.environ('RESEND_API_KEY')

  params = {
      "from": from_email,
      "to": [to_email],
      "subject": subject,
      "html": body,
  }

  email = resend.Emails.send(params)
  print(email)  