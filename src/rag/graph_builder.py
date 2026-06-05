from langgraph.graph import StateGraph, END
from src.models.state import GraphState
from src.rag.nodes import (
    classify_query, retrieve, grade_documents,
    rewrite_query, generate, web_search,
    general_llm, route_query, decide_to_rewrite,
)


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("classify", classify_query)
    graph.add_node("retrieve", retrieve)
    graph.add_node("grade", grade_documents)
    graph.add_node("rewrite", rewrite_query)
    graph.add_node("generate", generate)
    graph.add_node("web_search", web_search)
    graph.add_node("general_llm", general_llm)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_query,
        {
            "index": "retrieve",
            "general": "general_llm",
            "search": "web_search",
        }
    )

    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        decide_to_rewrite,
        {
            "rewrite": "rewrite",
            "generate": "generate",
        }
    )

    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("web_search", "generate")
    graph.add_edge("generate", END)
    graph.add_edge("general_llm", END)

    return graph.compile()


rag_graph = build_graph()
