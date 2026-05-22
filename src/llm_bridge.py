#!/usr/bin/env python3
"""
Bridge: Sakshi Jyotish ↔ Divine Earthly ASI Knowledge Base
Uses your 1,990-entry Vedic knowledge base for enhanced guidance.
(SLM demo always returns fixed output; KB gives specific answers.)
"""

import json, os

ASI_PATH = os.path.expanduser("~/Divine-Earthly-ASI")
KNOWLEDGE_FILE = os.path.join(ASI_PATH, "data", "unified_knowledge.json")

def query_knowledge_base(question):
    """Query the Vedic knowledge base with partial matching."""
    if not os.path.exists(KNOWLEDGE_FILE):
        return None
    with open(KNOWLEDGE_FILE, 'r') as f:
        kb = json.load(f)
    q = question.lower().strip().rstrip('?.')
    if q in kb:
        return kb[q]
    q_words = set(w for w in q.split() if len(w) > 2)
    if not q_words:
        return None
    best_score, best_answer = 0, None
    for key, val in kb.items():
        k_words = set(w for w in key.split() if len(w) > 2)
        if not k_words: continue
        score = len(q_words & k_words) / len(q_words | k_words)
        if score > best_score:
            best_score = score
            best_answer = val
    return best_answer if best_score > 0.2 else None

def get_enhanced_sakshi(graha, house, intensity):
    """Get enhanced guidance using knowledge base lookups."""
    queries = [
        f"spiritual significance of {graha}",
        f"{graha} vedic astrology house {house}",
        f"what is {graha} in vedic philosophy"
    ]
    for q in queries:
        answer = query_knowledge_base(q)
        if answer and len(answer) > 20:
            return {
                'slm_response': None,
                'knowledge_base': answer[:300],
                'combined': f"[Vedic Knowledge]: {answer[:300]}"
            }
    # Fallback to built-in Sakshi wisdom
    return {
        'slm_response': None,
        'knowledge_base': None,
        'combined': f"For {graha} in house {house}: Observe the {graha} energy without identification. Rest in the witness."
    }

if __name__ == "__main__":
    print("Testing Knowledge Base Bridge...")
    print(f"KB: {'✅ Found' if os.path.exists(KNOWLEDGE_FILE) else '❌ Missing'}")
    g = get_enhanced_sakshi("Venus", 8, "Challenging")
    print(f"Guidance: {g['combined'][:200]}...")
