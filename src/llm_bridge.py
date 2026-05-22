import json, os, subprocess, sys

# Knowledge base path (already verified)
ASI_PATH = os.path.expanduser("~/Divine-Earthly-ASI")
KB_PATH = os.path.join(ASI_PATH, "data", "unified_knowledge.json")
# Quantized SLM wrapper path
SLM_WRAPPER = os.path.join(ASI_PATH, "quantized_slm_wrapper.py")

def query_knowledge_base(question):
    if not os.path.exists(KB_PATH): return None
    with open(KB_PATH) as f: kb = json.load(f)
    q = question.lower().rstrip('?.')
    if q in kb: return kb[q]
    # partial matching ...
    return None

def query_quantized_slm(prompt):
    if not os.path.exists(SLM_WRAPPER): return None
    try:
        result = subprocess.run(["python3", SLM_WRAPPER],
                                input=prompt, capture_output=True, text=True, timeout=10)
        # Extract the actual response line
        for line in result.stdout.split('\n'):
            if line.startswith("Response: "):
                return line.split("Response: ",1)[1].strip()
    except: pass
    return None

def get_enhanced_sakshi(graha, house, intensity):
    # Try quantized SLM first (if available)
    prompt = f"How should one practice Sakshi Bhava with {graha} transiting house {house}?"
    slm = query_quantized_slm(prompt)
    if slm and len(slm)>20:
        return {'source':'quantized_slm', 'combined': slm[:300]}
    # Fallback to knowledge base
    kb = query_knowledge_base(f"spiritual significance of {graha}")
    if kb: return {'source':'knowledge_base', 'combined': kb[:300]}
    # Final fallback
    return {'source':'builtin', 'combined': f"Observe {graha} energy in house {house} with detachment."}

if __name__ == "__main__":
    print("Testing updated bridge...")
    g = get_enhanced_sakshi("Venus",8,"Challenging")
    print(f"Source: {g['source']} -> {g['combined'][:100]}...")
