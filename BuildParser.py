import smtplib
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def parse_build_output(build_output):
    # Regular expression pattern for parsing test summary information
    test_summary_pattern = re.compile(r'(?:Test runs?|Tests|Test cases?) run: (\d+),\s*Failures: (\d+),\s*Errors: (\d+),\s*Skipped: (\d+)', re.IGNORECASE)

    # Parsing test summary from the build output using the pattern
    test_summary_match = test_summary_pattern.search(build_output)
    if not test_summary_match:
        raise ValueError("No test summary found in build output.")
    
    total_tests = test_summary_match.group(1)  # Change this line to capture total tests
    total_failures = test_summary_match.group(2)
    total_errors = test_summary_match.group(3)
    total_skipped = test_summary_match.group(4)
    
    # Determine build status based on failures and errors
    build_status = "SUCCESS" if int(total_failures) == 0 and int(total_errors) == 0 else "FAILURE"
    
    return {
        "total_tests": total_tests,
        "total_failures": total_failures,
        "total_errors": total_errors,
        "total_skipped": total_skipped,
        "build_status": build_status
    }

def send_email(summary, developer_emails):
    # Extracting values from the summary dictionary
    total_tests = summary.get('total_tests', 'N/A')
    total_failures = summary.get('total_failures', 'N/A')
    total_errors = summary.get('total_errors', 'N/A')
    total_skipped = summary.get('total_skipped', 'N/A')
    build_status = summary.get('build_status', 'N/A')

    # Email credentials and settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "khusheel26@gmail.com"
    smtp_password = "sgoy anpi zqzo hctc"
    from_email = smtp_username
    to_emails = developer_emails
    subject = f"Jenkins Build Summary: {build_status}"

    # Email body
    body = f"""
    Hello Team,
    Here is the summary of the latest Jenkins build:
    Total Tests: {total_tests}
    Total Failures: {total_failures}
    Total Errors: {total_errors}
    Total Skipped: {total_skipped}
    Build Status: {build_status}
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
    if len(sys.argv) != 2:
        print("Usage: python BuildParser.py <path_to_log_file>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    
    # Read the build output from the file
    with open(log_file_path, 'r') as file:
        build_output = file.read()
    
    # Developer emails
    developer_emails = [
        "khusheel26@gmail.com",
        "khusheel.maskar@octobit8.com"
    ]
    
    # Parse the build output
    try:
        summary = parse_build_output(build_output)
    except ValueError as e:
        print(f"Failed to parse build output: {e}")
        sys.exit(1)
    
    # Send the email summary
    send_email(summary, developer_emails)
