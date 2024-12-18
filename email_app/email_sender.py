import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

# Function to send email
def send_email(to, subject, body, cc=None, bcc=None, attachment=None):
    # Load configuration from JSON file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    from_email = config["email"]
    password = config["password"]

    # Create the MIME message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to)  # Join the list of 'To' emails with commas
    msg['Subject'] = subject
    
    if cc:
        msg['Cc'] = ", ".join(cc)  # Join the list of 'CC' emails with commas
    if bcc:
        # BCC is not added to the headers, it's handled when sending
        recipients = to + cc + bcc  # Combine all email lists (To, CC, BCC)
    else:
        recipients = to + cc if cc else to  # Only add CC if it exists

    # Attach the body content
    msg.attach(MIMEText(body, 'plain'))

    # Attach file if provided
    if attachment:
        filename = os.path.basename(attachment)
        attachment_part = MIMEBase('application', 'octet-stream')
        try:
            with open(attachment, 'rb') as attach_file:
                attachment_part.set_payload(attach_file.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(attachment_part)
        except Exception as e:
            print(f"Error attaching file: {e}")

    try:
        # Set up the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, password)
        server.sendmail(from_email, recipients, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Function to split comma-separated email input into a list
def parse_email_input(email_input):
    return [email.strip() for email in email_input.split(",")]

# Main function to take user input
def main():
    print("Enter the details for the email.")
    
    # User inputs
    to_input = input("To (comma-separated): ")
    to = parse_email_input(to_input)
    
    subject = input("Subject: ")
    body = input("Email content: ")
    
    cc_input = input("CC (optional, comma-separated): ") or None
    bcc_input = input("BCC (optional, comma-separated): ") or None
    attachment = input("Attachment file path (optional): ") or None

    # Convert CC and BCC to lists if not None
    cc = parse_email_input(cc_input) if cc_input else []
    bcc = parse_email_input(bcc_input) if bcc_input else []
    
    # Send the email
    send_email(to, subject, body, cc, bcc, attachment)

if __name__ == "__main__":
    main()
