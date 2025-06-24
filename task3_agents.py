# task3.py

import asyncio
import json
from pathlib import Path
from openai_core.async_openai import AsyncOpenAI
# ── 1) your real trips and tools ──
from trips_data import TRIPS
from booking_tools import (
    search_trips,
    book_trip,
    cancel_booking,
)

# ── 2) OpenAI / ChatFire setup ──
API_KEY  = "sk-K0I3NbFfHA2RRhenI1ebHLAEPAb1vaBCreGMw7t8SveewCaI"
BASE_URL = "https://api.chatfire.cn/v1"
if not API_KEY.startswith("sk-"):
    raise RuntimeError("Please set API_KEY to your lab-provided sk-token.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)


async def call_gpt(system_prompt: str, user_content: str) -> str:
    """Wrapper for a single GPT-4O chat completion."""
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ],
        temperature=0.0,
    )
    return resp.choices[0].message.content


async def generate_dsl_artifacts():
    """Run the 4‐step DSL workflow and save JSON files."""
    # Step 1: UseCaseDSL
    uc_prompt = (
        "You are the UseCaseAgent for BookMyTrip.\n"
        "Based on these trips:\n"
        f"{json.dumps(TRIPS, indent=2)}\n\n"
        "Generate a JSON object with:\n"
        "  • systemName (string),\n"
        "  • usecases (array of { name, includes, extends })."
    )
    usecase_json = await call_gpt(uc_prompt, "")
    Path("UseCaseDSL.json").write_text(usecase_json, encoding="utf-8")
    print("✔︎ Saved UseCaseDSL.json")

    # Step 2: SSDDSL
    ssd_prompt = (
        "You are the SSDAgent for BookMyTrip.\n"
        "Given the UseCaseDSL JSON, produce a JSON array of:\n"
        "  { usecase, lifelines: [...], messages: [ { from_role, to_role, action } ] }"
    )
    ssd_json = await call_gpt(ssd_prompt, usecase_json)
    Path("SSDDSL.json").write_text(ssd_json, encoding="utf-8")
    print("✔︎ Saved SSDDSL.json")

    # Step 3: ClassDSL
    class_prompt = (
        "You are the ClassAgent for BookMyTrip.\n"
        "Given UseCaseDSL and SSDDSL JSONs, generate a conceptual class diagram JSON with key:\n"
        "  classes: [ { name, attributes: [ {name,type} ], relationships: [ {type,target,multiplicity} ] } ]"
    )
    class_json = await call_gpt(class_prompt, usecase_json + "\n\n" + ssd_json)
    Path("ClassDSL.json").write_text(class_json, encoding="utf-8")
    print("✔︎ Saved ClassDSL.json")

    # Step 4: OCLDSL
    ocl_prompt = (
        "You are the OCLAgent for BookMyTrip.\n"
        "Given the ClassDSL JSON, generate a JSON object with:\n"
        "  invariants:    [ { name, constraint } ],\n"
        "  preconditions: [ { name, on, constraint } ],\n"
        "  postconditions:[ { name, on, constraint } ]."
    )
    ocl_json = await call_gpt(ocl_prompt, class_json)
    Path("OCLDSL.json").write_text(ocl_json, encoding="utf-8")
    print("✔︎ Saved OCLDSL.json")

    print("\n🏁 DSL workflow complete.")


async def interactive_cli():
    """Simple menu: search/book/cancel trips, or regenerate DSL."""
    while True:
        print("\n=== BookMyTrip CLI ===")
        print("1) List all trips")
        print("2) Search by max budget")
        print("3) Book a trip")
        print("4) Cancel a booking")
        print("5) Regenerate DSL artifacts")
        print("0) Exit")
        choice = input("→ ").strip()

        if choice == "0":
            break
        elif choice == "1":
            for t in TRIPS:
                print(f" {t['id']}: {t['destination']} {t['start']}→{t['end']} @ ${t['price']}")
        elif choice == "2":
            b = float(input(" Max budget? $"))
            results = search_trips(TRIPS, b)
            if not results:
                print(" No trips match.")
            else:
                for t in results:
                    print(f" {t['id']}: {t['destination']} @ ${t['price']}")
        elif choice == "3":
            uid = input(" Your user ID: ").strip()
            tid = input(" Trip ID to book: ").strip()
            try:
                booking = book_trip(uid, tid)
                print(f"✅ Booked: {booking}")
            except ValueError as e:
                print("❌", e)
        elif choice == "4":
            bid = input(" Booking ID to cancel: ").strip()
            ok = cancel_booking(bid)
            print("✅ Canceled" if ok else "❌ Not found")
        elif choice == "5":
            print("Regenerating DSL…")
            await generate_dsl_artifacts()
        else:
            print("Invalid choice.")


async def main():
    # First generate your DSL artifacts
    await generate_dsl_artifacts()
    # Then drop into the interactive CLI
    await interactive_cli()

if __name__ == "__main__":
    asyncio.run(main())
