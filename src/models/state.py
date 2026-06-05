from typing import List, Optional
from typing_extensions import TypedDict


class GraphState(TypedDict):
    query: str
    session_id: str
    route: Optional[str]       # index / general / search
    documents: Optional[List[str]]
    answer: Optional[str]
    rewrite_count: int         # stops infinite rewrite loops
    