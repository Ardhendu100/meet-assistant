mkdir meet-assistant
cd meet-assistant
python3 -m venv venv
source venv/bin/activate


install core packages

pip install fastapi langgraph playwright openai whisper uvicorn

Install Playwright browsers:
playwright install
Playwright is an open-source testing and automation framework used mainly for automating web browsers. Developers use it to test websites and web applications automatically.