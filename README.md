# NEXUS Voice Assistant

A compact, personal voice assistant that listens for the wake word "nexus" and then executes simple voice commands: opening websites, playing saved video links, fetching top news, or forwarding general queries to a hosted language model (GitHub Models API).

This README documents the project's features, how to configure and run it, available voice commands, and troubleshooting tips.



## Table of contents

- About
- Features
- Project structure
- Requirements
- Environment variables
- Installation
- How it works / architecture
- Voice commands and examples
- Playable items (supported `play` keywords)
- Supported websites (supported `open` keywords)
- Troubleshooting




## About

This project uses:
- `speech_recognition` for speech -> text (Google recognizer by default)
- `pyttsx3` for text-to-speech feedback
- `webbrowser` to open URLs in the default browser
- `requests` to call the GitHub Models inference endpoint and a news API

The current assistant implementation lives in `main.py`. It delegates to two small lookup libraries:
- `playable_Library.py` — mapping of short keywords to YouTube links (used by the `play` command)
- `sites_Library.py` — mapping of site keywords to URLs (used by the `open` command)




## Features

- Wake-word activation: say "nexus" to activate the assistant
- Open predefined websites with: "open <site>"
- Play predefined videos with: "play <keyword>"
- Read top headlines when you say "news" (requires `NEWS_API_KEY`)
- General conversational queries are forwarded to the GitHub Models inference API and the response is spoken back



## Project structure (key files)

- `main.py` — main assistant loop and command processing
- `playable_Library.py` — a dict of playable keywords -> YouTube links
- `sites_Library.py` — a dict of site keywords -> URL
- `requirements.txt` — Python dependency list



## Requirements

- Python 3.8+
- Operating system: macOS / Linux / Windows with a working microphone
- On macOS, install PortAudio before installing PyAudio: `brew install portaudio` (if using `pyaudio`)

Recommended workflow: create a Python virtual environment and install dependencies with `pip`.



## Environment variables

The assistant reads a few environment variables for optional features:

- `GITHUB_MODELS_TOKEN` (required for the GitHub Models integration) — used by `main.py` to call the GitHub Models inference endpoint.
- `NEWS_API_KEY` (required for the `news` command) — used to fetch top headlines from a news provider.




## Installation

1. Clone the repository and change into the project directory.
2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Add your keys to `.env` (see "Environment variables" above).



## How it works / architecture (short)

1. `main.py` runs a loop that listens on the microphone.
2. Saying "nexus" activates the assistant; it then listens for a follow-up command.
3. The follow-up command is processed by `processCommand()`:
   - `open <site>` → opens URL from `sites_Library.py`.
   - `play <keyword>` → opens a YouTube link from `playable_Library.py`.
   - `news` → calls the News API and speaks top headlines.
   - anything else → forwarded to `ask_github_model()` which calls the GitHub Models inference endpoint and speaks the returned answer.

Speech-to-text is handled by `speech_recognition` (Google recognizer) and speech output uses `pyttsx3`.



## Voice commands and examples

Start by saying the wake word exactly: "nexus"

After you hear the assistant confirm, try these commands:

- Open a website:
  - "open youtube" — opens YouTube
  - "open google" — opens Google
  - Example: say: nexus → yes → open youtube

- Play a saved video (keyword-based):
  - "play lofi" — opens the lofi video mapped in `playable_Library.py`
  - Example: say: nexus → yes → play piano

- Read top news:
  - Say: "news"
  - The assistant will call the configured news API, then speak headlines one by one.

- Ask general questions / perform conversational prompts:
  - Say any question that is not `open`/`play`/`news` and the assistant will forward it to the GitHub Models endpoint and speak the returned response.

- Exit / deactivate:
  - Say: "exit", "quit", or "deactivate" to stop the assistant after activation.



## Playable items (supported `play` keywords)

The following keywords are supported by `playable_Library.py` and will open their mapped YouTube links when you say `play <keyword>`:

wolf, space, study, relax, motivation, coding, python, javascript, machine, neural, quantum, galaxy, meditation, energy, rain, ambience, forest, lofi, anime, nature, medieval, piano, sunset, rainbow, city, travel, island, storm, snow, birds, calm, zen, deep, vibes

(These map to the YouTube links held in `playable_Library.py`. You can add or remove entries in that file to customize your library.)



## Supported websites (supported `open` keywords)

The following site keywords are supported by `sites_Library.py` and will open in your default browser when you say `open <site>`:

google, youtube, facebook, instagram, linkedin, github, gmail



## Troubleshooting and tips

- Microphone not detected / recognition errors:
  - Make sure your OS microphone permissions are granted for Python/Terminal.
  - Try running in a quieter room and increase ambient noise adjustment in the code if needed.

- `pyaudio` installation fails on macOS:
  - Install PortAudio with Homebrew: `brew install portaudio` then reinstall requirements.

- GitHub Models or News API requests fail:
  - Verify `GITHUB_MODELS_TOKEN` and `NEWS_API_KEY` environment variables are set and valid.
  - Check network/firewall settings.

- Responses are repetitive or 'same every time':
  - If using a model endpoint, tweak model parameters on the server side (temperature) or in the client.
  - Confirm different prompts are being sent; add logging to `main.py` to inspect the exact prompt.
