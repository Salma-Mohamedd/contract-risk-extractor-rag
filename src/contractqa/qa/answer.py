from typing import List, Tuple
from contractqa.config import settings
from contractqa.indexing.vectorstore import get_vectorstore
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def answer_question(question: str, history: List[Tuple[str, str]] | None = None) -> str:
    history = history or []
    vs = get_vectorstore()

    results = vs.similarity_search_with_relevance_scores(question, k=settings.top_k)
    if not results or results[0][1] < settings.min_relevance:
        return (
            "I couldn’t find strong support for that question in the uploaded contract.\n\n"
            "Try rephrasing or ask about a specific topic (termination, liability, payment, notice period)."
        )

    context_blocks = []
    for i, (doc, _score) in enumerate(results, start=1):
        src = doc.metadata.get("source", "?")
        page = doc.metadata.get("page", "?")
        context_blocks.append(f"[S{i}] {src} p.{page}\n{doc.page_content}")

    trimmed = history[-4:]
    history_text = "\n".join([f"User: {u}\nAssistant: {a}" for u, a in trimmed]).strip()

    system = (
        "You are a contract Q&A assistant.\n"
        "Use ONLY the provided context.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Add citations like [S1], [S2] after the sentences you used.\n"
        "Not legal advice."
    )

    user = (
        f"Conversation so far:\n{history_text}\n\n"
        f"Context:\n\n{chr(10).join(context_blocks)}\n\n"
        f"Question: {question}\n"
        "Answer clearly and concisely, with citations."
    )

    llm = ChatOpenAI(model=settings.openai_chat_model, temperature=settings.temperature)
    resp = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return resp.content