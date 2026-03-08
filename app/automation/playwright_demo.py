import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pyttsx3
import threading
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from recording.ffmpeg_recorder import FFmpegRecorder

load_dotenv()

# Get credentials from environment variables
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")
MEET_URL = os.getenv("MEET_URL")  # Add your test Meet link to .env

RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

if not GOOGLE_EMAIL or not GOOGLE_PASSWORD:
    raise ValueError("Set GOOGLE_EMAIL and GOOGLE_PASSWORD in your .env file or environment.")
if not MEET_URL:
    raise ValueError("Set MEET_URL in your .env file or environment.")


def google_login(page):
    page.goto("https://accounts.google.com/signin")
    page.fill("input[type='email']", GOOGLE_EMAIL)
    page.click("button:has-text('Next')")
    page.wait_for_timeout(2000)
    page.fill("input[type='password']", GOOGLE_PASSWORD)
    page.click("button:has-text('Next')")
    # Wait for Google account profile icon as login success indicator
    try:
        page.wait_for_selector('img[alt="Google Account profile picture"]', timeout=15000)
        print("Login successful, profile icon found.")
    except Exception:
        print("Login may not be successful, profile icon not found.")
    page.wait_for_timeout(2000)


def disable_camera_and_mic(page):
    # Try to disable camera and mic, but continue if not found
    try:
        page.wait_for_selector('button[aria-label*="camera"]', timeout=5000)
        page.click('button[aria-label*="camera"]')
        print("Camera toggled.")
    except Exception:
        print("Camera toggle not found or already off. Skipping.")
    try:
        page.wait_for_selector('button[aria-label*="microphone"]', timeout=5000)
        page.click('button[aria-label*="microphone"]')
        print("Microphone toggled.")
    except Exception:
        print("Microphone toggle not found or already off. Skipping.")


def join_meeting(page):
    # Wait for either 'Ask to join' or 'Join now' and click whichever is available
    try:
        page.wait_for_selector('button:has-text("Join now")', timeout=5000)
        page.click('button:has-text("Join now")')
        print("Clicked 'Join now' to enter the meeting.")
    except Exception:
        try:
            page.wait_for_selector('button:has-text("Ask to join")', timeout=5000)
            page.click('button:has-text("Ask to join")')
            print("Clicked 'Ask to join' to request entry.")
        except Exception:
            print("Neither 'Join now' nor 'Ask to join' button found. Skipping join.")


def send_chat_message(page, message):
    try:
        # Wait for chat button and click it
        page.wait_for_selector('button[aria-label="Chat with everyone"]', timeout=10000)
        page.click('button[aria-label="Chat with everyone"]')
        print("Chat panel opened.")
        # Wait for chat textarea and send message
        page.wait_for_selector('textarea[aria-label="Send a message"]', timeout=10000)
        page.fill('textarea[aria-label="Send a message"]', message)
        page.press('textarea[aria-label="Send a message"]', 'Enter')
        print("Chat message sent.")
    except Exception as e:
        print(f"Failed to send chat message: {e}")


def handle_permissions_popup(page):
    try:
        # Wait for the popup and click the 'Continue without microphone and camera' button
        page.wait_for_selector('button:has-text("Continue without microphone and camera")', timeout=10000)
        page.click('button:has-text("Continue without microphone and camera")')
        print("Permissions popup handled: continued without mic and camera.")
    except Exception:
        print("Permissions popup not found or already handled.")


def speak_introduction():
    try:
        engine = pyttsx3.init()
        engine.say("Hi everyone I am Ardhendu's personal assistant He is busy so I am here to take notes.")
        engine.runAndWait()
    except Exception as e:
        print(f"TTS error suppressed: {e}")


def monitor_meeting_end(page):
    print("Monitoring meeting state...")
    try:
        # Wait for the 'You left the meeting' message or similar DOM change
        page.wait_for_selector('div:has-text("You left the meeting")', timeout=60*60*1000)  # 1 hour max
        print("Detected meeting end.")
    except Exception:
        print("Meeting end not detected, timeout or manual exit.")


# Simple script to launch browser and open a webpage

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        google_login(page)
        print(f"Navigating to Google Meet: {MEET_URL}")
        page.goto(MEET_URL)
        handle_permissions_popup(page)
        disable_camera_and_mic(page)
        join_meeting(page)
        # Save audio in 'recordings' directory with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = RECORDINGS_DIR / f"meeting_audio_{timestamp}.wav"
        recorder = FFmpegRecorder(output_file=str(audio_path), device="default")
        recorder.start()
        send_chat_message(page, "Hi, I am Ardhendu's personal assistant. He is busy so I will take notes.")
        time.sleep(2)
        speak_introduction()
        time.sleep(2)
        monitor_meeting_end(page)
        recorder.stop()
        browser.close()

if __name__ == "__main__":
    main()
