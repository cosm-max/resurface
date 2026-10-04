# Resurface

**Rescue your screenshot graveyard.**

We screenshot things as reminders to ourselves: an event poster, a deadline, a flight, a product, an address. Then they sink into a gallery of thousands of images and never get looked at again. The screenshot *was* the to-do item, and nothing ever turns it into one.

Resurface is a Windows background app that watches your screenshots folder, asks for your permission, reads each screenshot with **Gemma**, sorts it into a category, and reminds you at the right time with a desktop notification.

Built for the Hacktoberfest Hack Day (Bengaluru, Oct 4, 2026).

## How it works

1. **Watch.** `watchdog` monitors the `screenshots/` folder for new images.
2. **Ask first.** When a new image appears, a small popup asks: *"Scan this screenshot?"* with **Scan it** or **Just a screenshot**. Nothing is read or sent anywhere unless you click Scan.
3. **Understand.** On consent, the image is sent to Gemma, which returns structured JSON: category, title, summary, date, time, location, suggested action, and whether it has already expired.
4. **Store.** Results are saved to a local SQLite database (`resurface.db`).
5. **Remind.** A scheduler (`APScheduler`) checks stored items and fires a Windows notification (`plyer`) before the date. Items with no date, and `notice` items, never trigger reminders.

Example output for an event poster:

```json
{
  "category": "event",
  "title": "Hacktoberfest Hack Day Bengaluru",
  "summary": "Build, experiment, and ship with open-source AI in one day.",
  "date": "2026-10-04",
  "time": "10:00",
  "location": "Bengaluru, Karnataka",
  "action": "Register at events.mlh.com",
  "expired": false
}
```

## Privacy

- **Consent first:** no screenshot is analyzed unless you click **Scan it**.
- **Local storage:** extracted data lives in a SQLite file on your machine and is excluded from Git.
- **Secrets stay out of the repo:** your API key lives in `.env`, which is git-ignored.
- **Honest limitation:** in the current version, a scanned image is sent to Google's Gemma API for analysis. A fully on-device mode is on the roadmap (see below).

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point; wires the watcher, popup, database and scheduler together |
| `watcher.py` | Watches the screenshots folder for new images |
| `ui.py` | Tkinter consent popup |
| `gemma_client.py` | Sends the image to Gemma and parses the JSON result |
| `db.py` | SQLite storage |
| `scheduler.py` | Decides when reminders are due |
| `notifier.py` | Shows Windows desktop notifications |

## Setup

Requires Windows and Python 3.10+.

```powershell
git clone https://github.com/cosm-max/resurface.git
cd resurface

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) and add your Gemini API key, which you can get from [Google AI Studio](https://aistudio.google.com):

```
GEMINI_API_KEY=your_key_here
```

## Run

```powershell
python main.py
```

Then drop or save any screenshot into the `screenshots/` folder. Click **Scan it** on the popup, and the result is printed in the terminal and saved to the database.

### Demo mode

`DEMO_MODE = True` (set at the top of `main.py`) makes reminders fire within seconds instead of on the real schedule, so you can see them without waiting. Set it to `False` for realistic timing.

## Roadmap

- Streamlit dashboard with tabs (Events, To Buy, Deadlines, Places) and a "done" button
- One-tap actions: export to calendar (.ics), copy address
- Local mode with Gemma running on-device (for example through Ollama), so nothing leaves the machine
- Phone screenshots: sync your phone's screenshot folder to the laptop (Syncthing or Google Drive) and let the watcher pick them up
- Semantic search ("that restaurant my cousin sent")
- Smarter handling of screenshots with no date, such as a gentle weekend nudge

## Tech stack

Python, Gemma (via the Gemini API), watchdog, Tkinter, SQLite, APScheduler, plyer.

## License

Add a license file before submitting (MIT is a common choice for hackathons).
