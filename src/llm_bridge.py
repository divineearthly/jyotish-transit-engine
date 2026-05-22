#!/usr/bin/env python3
"""
Bridge: Sakshi Jyotish ↔ Divine Earthly ASI SLM
Your Vedic inference engine is at ~/Divine-Earthly-ASI/vedic_inference_engine
"""

import subprocess, json, os

ASI_PATH = os.path.expanduser("~/Divine-Earthly-ASI")
LLM_ENGINE = os.path.join(ASI_PATH, "vedic_inference_engine")  # Root, not engines/
KNOWLEDGE_FILE = os.path.join(ASI_PATH, "unified_knowledge.json")

def query_vedic_slm(prompt):
    """Send query to your working Vedic SLM."""
    if not os.path.exists(LLM_ENGINE):
        return None
    try:
        result = subprocess.run(
            [LLM_ENGINE],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=ASI_PATH
        )
        # Extract the actual answer from the verbose output
        output = result.stdout
        # Look for the knowledge query answer pattern
        if "VEDIC KNOWLEDGE QUERY:" in output:
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if "A:" in line and i > 0:
                    return line.split("A:", 1)[1].strip()
        return output.strip()[:300] if output else None
    except:
        return None

def query_knowledge_base(question):
    """Query the 1,990-entry Vedic knowledge base."""
    if not os.path.exists(KNOWLEDGE_FILE):
        return None
    try:
        with open(KNOWLEDGE_FILE, 'r') as f:
            kb = json.load(f)
        q = question.lower().strip().rstrip('?.')
        if q in kb:
            return kb[q]
        q_words = set(w for w in q.split() if len(w) > 2)
        best_score, best_answer = 0, None
        for key, val in kb.items():
            k_words = set(w for w in key.split() if len(w) > 2)
            if not k_words: continue
            score = len(q_words & k_words) / len(q_words | k_words)
            if score > best_score:
                best_score = score
                best_answer = val
        return best_answer if best_score > 0.2 else None
    except:
        return None

def get_enhanced_sakshi(graha, house, intensity):
    """Get Sakshi guidance combining SLM + Knowledge Base."""
    prompt = f"What is the spiritual teaching of {graha} transiting house {house} for Sakshi Bhava practice?"
    
    slm_answer = query_vedic_slm(prompt)
    kb_answer = query_knowledge_base(f"what is {graha}")
    
    return {
        'slm_response': slm_answer,
        'knowledge_base': kb_answer[:200] if kb_answer else None,
        'combined': slm_answer or kb_answer or "Meditate on the witness consciousness."
    }

if __name__ == "__main__":
    print("Testing SLM Bridge...")
    
    # Test SLM
    slm = query_vedic_slm("What is Sakshi Bhava?")
    print(f"SLM: {'✅ Responding' if slm else '❌ Not responding'}")
    if slm:
        print(f"   Response: {slm[:150]}...")
    
    # Test knowledge base
    kb = query_knowledge_base("what is brahman")
    print(f"KB:  {'✅ Connected' if kb else '❌ Not found'} ({len(kb) if kb else 0} chars)")
    
    # Test combined
    guidance = get_enhanced_sakshi("Saturn", 3, "High")
    print(f"\n🕉️ Enhanced Sakshi Guidance:")
    print(f"   {guidance['combined'][:200]}...")
