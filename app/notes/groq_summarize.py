import os
import requests
import glob
from dotenv import load_dotenv

def summarize_notes(transcript_path=None, model="llama-3.3-70b-versatile"):
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TRANSCRIPTS_DIR = "transcripts"
    NOTES_DIR = "notes"
    os.makedirs(NOTES_DIR, exist_ok=True)

    # Find latest transcript if not provided
    if not transcript_path:
        files = glob.glob(os.path.join(TRANSCRIPTS_DIR, "meeting_audio_*.txt"))
        if not files:
            raise FileNotFoundError("No transcript files found.")
        transcript_path = max(files, key=os.path.getctime)

    with open(transcript_path, "r") as f:
        transcript = f.read()

    prompt = f"""
Summarize the following meeting transcript.

Provide:
1. Summary
2. Key discussion points
3. Action items
4. Decisions

Transcript:
{transcript}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "temperature": 0.3,
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI meeting assistant that generates structured meeting notes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.text}")

    notes = response.json()["choices"][0]["message"]["content"]

    # Save notes
    base = os.path.basename(transcript_path).replace(".txt", "_notes.txt")
    out_path = os.path.join(NOTES_DIR, base)

    with open(out_path, "w") as f:
        f.write(notes)

    print(f"Meeting notes saved to {out_path}")
    return out_path

if __name__ == "__main__":
    summarize_notes()