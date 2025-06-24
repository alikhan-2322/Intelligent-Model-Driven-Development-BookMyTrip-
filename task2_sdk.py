# task2_sdk.py

import json
from openai import OpenAI
from openai.types.chat import ChatCompletion
from dotenv import load_dotenv
import os

# read .env from project root
load_dotenv()
API_KEY = os.getenv("BOOKMYTRIP_API_KEY")
if not API_KEY or not API_KEY.startswith("sk-"):
    raise RuntimeError("Please set BOOKMYTRIP_API_KEY in your .env file")


# ── BASE_URL FROM LAB INSTRUCTIONS ──
BASE_URL = "https://api.chatfire.cn/v1"

# ── Create an OpenAI client pointed at ChatFire ──
client: OpenAI = OpenAI(base_url=BASE_URL, api_key=API_KEY)

def call_sdk(messages_list, filename_raw, filename_clean):
    """
    Uses the OpenAI SDK to call ChatFire /chat/completions.
    Saves full JSON to filename_raw and assistant's content to filename_clean.
    """
    # 1) Create a ChatCompletion via the SDK
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o",           # EXACTLY as Section 9.2 prescribes
        messages=messages_list,
        temperature=0.0
    )

    # 2) The SDK returns an object whose .choices[0].message.content is the text
    assistant_text = completion.choices[0].message.content

    # 3) Convert the full response to a JSON-serializable dict
    raw_dict = completion.to_dict()

    # 4) Save the raw JSON dictionary
    with open(filename_raw, "w", encoding="utf-8") as f_raw:
        json.dump(raw_dict, f_raw, indent=2)

    # 5) Write the assistant text to a clean file
    with open(filename_clean, "w", encoding="utf-8") as f_clean:
        f_clean.write(assistant_text.strip())

    print(f"⟶ Wrote full JSON to {filename_raw}")
    print(f"⟶ Wrote cleaned text to {filename_clean}")

    return assistant_text.strip()


def generate_usecases():
    prompt_text = (
        "List all of the core use-cases for a BookMyTrip application. Assume users can:\n"
        "- search for trips (by destination, date, budget),\n"
        "- compare prices across trip types (e.g., CulturalHeritage, NatureEscape),\n"
        "- book a trip, and\n"
        "- cancel a booking.\n\n"
        "Return a numbered list of use-case names (for example: 1. SearchTrips)."
    )
    messages_list = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user",      "content": prompt_text}
    ]
    return call_sdk(messages_list, "usecases_raw.json", "usecases.txt")


def generate_data_model():
    with open("usecases.txt", "r", encoding="utf-8") as f_uc:
        uc_text = f_uc.read().strip()

    prompt_text = (
        f"Based on these use-cases:\n{uc_text}\n\n"
        "Generate a simple data model for BookMyTrip. Include 3–5 entities and their key fields. "
        "For example:\n"
        "- Trip {id, destination, startDate, endDate, price}\n"
        "- Booking {id, userId, tripId, status}\n"
        "- User {id, name, email}\n\n"
        "Return a bullet list describing each entity and its fields."
    )
    messages_list = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user",      "content": prompt_text}
    ]
    return call_sdk(messages_list, "data_model_raw.json", "data_model.txt")


def generate_api_endpoints():
    with open("usecases.txt",    "r", encoding="utf-8") as f_uc:
        uc_text = f_uc.read().strip()
    with open("data_model.txt",  "r", encoding="utf-8") as f_dm:
        dm_text = f_dm.read().strip()

    prompt_text = (
        f"Given these use-cases:\n{uc_text}\n\n"
        f"And this data model:\n{dm_text}\n\n"
        "List all the REST API endpoints for BookMyTrip. For each endpoint, specify:\n"
        "- HTTP method\n"
        "- Path\n"
        "- One-line description (for example: GET /trips – Retrieve a list of trips)."
    )
    messages_list = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user",      "content": prompt_text}
    ]
    return call_sdk(messages_list, "api_endpoints_raw.json", "api_endpoints.txt")


def main():
    print("--- Generating Use-Cases (Task 2 via SDK) ---")
    generate_usecases()
    print("\n--- Generating Data Model (Task 2 via SDK) ---")
    generate_data_model()
    print("\n--- Generating API Endpoints (Task 2 via SDK) ---")
    generate_api_endpoints()
    print("\n✅ All Task 2 artifacts have been generated. Please review the JSON and TXT files in your project folder.")


if __name__ == "__main__":
    main()
