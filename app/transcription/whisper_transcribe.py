import os
import glob
import whisper

RECORDINGS_DIR = "recordings"
TRANSCRIPTS_DIR = "transcripts"
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def get_latest_audio():
    files = glob.glob(os.path.join(RECORDINGS_DIR, "meeting_audio_*.wav"))
    if not files:
        raise FileNotFoundError("No meeting audio files found.")
    return max(files, key=os.path.getctime)

def transcribe_audio(audio_path):
    model = whisper.load_model("medium")  # You can use 'small', 'medium', 'large' if you have resources
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path, language="en", fp16=False)  # Set fp16=False for CPU
    transcript = result["text"]
    return transcript

def save_transcript(transcript, audio_path):
    base = os.path.basename(audio_path).replace(".wav", ".txt")
    out_path = os.path.join(TRANSCRIPTS_DIR, base)
    with open(out_path, "w") as f:
        f.write(transcript)
    print(f"Transcript saved to {out_path}")
    return out_path

if __name__ == "__main__":
    audio_path = get_latest_audio()
    transcript = transcribe_audio(audio_path)
    save_transcript(transcript, audio_path)
