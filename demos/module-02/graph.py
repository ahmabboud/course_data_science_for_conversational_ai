"""Module 2: the same order-status agent, rebuilt on LangGraph.

Used in lectures/dsca-module-02.html, slide 5 ("LangGraph: nodes, edges,
and state as one object") and slide 9 ("The one multi-agent pattern this
course teaches: routing and escalation"). Run this with `langgraph dev`
from this folder (see ../README.md for setup) to open LangGraph Studio and
step through the exact graph those two slides' boards describe: an agent
node that decides, a tool node that runs the real lookup and loops back,
and an escalate node for anything out of scope.

The point of this file is that nothing about calling the model changed
from raw_loop.py in this same folder: it is the same client.interactions.create
call, the same schema-as-contract idea from Module 1. What LangGraph adds
is structure around that call, an explicit state object and named edges,
not a new way of talking to Gemini. Compare this file to raw_loop.py
side by side if that is not obvious yet.
"""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph

DEMO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(DEMO_ROOT / ".env")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Mock backend: swap for your team's own tool, the graph shape around it
# does not change. This is deliberately not a real order system.
FAKE_ORDERS = {
    "A100": "shipped, arriving Thursday",
    "A200": "still processing, no ship date yet",
}

# What the agent node asks Gemini to decide, every turn: answer directly,
# call the order-status tool, or flag the turn for a human. Same
# schema-as-contract idea as Module 1's structured extraction, now
# deciding a routing choice instead of filling booking fields.
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
    "status (billing disputes, refunds, anything legal or safety related), "
    "set action to escalate instead of guessing. Only set action to answer "
    "once you have a tool result to answer from, or the request needs no "
    "lookup at all."
)


class AgentState(MessagesState):
    """Studio-compatible conversation history plus the routing fields."""

    order_id: Optional[str]
    route: Optional[str]


def get_order_status(order_id: str) -> str:
    """The real lookup a tool node runs. Mocked here, on purpose: the graph
    shape around a tool call does not depend on the tool being real."""
    return FAKE_ORDERS.get(order_id, f"no order found for '{order_id}'")


def call_model(messages) -> dict:
    """Send the whole state's message history to Gemini and get back a
    structured decision. Identical call to raw_loop.py's call_model, this
    is not a LangGraph-specific idea."""
    transcript = "\n".join(
        f"{message.type}: {message.content}" for message in messages
    )
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=f"system: {SYSTEM_PROMPT}\n{transcript}",
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": DECISION_SCHEMA,
        },
    )
    return json.loads(interaction.output_text)


def agent_node(state: AgentState) -> dict:
    """Calls the model with the full state and returns its decision. This
    is the raw loop's call_model step, wrapped as a graph node that reads
    and returns the explicit state object instead of a bare list."""
    decision = call_model(state["messages"])
    note = AIMessage(content=decision.get("reply") or f"[{decision['action']}]")
    return {
        "messages": [note],
        "order_id": decision.get("order_id") or state.get("order_id"),
        "route": decision["action"],
    }


def tool_node(state: AgentState) -> dict:
    """Runs the real lookup and appends the result, then the conditional
    edge below routes back to the agent node so it can turn that result
    into a reply. Same append-and-loop-back idea as the raw loop, now a
    named step instead of an implicit repeat."""
    result = get_order_status(state.get("order_id") or "")
    return {
        "messages": [
            ToolMessage(content=result, tool_call_id="order_status_lookup")
        ]
    }


def escalate_node(state: AgentState) -> dict:
    """Terminal node: the turn is flagged for a person instead of answered
    automatically. This is the clean failure from slide 9, not a bug."""
    return {
        "messages": [
            AIMessage(content="Escalated to a human. No automatic reply was sent.")
        ]
    }


def route_from_agent(state: AgentState) -> str:
    """The conditional edge's condition function. Reads the state the
    agent node just wrote, decides nothing new itself."""
    return state["route"]


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tool", tool_node)
builder.add_node("escalate", escalate_node)
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    route_from_agent,
    {"call_tool": "tool", "answer": END, "escalate": "escalate"},
)
builder.add_edge("tool", "agent")
builder.add_edge("escalate", END)

graph = builder.compile()

if __name__ == "__main__":
    # A quick check with no Studio and no API key required beyond what
    # call_model needs: confirms the graph compiles and traces one turn.
    result = graph.invoke(
        {
            "messages": [
                {"role": "user", "content": "can you check if order A100 shipped yet?"}
            ],
            "order_id": None,
            "route": None,
        }
    )
    print(json.dumps(result["messages"], indent=2))
