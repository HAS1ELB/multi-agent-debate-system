from src.knowledge.knowledge_base import KnowledgeBase

def test_knowledge_base():
    kb = KnowledgeBase()
    result = kb.query("What is AI?")
    assert result is not None, "Query result should not be None"
    assert "Answer" in result, "Expected answer format"