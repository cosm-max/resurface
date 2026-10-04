import os
import json
from datetime import date
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

MODEL = "gemma-4-26b-a4b-it"


def analyze_image(image_path):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Check your .env file.")
        return None

    client = genai.Client(api_key=api_key)

    prompt = f"""You sort screenshots for a personal reminder app. Return JSON in EXACTLY this shape:
{{
  "category": "event|deadline|to_buy|place|recipe|notice|reference|none",
  "title": "Short title",
  "summary": "One sentence",
  "date_text": "exact words in the image that state a future date, else null",
  "date": "YYYY-MM-DD or null",
  "time": "HH:MM or null",
  "location": "Location if any, else null",
  "action": "What the person should do, else null",
  "expired": false
}}

Categories:
- event: a gathering, class, meeting or appointment someone is invited to
- deadline: a bill, payment, form or task due by a date
- to_buy: a product, price or item to purchase
- place: a restaurant, shop or location to visit
- recipe: cooking instructions
- notice: a warning, safety alert, rule or announcement from an authority (hostel, school, workplace, government)
- reference: useful info to keep (tickets, codes, addresses, tips) with nothing to do
- none: memes, selfies, casual chat, random images, nothing useful

Today's date is {date.today().isoformat()}.
Rules:
- Chat labels like "Today" or "Yesterday" and message timestamps are NOT event dates. Ignore them.
- Fill "date" and "time" ONLY if the image states when something will happen or is due.
  Copy those exact words into "date_text". Otherwise date_text, date and time must be null.
- Never guess. Use null when unsure.
Return ONLY the JSON."""

    try:
        img = Image.open(image_path)
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt, img],
        )
        raw_text = response.text.strip()
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1:
            print("Gemma did not return JSON:", raw_text[:200])
            return None
        data = json.loads(raw_text[start:end + 1])

        if not data.get("date_text"):
            data["date"] = None
            data["time"] = None
        data.pop("date_text", None)
        return data
    except Exception as e:
        print(f"Error analyzing image with Gemma: {e}")
        return None