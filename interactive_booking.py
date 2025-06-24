# interactive_booking.py

import asyncio
import json

from task3_agents import generate_dsl_artifacts as build_models
from trips_data         import TRIPS
from booking_tools      import search_trips, book_trip, cancel_booking
from openai_core.async_openai import AsyncOpenAI
from providers.openai_provider import OpenAIProvider
from agents.tool        import function_tool
from agents.agent       import Agent
from agents.run         import Runner, RunConfig

API_KEY  = "sk-K0I3NbFfHA2RRhenI1ebHLAEPAb1vaBCreGMw7t8SveewCaI"
BASE_URL = "https://api.chatfire.cn/v1"

async def interactive():
    # ── 1) Build your DSL once ───────────────────────────────────────────────
    print("🔧 Generating requirement models (Task 3)...")
    uc, ssds, cls, ocl = await build_models()
    print("✅ Requirement models ready.\n")

    # ── 2) Set up a provider for the booking agent ───────────────────────────
    provider = OpenAIProvider(
        openai_client=AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY),
        use_responses=False
    )

    # ── 3) Wrap your Python tools as LLM‐callable functions ──────────────────
    @function_tool
    def fn_search(destination: str = None, budget: float = None):
        return search_trips(TRIPS, destination=destination, budget=budget)

    @function_tool
    def fn_book(trip_id: str, user_id: str):
        return book_trip(trip_id, user_id)

    @function_tool
    def fn_cancel(booking_id: str):
        return cancel_booking(booking_id)

    # ── 4) Define a single BookingAgent with all three tools ─────────────────
    booking_agent = Agent(
        name="BookingAgent",
        model="gpt-4o",
        instructions="""
You are the BookMyTrip assistant.  The user may ask you to search for trips,
to book a trip, or to cancel a booking.  Use the provided functions:

  • fn_search(destination, budget)
  • fn_book(trip_id, user_id)
  • fn_cancel(booking_id)

Call exactly one tool per user request, then return the tool’s JSON result
as your reply.
""",
        tools=[fn_search, fn_book, fn_cancel],
    )

    # ── 5) Interactive REPL ────────────────────────────────────────────────
    conversation = [{"role":"system","content":booking_agent.instructions}]
    print("💬 Welcome to BookMyTrip!  Type ‘exit’ to quit.\n")

    while True:
        user_input = input("You> ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break

        conversation.append({"role":"user","content":user_input})

        result = await Runner.run(
            booking_agent,
            conversation,
            run_config=RunConfig(model_provider=provider)
        )
        # final_output is the dataclass / dict returned by your tool
        output = result.final_output
        print("Bot> ", json.dumps(output, indent=2), "\n")

        # feed the assistant’s last reply back into the context
        conversation.append({"role":"assistant","content":json.dumps(output)})

if __name__ == "__main__":
    asyncio.run(interactive())
