import os
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv

def delete_latest_files():
    for folder, ext in [("recordings", ".wav"), ("transcripts", ".txt"), ("notes", "_notes.txt")]:
        files = glob.glob(os.path.join(folder, f"meeting_audio_*{ext}"))
        if files:
            latest = max(files, key=os.path.getctime)
            try:
                os.remove(latest)
                print(f"Deleted {latest}")
            except Exception as e:
                print(f"Failed to delete {latest}: {e}")

def send_meeting_notes(notes_path=None):
    load_dotenv()
    NOTES_DIR = "notes"

    # Find latest notes file if not provided
    if not notes_path:
        files = glob.glob(os.path.join(NOTES_DIR, "meeting_audio_*_notes.txt"))
        if not files:
            raise FileNotFoundError("No notes files found.")
        notes_path = max(files, key=os.path.getctime)

    with open(notes_path, "r") as f:
        notes_content = f.read()

    # Email config
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
        raise ValueError("Set EMAIL_USER, EMAIL_PASS, and EMAIL_TO in your .env file.")

    msg = MIMEMultipart()
    msg["From"] = formataddr(("Meet Assistant", EMAIL_USER))
    msg["To"] = EMAIL_TO
    msg["Subject"] = "Meeting Notes"
    msg.attach(MIMEText(notes_content, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        print(f"Meeting notes sent to {EMAIL_TO}")
        delete_latest_files()
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_meeting_notes()
