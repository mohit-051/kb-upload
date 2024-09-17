import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import re

# Load environment variables from .env file
load_dotenv()

send_email = os.environ["SENDER_EMAIL"]
send_password = os.environ["EMAIL_API_PASSWORD"]


def format_data(generated_data):
    # Use regular expression to insert <br/> tags
    # Use regular expression to insert <br/> tags
    formatted_text = re.sub(r'(\d+\.)', r'<br/><br/>\1', generated_data)
    formatted_text = re.sub(r'(\([a-z]\)\.)', r'<br/>\1', formatted_text)

    return formatted_text


def render_html_template(template_path, context):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    return template.render(context)


def send_email(
    receiver_email, content, sender_email=send_email, sender_password=send_password
):
    # Dynamic content as a dictionary
    dynamic_content = {
        "dynamic_heading": "Welcome to Our Mental Health Counseling Service",
        "dynamic_paragraph": format_data(content),
    }
    # Render the HTML template with dynamic content
    email_content = render_html_template("email/index.html", dynamic_content)

    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    subject = "Mental health report"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = (
        subject
        + " "
        + str(datetime.date.today())
        + " "
        + str(datetime.datetime.now().strftime("%H:%M"))
    )

    # Add body to the email as HTML content
    message.attach(MIMEText(email_content, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, sender_password)

        server.sendmail(sender_email, receiver_email, message.as_string())

        server.quit()

        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))


# # Send the email with dynamic content
# send_email("akibislam793@gmail.com", """1. What is the possible name of the mental discorder I am facing.
# 2. The explanation of the cause and effect of the mental discorder I am facing.
# 3. The possible solutions and therapy. Describe the therapy in pointwise form too. For example like the following:
# (a). therapy a
# (b). therapy b
# (c). dslfjsdfsdf
# 4. The day to day steps I should take to cure it.
# 5. The medicines that would be best for me.""")
