from typing import TypedDict

from langgraph.graph import StateGraph

from shelf_agent import analyze_shelf
from queue_agent import analyze_queue
from layout_agent import analyze_layout
from promotion_agent import analyze_promotions


class AgentState(TypedDict):

    shelf: str

    queue: str

    layout: str

    promotion: str


# ====================================
# AGENT NODES
# ====================================

def shelf_node(state):

    state["shelf"] = analyze_shelf()

    return state


def queue_node(state):

    state["queue"] = analyze_queue()

    return state


def layout_node(state):

    state["layout"] = analyze_layout()

    return state


def promotion_node(state):

    state["promotion"] = analyze_promotions()

    return state


# ====================================
# GRAPH
# ====================================

builder = StateGraph(
    AgentState
)

builder.add_node(
    "Shelf Agent",
    shelf_node
)

builder.add_node(
    "Queue Agent",
    queue_node
)

builder.add_node(
    "Layout Agent",
    layout_node
)

builder.add_node(
    "Promotion Agent",
    promotion_node
)

builder.set_entry_point(
    "Shelf Agent"
)

builder.add_edge(
    "Shelf Agent",
    "Queue Agent"
)

builder.add_edge(
    "Queue Agent",
    "Layout Agent"
)

builder.add_edge(
    "Layout Agent",
    "Promotion Agent"
)

builder.set_finish_point(
    "Promotion Agent"
)

graph = builder.compile()


# ====================================
# RUN
# ====================================

if __name__ == "__main__":

    result = graph.invoke(
        {}
    )

    print(result)