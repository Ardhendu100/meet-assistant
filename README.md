# Meet Assistant 🤖

An intelligent automation system that joins Google Meet calls, records audio, transcribes conversations, generates AI summaries, and emails you the meeting notes—all automatically!

## 📖 What Does This Project Do?

This project automates the entire Google Meet workflow from start to finish:

1. **Joins Google Meet** - Automatically opens browser and joins your meeting
2. **Introduces Itself** - Announces its presence using text-to-speech
3. **Records Audio** - Captures system audio throughout the meeting
4. **Waits for Meeting End** - Monitors when you leave or meeting ends
5. **Transcribes Audio** - Converts recording to text using AI
6. **Generates Summary** - Creates smart meeting notes with AI
7. **Emails Notes** - Sends summary to your email
8. **Cleans Up** - Deletes temporary files automatically

## 🏗️ Project Architecture

```
meet-assistant/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── automation/                # Browser automation scripts
│   │   └── playwright_demo.py     # Google Meet automation
│   ├── recording/                 # Audio recording modules
│   │   └── ffmpeg_recorder.py     # System audio capture
│   ├── transcription/             # Speech-to-text processing
│   │   └── whisper_transcribe.py  # Audio transcription
│   ├── notes/                     # AI summarization
│   │   └── groq_summarize.py      # Generate meeting notes
│   ├── services/                  # External services
│   │   └── send_email.py          # Email delivery
│   └── core/                      # Workflow orchestration
│       └── meeting_workflow.py    # LangGraph automation
├── recordings/                    # Audio files storage
├── transcripts/                   # Transcription files
├── notes/                         # Meeting summaries
└── .env                           # Configuration & secrets
```

## 🔧 Technologies & Libraries Used

### Core Framework
- **FastAPI** - Modern Python web framework for building APIs
  - *Role*: Provides modular structure and potential API endpoints

### Workflow Orchestration
- **LangGraph** - Graph-based workflow automation framework
  - *Role*: Orchestrates the entire automation sequence
  - *Why*: Manages state between steps, handles errors, controls flow

### Browser Automation
- **Playwright** - Modern browser automation library
  - *Role*: Opens browser, navigates to Google Meet, joins meeting
  - *Features*: Monitors meeting state, detects when you leave
  - *Why*: More reliable than Selenium, headless support

### Text-to-Speech
- **pyttsx3** - Offline text-to-speech engine
  - *Role*: Announces bot presence in meeting ("Hi, I'm meeting assistant")
  - *Why*: Works offline, no API costs, simple to use

### Audio Recording
- **FFmpeg** - Industry-standard multimedia framework
  - *Role*: Captures system audio during meeting
  - *How*: Runs via Python subprocess, records in MP3 format
  - *Why*: Best quality, cross-platform, widely supported

### Speech-to-Text (Transcription)
- **OpenAI Whisper** - State-of-the-art speech recognition AI
  - *Role*: Converts audio recording to accurate text transcript
  - *Why*: Most accurate transcription, handles multiple speakers
  - *Features*: Supports multiple languages, noise reduction

### AI Summarization
- **Groq API** - Ultra-fast LLM inference platform
  - *Model*: Uses llama-3.3-70b-versatile
  - *Role*: Reads transcript and generates structured meeting notes
  - *Output*: Key points, action items, decisions, participants
  - *Why*: Fast, affordable, high-quality summaries

### Email Delivery
- **SMTP (smtplib)** - Python's built-in email protocol
  - *Service*: Gmail SMTP server
  - *Role*: Sends meeting notes to your email
  - *Security*: Uses app-specific password, TLS encryption

### Configuration Management
- **python-dotenv** - Environment variable loader
  - *Role*: Loads credentials and settings from .env file
  - *Why*: Keeps secrets secure, easy configuration

## 🔄 How the Automation Works

### Step-by-Step Workflow

#### 1️⃣ **Join Meeting Node**
```
Library: Playwright
Function: join_meeting()
```
- Opens Chrome browser (headless or visible)
- Navigates to your Google Meet URL
- Automatically clicks "Join now" button
- Waits for meeting to load

#### 2️⃣ **Introduce Bot Node**
```
Library: pyttsx3
Function: introduce_bot()
```
- Uses text-to-speech to say: "Hi, I'm the meeting assistant"
- Lets participants know bot is recording
- Handles errors gracefully if TTS fails

