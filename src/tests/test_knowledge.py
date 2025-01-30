from src.knowledge.knowledge_base import KnowledgeBase

def test_knowledge_base():
    kb = KnowledgeBase()
    assert kb.query("Test question") is not None