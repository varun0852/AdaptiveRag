import yaml
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from src.models.state import GraphState
from src.llms.groq import llm
from src.rag.retriever_setup import retriever
from src.config.settings import TAVILY_API_KEY
from src.core.logger import get_logger

logger = get_logger(__name__)

# Load prompts
with open("src/config/prompts.yaml", "r") as f:
    prompts = yaml.safe_load(f)

# Tavily web search
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY or ""
web_search_tool = TavilySearchResults(max_results=3)


def classify_query(state: GraphState) -> GraphState:
    query = state["query"]
    prompt = prompts["classify_prompt"] + f"\n\nQuestion: {query}"
    response = llm.invoke(prompt)
    route = response.content.strip().lower()
    if route not in ["index", "general", "search"]:
        route = "general"
    logger.info(f"Classified as: {route}")
    return {**state, "route": route}


def retrieve(state: GraphState) -> GraphState:
    query = state["query"]
    docs = retriever.invoke(query)
    doc_texts = [doc.page_content for doc in docs]
    logger.info(f"Retrieved {len(doc_texts)} documents.")
    return {**state, "documents": doc_texts}


def grade_documents(state: GraphState) -> GraphState:
    query = state["query"]
    documents = state.get("documents", [])
    relevant = []
    for doc in documents:
        prompt = prompts["grading_prompt"] + f"\n\nQuestion: {query}\nDocument: {doc}"
        response = llm.invoke(prompt)
        if "yes" in response.content.strip().lower():
            relevant.append(doc)
    logger.info(f"{len(relevant)}/{len(documents)} documents relevant.")
    return {**state, "documents": relevant}


def rewrite_query(state: GraphState) -> GraphState:
    query = state["query"]
    prompt = prompts["rewrite_prompt"] + f"\n\nOriginal question: {query}"
    response = llm.invoke(prompt)
    new_query = response.content.strip()
    count = state.get("rewrite_count", 0) + 1
    logger.info(f"Rewritten query (attempt {count}): {new_query}")
    return {**state, "query": new_query, "rewrite_count": count}


def generate(state: GraphState) -> GraphState:
    query = state["query"]
    documents = state.get("documents", [])
    context = "\n\n".join(documents) if documents else "No context available."
    prompt = prompts["generate_prompt"].format(
        context=context,
        question=query
    )
    response = llm.invoke(prompt)
    return {**state, "answer": response.content.strip()}


def web_search(state: GraphState) -> GraphState:
    query = state["query"]
    results = web_search_tool.invoke(query)
    doc_texts = [r["content"] for r in results if "content" in r]
    logger.info(f"Web search returned {len(doc_texts)} results.")
    return {**state, "documents": doc_texts}


def general_llm(state: GraphState) -> GraphState:
    query = state["query"]
    response = llm.invoke(query)
    return {**state, "answer": response.content.strip()}


def route_query(state: GraphState) -> str:
    return state.get("route", "general")


def decide_to_rewrite(state: GraphState) -> str:
    documents = state.get("documents", [])
    rewrite_count = state.get("rewrite_count", 0)
    if not documents and rewrite_count < 2:
        return "rewrite"
    return "generate"