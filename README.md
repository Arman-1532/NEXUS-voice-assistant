# NAFIS-voice-assistant

A simple, personal voice assistant for opening websites and executing basic commands using speech recognition and text-to-speech.

## About

This project (powered by `speech_recognition` and `pyttsx3`) listens for the wake word "nafis" and then listens for a command. The included `main.py` implements some commands and can be adapted to run other actions.

## Features

- Wake word: "nafis" (speak exactly "nafis" to activate the current `main.py` implementation)
- Text-to-speech feedback using `pyttsx3`
- Opens some web pages in the default browser 

## Requirements

- Python 3.8+
- macOS (instructions below) or Linux/Windows with a working microphone and PortAudio/PyAudio
- Packages: `SpeechRecognition`, `pyttsx3`, `pyaudio` (or an alternative audio input backend)

## Install (macOS)

1. Install Homebrew portaudio (needed for PyAudio):

```bash
brew install portaudio
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

If `pyaudio` installation fails, ensure `portaudio` is installed (see step 1) and retry.

## Usage

Run the assistant from the project root:

```bash
python3 main.py
```

You should hear the assistant say it is initializing. The console will print status messages. Say "nafis" (exactly, in the current code) to activate it. After activation, speak one of the supported commands such as:

- "open youtube"
- "open google"
- "open linkedin"
- "open facebook"

The assistant will speak a confirmation and open the corresponding website.

## Troubleshooting

- If you see errors about missing modules, make sure you installed the dependencies in the correct Python environment.
- If speech isn't recognized well, try running in a quieter room or increase microphone sensitivity and ambient noise adjustment in `main.py`.
- If you get `RequestError`, your machine may have no internet connection (Google recognizer uses an online API).