#### 3️⃣ **Start Recording Node**
```
Library: FFmpeg
Function: start_recording()
```
- Launches FFmpeg in background process
- Captures system audio (what you hear)
- Saves to `recordings/meeting_audio_YYYYMMDD_HHMMSS.mp3`
- Continues recording until stopped

#### 4️⃣ **Monitor Meeting Node**
```
Library: Playwright
Function: monitor_meeting()
```
- Watches for "Leave call" button to disappear
- Checks every 5 seconds for meeting status
- Detects when you leave or meeting ends
- Triggers next step automatically

#### 5️⃣ **Stop Recording Node**
```
Library: FFmpeg
Function: stop_recording()
```
- Terminates FFmpeg process gracefully
- Finalizes audio file
- Ensures file is saved properly

#### 6️⃣ **Transcribe Audio Node**
```
Library: OpenAI Whisper
Function: transcribe_audio()
```
- Finds latest audio file in recordings folder
- Sends to Whisper API for transcription
- Saves transcript to `transcripts/transcript_YYYYMMDD_HHMMSS.txt`
- Returns transcript file path

#### 7️⃣ **Summarize Notes Node**
```
Library: Groq API (LLM)
Function: summarize_notes()
```
- Reads transcript file
- Sends to Groq LLM with prompt:
  - Extract key discussion points
  - Identify action items
  - List decisions made
  - Note participants mentioned
- Saves summary to `notes/notes_YYYYMMDD_HHMMSS.txt`
- Returns notes file path

#### 8️⃣ **Send Email Node**
```
Library: SMTP (Gmail)
Function: send_meeting_notes()
```
- Reads meeting notes file
- Connects to Gmail SMTP server
- Sends email with notes in body
- **Automatically deletes:**
  - Audio recording file
  - Transcript file
  - Notes file
- Keeps your folders clean!

### 🔗 Data Flow Between Nodes

```
join_meeting → introduce_bot → start_recording → monitor_meeting
                                       ↓
                                 stop_recording
                                       ↓
                                transcribe_audio
                         (returns transcript_path)
                                       ↓
                                 summarize_notes
                            (returns notes_path)
                                       ↓
                                  send_email
                          (deletes all temp files)
```

## ⚙️ Configuration Required

Create a `.env` file with:

```env
# Google Meet
MEET_URL=https://meet.google.com/your-meeting-code

# Email Settings (Gmail)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password
RECEIVER_EMAIL=recipient@example.com

# API Keys
GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-api-key
```

## 🚀 How to Run

### Install Dependencies
```bash
pip install fastapi uvicorn langgraph playwright pyttsx3 openai groq python-dotenv
playwright install chromium
```

### Run the Automation
```bash
PYTHONPATH=. python app/core/meeting_workflow.py
```

The system will:
- ✅ Join your meeting automatically
- ✅ Record the entire conversation
- ✅ Wait for meeting to end
- ✅ Transcribe and summarize
- ✅ Email you the notes
- ✅ Clean up all files

## 🎯 Key Features

### ✨ Fully Automated
No manual intervention needed—just start the script and let it work!

### 🧠 AI-Powered
Uses cutting-edge AI for transcription (Whisper) and summarization (Groq)

### 🔒 Secure
Credentials stored in .env file, not in code

### 🧹 Self-Cleaning
Automatically deletes temporary files after email is sent

### 📧 Email Delivery
Receive meeting notes directly in your inbox

### 🎤 Voice Announcement
Politely announces presence to meeting participants

### 🔍 Meeting Monitoring
Automatically detects when meeting ends

### 🎵 High-Quality Recording
Uses FFmpeg for professional audio capture

## 📚 Learning Purpose

This project demonstrates:
- **Modular Python Architecture** - Clean separation of concerns
- **Workflow Orchestration** - Using LangGraph for complex automation
- **API Integration** - Working with multiple external services
- **Browser Automation** - Controlling web applications programmatically
- **Audio Processing** - Recording and transcribing speech
- **AI/LLM Integration** - Using modern AI models for summarization
- **Error Handling** - Robust exception handling throughout
- **File Management** - Organized storage and cleanup
- **Environment Configuration** - Secure credential management

## 🔮 Future Enhancements

- Add scheduling (cron jobs for recurring meetings)
- Support multiple meeting platforms (Zoom, Teams)
- Real-time transcription during meeting
- Live dashboard to monitor automation status
- Multiple language support
- Speaker identification in transcripts
- Calendar integration
