#!/usr/bin/env python3
"""Bridge between Sakshi Jyotish and Divine Earthly ASI LLM."""
import subprocess, json

def query_vedic_llm(prompt):
    """Send query to your existing Vedic LLM engine."""
    try:
        result = subprocess.run(
            ['../Divine-Earthly-ASI/engines/vedic_inference_engine'],
            input=prompt, capture_output=True, text=True, timeout=5
        )
        return result.stdout
    except:
        return None

# Example: Get LLM-enhanced Sakshi interpretation
prompt = "Given Saturn transiting 3rd house, provide Sakshi Bhava guidance for liberation."
print(query_vedic_llm(prompt))
