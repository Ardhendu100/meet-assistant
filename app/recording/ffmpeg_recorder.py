import subprocess
import time

class FFmpegRecorder:
    def __init__(self, output_file="meeting_audio.wav", device="default"):
        self.output_file = output_file
        self.device = device
        self.process = None

    def start(self):
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if exists
            "-f", "pulse",
            "-i", self.device,
            self.output_file
        ]
        print(f"Starting ffmpeg recording on device '{self.device}' to '{self.output_file}'...")
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop(self):
        if self.process:
            print("Stopping ffmpeg recording...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print(f"Recording saved to '{self.output_file}'")
        else:
            print("No recording process to stop.")

if __name__ == "__main__":
    # Example usage: record for 10 seconds
    recorder = FFmpegRecorder(output_file="test_meeting.wav", device="default")
    recorder.start()
    time.sleep(10)
    recorder.stop()
