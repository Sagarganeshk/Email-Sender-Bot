import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import mimetypes

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

recipients = input(" Enter recipient email(comma-separated): ").split(",")
recipients = [email.strip() for email in recipients]

subject = input(" Enter subject: ")
plain_body = input("Enter your message(plain text): ")

html_body = f"""
<html>
  <body>
    <h2 style="color: #007BF28a745;">HELLO from Python Email Bot, Here you can add the Attachments</h2>
    <p>{plain_body}</p>
    <p><b>Sent by:</b> {EMAIL_ADDRESS}</p>
    <p><a herf="https://openai.com" target="_blank">Click here</a> to visit
    OpenAi</p>
    <p><i>Attachments included below.<i/></p>
  <body>
</html>    
"""

msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = ", ".join(recipients)
msg.set_content(plain_body)
msg.add_alternative(html_body, subtype='html')

file_input = input("Enter file paths to attach(comma-separated): ").split(",")

for file_path in file_input:
  file_path = file_path.strip()
  if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
      file_data = f.read()
      mime_type, _= mimetypes.guess_type(file_path)
      maintype, subtype = mime_type.split('/') if mime_type else ('application','octet-stream')
      filename = os.path.basename(file_path)
      msg.add_attachment(file_data, maintype=mime_type, subtype=subtype, filename=filename)
  else:
    print(f" File not found: {file_path}")    

context = ssl.create_default_context()

try: 
   with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
    print("✅ Email sent to multiple recipients successfully!")
except Exception as e:
  print("❌ Failed to send email:",e)