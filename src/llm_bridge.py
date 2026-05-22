import subprocess, os

ASI = os.path.expanduser("~/Divine-Earthly-ASI")
MODEL = os.path.join(ASI, "vedic_trained.vedic")

def query_vedic_model(prompt):
    if not os.path.exists(MODEL):
        return None
    try:
        r = subprocess.run(["./vedic_inference_engine", MODEL],
                           input=prompt, capture_output=True, text=True, timeout=10)
        for line in r.stdout.split('\n'):
            if line.startswith("A:"):
                return line[2:].strip()
    except:
        return None
    return None

def get_enhanced_sakshi(graha, house, intensity):
    prompt = f"spiritual lesson of {graha} transiting house {house}"
    wisdom = query_vedic_model(prompt)
    if wisdom:
        return {'source': 'vedic_trained_model', 'combined': wisdom[:600]}
    return {'source': 'builtin', 'combined': f"Observe {graha} energy in house {house}. The witness is free."}
