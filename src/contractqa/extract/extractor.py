import re
from contractqa.config import settings
from contractqa.indexing.vectorstore import get_vectorstore

OBLIGATIONS_QUERY = "must shall required obligation responsibilities"
DEADLINES_QUERY   = "deadline due date no later than within days notice period term"
PENALTIES_QUERY   = "penalty fee liquidated damages liability indemnify breach terminate"

_OBLIGATION_KW = ("shall", "must", "required", "obligated", "responsible", "agree to")
_DEADLINE_KW = ("within", "no later than", "deadline", "due", "effective date", "term", "notice")
_PENALTY_KW = ("penalty", "liquidated", "damages", "liable", "liability", "indemn", "terminate", "breach", "fee")


def _sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return re.split(r"(?<=[\.\!\?])\s+", text)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _make_item(sentence: str, meta: dict) -> dict:
    return {
        "text": sentence.strip(),
        "citation": {"source": meta.get("source", "?"), "page": meta.get("page", "?")},
    }


def _retrieve(query: str):
    vs = get_vectorstore()
    results = vs.similarity_search_with_relevance_scores(query, k=settings.top_k)
    if not results:
        return []
    if results[0][1] < settings.min_relevance:
        return []
    return results


def extract_key_items() -> dict:
    obligations, deadlines, penalties = [], [], []
    seen_o, seen_d, seen_p = set(), set(), set()

    for doc, _score in _retrieve(OBLIGATIONS_QUERY):
        for s in _sentences(doc.page_content):
            if any(k in s.lower() for k in _OBLIGATION_KW):
                key = _norm(s)
                if key not in seen_o:
                    obligations.append(_make_item(s, doc.metadata))
                    seen_o.add(key)

    for doc, _score in _retrieve(DEADLINES_QUERY):
        for s in _sentences(doc.page_content):
            low = s.lower()
            has_date = bool(re.search(r"\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{4}[/\-]\d{1,2}[/\-]\d{1,2})\b", s))
            has_time_phrase = any(k in low for k in _DEADLINE_KW)
            if has_date or has_time_phrase:
                key = _norm(s)
                if key not in seen_d:
                    deadlines.append(_make_item(s, doc.metadata))
                    seen_d.add(key)

    for doc, _score in _retrieve(PENALTIES_QUERY):
        for s in _sentences(doc.page_content):
            if any(k in s.lower() for k in _PENALTY_KW):
                key = _norm(s)
                if key not in seen_p:
                    penalties.append(_make_item(s, doc.metadata))
                    seen_p.add(key)

    return {
        "obligations": obligations[:12],
        "deadlines": deadlines[:12],
        "penalties_liability": penalties[:12],
        "guardrail": {
            "min_relevance": settings.min_relevance,
            "top_k": settings.top_k,
            "note": "If similarity is weak, extraction returns fewer/no items instead of guessing.",
        },
    }