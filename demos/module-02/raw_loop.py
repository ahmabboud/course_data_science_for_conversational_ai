"""Module 2: the raw agent loop, with nothing hidden.

Used in lectures/dsca-module-02.html, slide 3 ("The raw agent loop, with
nothing hidden") and slide 12 ("Walkthrough: the raw loop, one call at a
time"). Run directly, no LangGraph, no CLI:

    python raw_loop.py

Prints the messages array after every step, so you see exactly what
graph.py's LangGraph version is managing under the hood: one growing list,
one model call, one appended tool result, repeated. Compare the two files
side by side, they call the model the same way, the only difference is
whether the state and the branching are explicit or implicit.
"""

import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

FAKE_ORDERS = {
    "A100": "shipped, arriving Thursday",
    "A200": "still processing, no ship date yet",
}

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["answer", "call_tool", "escalate"]},
        "reply": {"type": ["string", "null"]},
        "order_id": {"type": ["string", "null"]},
        "reason": {"type": ["string", "null"]},
    },
    "required": ["action", "reply", "order_id", "reason"],
}

SYSTEM_PROMPT = (
    "You are an order-status agent. You can call get_order_status(order_id) "
    "to look up a real order. If the user asks something outside order "
    "status, set action to escalate instead of guessing. Only set action to "
    "answer once you have a tool result to answer from, or the request "
    "needs no lookup at all."
)


def get_order_status(order_id: str) -> str:
    """The real lookup, run by hand once the model asks for it. Mocked
    here on purpose, same fake backend as graph.py."""
    return FAKE_ORDERS.get(order_id, f"no order found for '{order_id}'")


def call_model(messages: list[dict]) -> dict:
    """One call, the whole array sent every time. Identical to graph.py's
    call_model: LangGraph does not change how the model is called."""
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=transcript,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": DECISION_SCHEMA,
        },
    )
    return json.loads(interaction.output_text)


def show(step_label: str, messages: list[dict]) -> None:
    print(f"--- {step_label} ---")
    print(json.dumps(messages, indent=2))
    print()


def run(turn: str) -> list[dict]:
    # Step 1: start the array. Nothing exists yet except the system
    # message and this turn.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": turn},
    ]
    show("step 1: state after appending the user turn", messages)

    # Step 2: append the result, call the model with the whole array.
    decision = call_model(messages)
    messages.append(
        {"role": "assistant", "content": decision.get("reply") or f"[{decision['action']}]"}
    )
    show("step 2: state after the model's first decision", messages)

    # Step 3 and 4 only happen if the model asked for a tool. If it
    # answered or escalated directly, the loop is already done.
    if decision["action"] == "call_tool":
        result = get_order_status(decision.get("order_id") or "")
        messages.append({"role": "tool", "content": result})
        show("step 3: state after running the tool by hand", messages)

        decision = call_model(messages)
        messages.append(
            {"role": "assistant", "content": decision.get("reply") or f"[{decision['action']}]"}
        )
        show("step 4: state after looping back to the model", messages)

    return messages


if __name__ == "__main__":
    run("can you check if order A100 shipped yet?")
