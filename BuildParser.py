import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def parse_build_output(build_output):
    # Parsing success and failure counts from the build output
    test_summary = re.findall(r'(\d+) tests, (\d+) failures', build_output)
    if not test_summary:
        raise ValueError("No test summary found in build output.")
    total_tests, total_failures = test_summary[0]
    # Extract additional info if needed
    build_status = "SUCCESS" if int(total_failures) == 0 else "FAILURE"
    return {
        "total_tests": total_tests,
        "total_failures": total_failures,
        "build_status": build_status
    }
def send_email(summary, developer_emails):
    # Email credentials and settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "khusheel26@gmail.com"
    smtp_password = "sgoy anpi zqzo hctc"
    from_email = smtp_username
    to_emails = developer_emails
    subject = f"Jenkins Build Summary: {summary['build_status']}"
    # Email body
    body = f"""
    Hello Team,
    Here is the summary of the latest Jenkins build:
    Total Tests: {summary['total_tests']}
    Total Failures: {summary['total_failures']}
    Build Status: {summary['build_status']}
    Best Regards,
    Jenkins Automation
    """
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
if __name__ == "__main__":
    # Example build output
    build_output = """
    Running tests...
    100 tests, 5 failures
    ... other build output ...
    """
    # Developer emails
    developer_emails = [
        "khusheel26@gmail.com",
        "khusheel.maskar@octobit8.com"
    ]
    # Parse the build output
    summary = parse_build_output(build_output)
    # Send the email summary
    send_email(summary, developer_emails)
