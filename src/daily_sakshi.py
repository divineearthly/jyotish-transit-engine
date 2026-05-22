#!/usr/bin/env python3
"""
🕉️ Daily Sakshi Reminder — Morning Practice Generator
Based on current transits, generates your daily witness-consciousness practice.
Now with SLM-enhanced deep guidance from your Vedic inference engine.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from sakshi_jyotish import SakshiJyotish

def generate_daily_practice(birth_date="1993-12-24", birth_time="05:40", lat=24.83, lon=92.80):
    sakshi = SakshiJyotish(birth_date, birth_time, lat, lon)
    interps = [sakshi.get_sakshi_interpretation(t) for t in sakshi.transits]
    
    priority = {'Challenging': 4, 'High': 3, 'Benefic': 2, 'Strong': 2, 'Moderate': 1, 'Low': 0}
    interps.sort(key=lambda x: priority.get(x['intensity'], 0), reverse=True)
    
    today = datetime.now().strftime("%A, %d %B %Y")
    
    print("╔══════════════════════════════════════════════════════╗")
    print(f"║  🕉️ DAILY SAKSHI PRACTICE — {today} ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    print("\n🌅 MORNING INVOCATION")
    print("═" * 50)
    print("Sit silently. Three deep breaths.")
    print("Ask: 'Who is aware of this breath?'")
    print("Rest in the awareness, not the breath.\n")
    
    primary = interps[0]
    print(f"🔥 TODAY'S PRIMARY PRACTICE: {primary['graha']} ({primary['sanskrit']})")
    print("═" * 50)
    print(f"Transit: {primary['graha']} in House {primary['house']} — {primary['intensity']}")
    print(f"\nSeizure pattern: {primary['seizure']}")
    print(f"\n👁️ Sakshi Practice:")
    print(f"   {primary['sakshi_practice']}")
    print(f"\n📿 Mantra for today:")
    print(f"   {primary['mantra']}")
    print(f"\n🧘 Concrete practice:")
    print(f"   {primary['daily_practice']}")
    
    if len(interps) > 1:
        secondary = interps[1]
        print(f"\n\n🌟 SECONDARY SUPPORT: {secondary['graha']} ({secondary['sanskrit']})")
        print("═" * 50)
        print(f"Practice: {secondary['daily_practice']}")
    
    print(f"\n\n🌙 EVENING REFLECTION")
    print("═" * 50)
    print("Before sleep, ask three questions:")
    print("1. Where did I identify with thoughts/emotions today?")
    print("2. Where did I remember to witness?")
    print("3. Who is asking these questions?")
    
    # SLM-ENHANCED DEEP GUIDANCE
    try:
        from llm_bridge import get_enhanced_sakshi
        enhanced = get_enhanced_sakshi(primary['graha'], primary['house'], primary['intensity'])
        if enhanced and enhanced.get('combined'):
            print(f"\n\n🧠 SLM-ENHANCED DEEP GUIDANCE")
            print("═" * 50)
            print(enhanced['combined'][:400])
    except Exception:
        pass  # SLM not available, gracefully skip
    
    print(f"\n\n🕉️ SAKSHI REMINDER")
    print("═" * 50)
    print(f"{sakshi.knowledge['root']['essence']}")
    print(f"\n📖 {sakshi.knowledge['root']['maha_vakya']}")
    
    return {
        'date': today,
        'primary_graha': primary['graha'],
        'primary_practice': primary['sakshi_practice'],
        'primary_mantra': primary['mantra'],
        'secondary_graha': interps[1]['graha'] if len(interps) > 1 else None
    }

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    birth_date = "1993-12-24"
    birth_time = "05:40"
    lat, lon = 24.83, 92.80
    
    i = 0
    while i < len(args):
        if args[i] == '--birth' and i+1 < len(args):
            parts = args[i+1].split()
            birth_date = parts[0]
            birth_time = parts[1] if len(parts) > 1 else "05:40"
            i += 2
        elif args[i] == '--json':
            import json
            print(json.dumps(generate_daily_practice(birth_date, birth_time, lat, lon), indent=2))
            sys.exit(0)
        else:
            i += 1
    
    generate_daily_practice(birth_date, birth_time, lat, lon)
