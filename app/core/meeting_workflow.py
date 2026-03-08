from langgraph.graph import StateGraph, START, END
import os
import glob
from app.automation.playwright_demo import main as join_meeting_main
from app.recording.ffmpeg_recorder import FFmpegRecorder
from app.transcription.whisper_transcribe import transcribe_audio, get_latest_audio, save_transcript
from app.notes.groq_summarize import summarize_notes
from app.services.send_email import send_meeting_notes

# run PYTHONPATH=. python app/core/meeting_workflow.py
# Node: Join Meeting (browser automation)
def join_meeting_node(data):
    print("Joining meeting...")
    join_meeting_main()  # Runs the Playwright automation
    return {"step": "join_meeting", "data": data}

# Node: Record Audio
def record_audio_node(data):
    print("Recording audio...")
    # Audio recording is handled in join_meeting_main, so just return
    return {"step": "record_audio", "data": data}

# Node: Transcribe Audio
def transcribe_audio_node(data):
    print("Transcribing audio...")
    audio_path = get_latest_audio()
    transcript = transcribe_audio(audio_path)
    transcript_path = save_transcript(transcript, audio_path)
    return {"step": "transcribe_audio", "transcript_path": transcript_path, "data": data}

# Node: Summarize Notes
def summarize_notes_node(data):
    print("Summarizing notes...")
    # Get latest transcript
    files = glob.glob(os.path.join("transcripts", "meeting_audio_*.txt"))
    if files:
        latest_transcript = max(files, key=os.path.getctime)
        notes_path = summarize_notes(latest_transcript)
        return {"step": "summarize_notes", "notes_path": notes_path, "data": data}
    return {"step": "summarize_notes", "data": data}

# Node: Send Email
def send_email_node(data):
    print("Sending email...")
    # Get latest notes
    files = glob.glob(os.path.join("notes", "meeting_audio_*_notes.txt"))
    if files:
        latest_notes = max(files, key=os.path.getctime)
        send_meeting_notes(latest_notes)
    return {"step": "send_email", "data": data}

# Build the graph
workflow_graph = StateGraph(dict)
workflow_graph.add_node("join_meeting", join_meeting_node)
workflow_graph.add_node("record_audio", record_audio_node)
workflow_graph.add_node("transcribe_audio", transcribe_audio_node)
workflow_graph.add_node("summarize_notes", summarize_notes_node)
workflow_graph.add_node("send_email", send_email_node)

# Connect nodes
workflow_graph.add_edge(START, "join_meeting")
workflow_graph.add_edge("join_meeting", "record_audio")
workflow_graph.add_edge("record_audio", "transcribe_audio")
workflow_graph.add_edge("transcribe_audio", "summarize_notes")
workflow_graph.add_edge("summarize_notes", "send_email")
workflow_graph.add_edge("send_email", END)

workflow = workflow_graph.compile()

if __name__ == "__main__":
    result = workflow.invoke({"input": "Start meeting workflow"})
    print("Workflow result:", result)
