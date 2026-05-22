import subprocess, os, json

ASI = os.path.expanduser("~/Divine-Earthly-ASI")
KB = os.path.join(ASI, "data", "unified_knowledge.json")
GEN = os.path.join(ASI, "generate_quantized.py")
MODEL = os.path.join(ASI, "vedic_tiny_quantized.vedic")

def query_light(prompt):
    if not os.path.exists(GEN):
        return None
    try:
        r = subprocess.run(["python3", GEN, MODEL], input=prompt,
                           capture_output=True, text=True, timeout=15)
        for line in r.stdout.split('\n'):
            if line.startswith("A:"):
                return line[2:].strip()
    except:
        return None

def query_kb(q):
    if not os.path.exists(KB): return None
    with open(KB) as f: kb = json.load(f)
    q = q.lower().rstrip('?.')
    if q in kb: return kb[q]
    return None

def get_enhanced_sakshi(graha, house, intensity):
    # Try lightweight quantized generator
    ans = query_light(f"Sakshi Bhava for {graha} in house {house}")
    if ans and len(ans)>15:
        return {'source':'quantized_gen', 'combined': ans[:300]}
    # Fallback to knowledge base
    kb = query_kb(f"spiritual significance of {graha}")
    if kb:
        return {'source':'knowledge_base', 'combined': kb[:300]}
    return {'source':'builtin', 'combined': f"Observe {graha} energy in house {house}. The witness is free."}
