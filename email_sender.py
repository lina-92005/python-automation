import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import os

def send_email(server, user_email, to_email, subject, body, attachment=None):
    """Send one email"""
    msg = MIMEMultipart()
    msg['From'] = user_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Add attachment if exists
    if attachment and os.path.isfile(attachment):
        with open(attachment, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)

    try:
        server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending to {to_email}: {e}")

def main():
    print("📧 Python Email Sender\n")
    
    print("⚠️ Before continuing, you need a Gmail App Password.")
    print("Steps to get one:")
    print("1. Enable 2-Step Verification in your Google Account.")
    print("2. Go to https://myaccount.google.com/apppasswords")
    print("3. Choose 'Mail' and your device, generate a 16-char password.")
    print("4. Copy it here (instead of your normal Gmail password).\n")
    
    user_email = input("Enter your Gmail address: ").strip()
    user_pass = input("Enter your Gmail App Password: ").strip()

    # ✅ Test login first before asking Excel stuff
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user_email, user_pass)
        print("✅ Logged in successfully!\n")
    except Exception as e:
        print("❌ Login failed. Please check your Gmail and App Password.")
        print("Error:", e)
        return

    print("Choose sending mode:")
    print("1 → Send the SAME message to all emails")
    print("2 → Send DIFFERENT messages for each email")
    choice = input("Option (1 or 2): ").strip()

    if choice == "1":
        print("\n✅ SAME message mode selected")
        print("Excel format required: Column 'email'")
        print("Example:\nemail\nfriend1@gmail.com\nfriend2@gmail.com\n")
    elif choice == "2":
        print("\n✅ DIFFERENT messages mode selected")
        print("Excel format required: Columns 'email' and 'message'")
        print("Example:\nemail              message\nfriend1@gmail.com  Hello friend1!\nfriend2@gmail.com  Hi friend2!\n")
    else:
        print("❌ Invalid choice. Please restart and select 1 or 2.")
        return

    excel_file = input("\nEnter the path to your Excel file (e.g. emails.xlsx): ").strip()
    if not os.path.isfile(excel_file):
        print("❌ File not found. Please check the path.")
        return

    subject = input("Enter the subject of the email: ").strip()
    attachment = input("Enter the path to attachment (or press Enter to skip): ").strip() or None

    try:
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.strip()  # strip spaces
    except Exception as e:
        print("❌ Error reading Excel file:", e)
        return

    if choice == "1":
        body = input("\nEnter the email body (same for all recipients):\n").strip()
        if not body:
            print("❌ Email body cannot be empty.")
            return
        for _, row in df.iterrows():
            to_email = row.get("email")
            if pd.notna(to_email):
                send_email(server, user_email, to_email, subject, body, attachment)

    elif choice == "2":
        for _, row in df.iterrows():
            to_email = row.get("email")
            body = row.get("message")
            if pd.notna(to_email) and pd.notna(body):
                send_email(server, user_email, to_email, subject, body, attachment)

    server.quit()
    print("\n🎉 All emails processed.")

if __name__ == "__main__":
    main()
