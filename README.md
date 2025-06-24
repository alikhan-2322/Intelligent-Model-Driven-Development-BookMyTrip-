# BookMyTrip Lab Report

**Course**: Intelligent Model-Driven Development  
**Author**: Muhammad Ali Khan  
**Date**: June 2025  

---

## Overview

This lab explores three progressive methods for automated requirements modeling of a travel-booking system:

1. **Task 1 – RESTful API**  
   Direct HTTP POSTs to the ChatFire `/chat/completions` endpoint.  
2. **Task 2 – OpenAI SDK**  
   The same prompts via the official Python client for cleaner integration.  
3. **Task 3 – MultiAgent Workflow**  
   Four specialized GPT-4O agents producing a full JSON-based DSL for:
   - Use-Case Diagrams  
   - System Sequence Diagrams  
   - Conceptual Class Diagrams  
   - OCL Constraints  
   plus an **interactive CLI** with real trip-booking capabilities.

---

## Task 1: ChatFire REST API

- **Objective**  
  Learn the raw HTTP interface (Section 9.1).

- **Approach**  
  1. Hard-code the lab API key and base URL (`https://api.chatfire.cn/v1`).  
  2. Build minimal JSON messages: a “developer” system role and a “user” prompt.  
  3. POST to `/chat/completions` with `model="gpt-4o"` and `temperature=0.0`.  
  4. Save the full JSON response as `usecases_raw.json` and extract the assistant’s plain-text reply into `usecases.txt`.

- **Outputs**  
  - `usecases.txt`: numbered list of core use-cases (e.g. “1. SearchTrips”)  
  - `usecases_raw.json`: full API response  

> **Screenshot**  
> *![Task 1 Console](lab4_images/task1%20console.png)*

---

## Task 2: OpenAI Python SDK

- **Objective**  
  Perform the same generation using the official Python SDK (Section 9.2).

- **Approach**  
  1. Initialize the `OpenAI` client pointing to the ChatFire base URL with the same token.  
  2. Call the chat completion method with identical messages and parameters.  
  3. Serialize the SDK’s response object to a Python dict → `usecases_raw.json`.  
  4. Extract and save the assistant’s text to `usecases.txt`.

- **Outputs**  
  - `usecases.txt`: matching use-case list  
  - `usecases_raw.json`: SDK-formatted JSON  

> **Screenshot**  
> *![Task 2 Console](lab4_images/task2%20console.png)*

---

## Task 3: MultiAgent DSL Workflow

### A. Trip Data & Booking Tools

- **`trips_data.py`** defines 10 sample trips (`id`, `destination`, `start`, `end`, `price`).  
- **`booking_tools.py`** provides simple in-memory functions:
  - Search by budget  
  - Book a trip (returns booking record)  
  - Cancel a booking  

### B. Agent Definitions & Sequential Workflow

Four GPT-4O agents each emit one piece of the requirements model in JSON:

| Agent           | Prompt Description                  | DSL Structure                                                 | Output File        |
| --------------- | ----------------------------------- | ------------------------------------------------------------- | ------------------ |
| **UseCaseAgent** | Generate use-case JSON              | `{ systemName, usecases:[{name,includes,extends},…] }`         | `UseCaseDSL.json`  |
| **SSDAgent**     | Build sequence diagrams             | `[{usecase, lifelines:[…], messages:[{from_role,to_role,action}]}]` | `SSDDSL.json`      |
| **ClassAgent**   | Produce class diagram               | `{ classes:[{ name, attributes:[{name,type}], relationships:[{type,target,multiplicity}] }]} ` | `ClassDSL.json`    |
| **OCLAgent**     | Emit OCL constraints                | `{ invariants:[{name,constraint}], preconditions:[…], postconditions:[…] }` | `OCLDSL.json`      |

Each agent runs in sequence, passing its JSON output as the next agent’s input.

### C. Interactive CLI

After generating all four DSL artifacts, the script presents a console menu to:

1. List all predefined trips  
2. Search trips by maximum budget  
3. Book a trip (prints booking confirmation)  
4. Cancel an existing booking  
5. Regenerate all DSL artifacts on demand  

> **Screenshots**  
> -  *![Task 3 Console](lab4_images/task3%20console.png)*  
> -      *![Task 3 Console](lab4_images/Task3%20imports.png)*  
> -    *![Task 3 Console](lab4_images/Task3%20Define%20agent.png)*  
> -      *![Task 3 Console](lab4_images/Task3%20fuction_tool.png)*  
> -  *![Task 3 Console](lab4_images/Task3%20asyncio.run.png)*
> -  [Click here to view Task 3 video](lab4_images/task3%20video.mp4)

---

## Conclusion

- **Task 1** provided hands-on experience with raw HTTP calls.  
- **Task 2** showcased SDK-based integration for cleaner code.  
- **Task 3** delivered a full model-driven pipeline, chaining multiple LLM agents to produce structured, formalized requirements artifacts, backed by real trip data and an interactive CLI.

This workflow demonstrates how LLMs can be orchestrated to generate end-to-end requirements models—including diagrams and constraints—driven entirely by code and real data.

---

_End of Report_  
