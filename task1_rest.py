# task1_rest.py
import json
import requests

# ── HARD‐CODED LAB TOKEN ──
# Make sure this is the exact key you verified with /models (no extra spaces).
api_key = "sk-K0I3NbFfHA2RRhenI1ebHLAEPAb1vaBCreGMw7t8SveewCaI"
if not api_key.startswith("sk-"):
    raise RuntimeError("Please replace api_key with your verified lab‐provided token.")

# ── BASE_URL FROM LAB INSTRUCTIONS ──
BASE_URL = "https://api.chatfire.cn/v1"
endpoint = f"{BASE_URL}/chat/completions"

# ── Section 9.1: Must use 'Authorization: Bearer <api_key>' ──
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def call_chatfire(messages_list, filename_raw, filename_clean):

    payload = {
        "model": "gpt-4o",            # EXACTLY as Section 9.1 shows
        "messages": messages_list,
        "temperature": 0.0
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    # Save the full JSON response
    with open(filename_raw, "w", encoding="utf-8") as fr:
        json.dump(result, fr, indent=2)

    # Extract the assistant’s reply
    assistant_text = result["choices"][0]["message"]["content"]

    # Save only the assistant’s plain text
    with open(filename_clean, "w", encoding="utf-8") as fc:
        fc.write(assistant_text.strip())

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
    return call_chatfire(messages_list, "usecases_raw.json", "usecases.txt")

def generate_data_model():
    with open("usecases.txt", "r", encoding="utf-8") as f:
        uc = f.read().strip()

    prompt_text = (
        f"Based on these use-cases:\n{uc}\n\n"
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
    return call_chatfire(messages_list, "data_model_raw.json", "data_model.txt")

def generate_api_endpoints():
    with open("usecases.txt", "r", encoding="utf-8") as f_uc:
        uc = f_uc.read().strip()
    with open("data_model.txt", "r", encoding="utf-8") as f_dm:
        dm = f_dm.read().strip()

    prompt_text = (
        f"Given these use-cases:\n{uc}\n\n"
        f"And this data model:\n{dm}\n\n"
        "List all the REST API endpoints for BookMyTrip. For each endpoint, specify:\n"
        "- HTTP method\n"
        "- Path\n"
        "- One-line description (for example: GET /trips – Retrieve a list of trips)."
    )
    messages_list = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user",      "content": prompt_text}
    ]
    return call_chatfire(messages_list, "api_endpoints_raw.json", "api_endpoints.txt")

def main():
    print("--- Generating Use-Cases ---")
    generate_usecases()
    print("\n--- Generating Data Model ---")
    generate_data_model()
    print("\n--- Generating API Endpoints ---")
    generate_api_endpoints()
    print("\n✅ All Task 1 artifacts have been generated. Please review the JSON and TXT files in your project folder.")

if __name__ == "__main__":
    main()
