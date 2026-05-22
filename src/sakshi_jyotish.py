#!/usr/bin/env python3
"""
🕉️ SAKSHI JYOTISH -- Liberation-Focused Transit Interpreter
Combines transit calculations with Vedic wisdom for Sakshi Bhava practice.
Uses local knowledge base for interpretations. No cloud. No API.

Architecture:
  Jyotish Transit Engine → Calculates Gochar positions
  Vedic Knowledge Base → Retrieves relevant spiritual teachings
  Sakshi Interpreter → Generates liberation-focused guidance
"""

import ephem
import json
import os
import re
from datetime import datetime, timedelta
from math import degrees
from typing import Dict, List, Optional

# ============================================================
# VEDIC KNOWLEDGE BASE FOR SAKSHI INTERPRETATIONS
# ============================================================
SAKSHI_KNOWLEDGE = {
    # Planet-specific Sakshi practices
    'Sun': {
        'seizure': 'The ego identifies with power, status, and being "right."',
        'sakshi': 'Observe the urge to dominate or seek validation. Ask: "Who is seeking recognition?"',
        'mantra': 'ॐ सूर्याय नमः -- I am not the doer. I am the witness of action.',
        'upanishad': 'The Self is not the body, not the senses, not the mind. -- Kaivalya Upanishad',
        'practice': 'At sunrise, sit silently. Watch the light. Feel it illuminate, not define you.'
    },
    'Moon': {
        'seizure': 'The mind identifies with emotions, moods, and memories.',
        'sakshi': 'Observe feelings arising. They are clouds in the sky of consciousness. You are the sky.',
        'mantra': 'ॐ सोमाय नमः -- I am not the emotion. I am the space in which emotions arise.',
        'upanishad': 'When the mind is still, the Self shines forth. -- Amritabindu Upanishad',
        'practice': 'At night, gaze at the moon. Notice how it reflects light, like the mind reflects consciousness.'
    },
    'Mars': {
        'seizure': 'The life force identifies with anger, competition, and conquest.',
        'sakshi': 'Observe the surge of energy. Channel it, but do not become it. Action without attachment.',
        'mantra': 'ॐ मङ्गलाय नमः -- I am not the warrior. I am the stillness behind the battle.',
        'upanishad': 'Established in non-violence, all hostility ceases in ones presence. -- Yoga Sutras 2.35',
        'practice': 'When anger rises, pause. Three breaths. Watch the fire without fueling it.'
    },
    'Mercury': {
        'seizure': 'The intellect identifies with thoughts, opinions, and being "smart."',
        'sakshi': 'Observe thoughts flowing. They are ripples on consciousness. The thinker is the thought.',
        'mantra': 'ॐ बुधाय नमः -- I am not the thought. I am the awareness between thoughts.',
        'upanishad': 'The mind is the cause of both bondage and liberation. -- Amritabindu Upanishad',
        'practice': 'Watch a thought arise. Do not pursue it. See how it dissolves on its own.'
    },
    'Jupiter': {
        'seizure': 'The wisdom-faculty identifies with knowledge, teaching, and being "righteous."',
        'sakshi': 'True wisdom is not accumulated. It is revealed when the knower dissolves into the known.',
        'mantra': 'ॐ गुरवे नमः -- I am not the teacher. I am the light in which teaching and learning appear.',
        'upanishad': 'When all desires that dwell in the heart are released, the mortal becomes immortal. -- Katha Upanishad',
        'practice': 'Study a scripture. Then close it. Sit. Let the words dissolve into silence.'
    },
    'Venus': {
        'seizure': 'The heart identifies with pleasure, beauty, attachment, and possession.',
        'sakshi': 'Observe desire. Do not suppress it. Do not indulge it. See it as energy seeking its source.',
        'mantra': 'ॐ शुक्राय नमः -- I am not the lover. I am love itself, without object.',
        'upanishad': 'Not for the sake of the beloved is the beloved dear, but for the sake of the Self. -- Brihadaranyaka Upanishad',
        'practice': 'When drawn to beauty, pause. See the beauty in the formless awareness beholding it.'
    },
    'Saturn': {
        'seizure': 'The ego identifies with suffering, limitation, delay, and hardship.',
        'sakshi': 'Pain is inevitable. Suffering is identification with pain. Observe the contraction without becoming it.',
        'mantra': 'ॐ शनैश्चराय नमः -- I am not the sufferer. I am the eternal witness of all experience.',
        'upanishad': 'The Self is untouched by suffering, old age, death, hunger, or thirst. -- Chandogya Upanishad',
        'practice': 'In difficulty, ask: "Who is suffering?" The one who asks is already free.'
    },
    'Rahu': {
        'seizure': 'The mind is seized by illusion, obsession, craving for the new, and digital addiction.',
        'sakshi': 'The shadow is not evil. It is unrecognized light. Integrate, do not fight.',
        'mantra': 'ॐ राहवे नमः -- I am not the craving. I am the fullness that seeks nothing.',
        'upanishad': 'Where one sees nothing else, hears nothing else, knows nothing else -- that is the Infinite. -- Chandogya Upanishad',
        'practice': 'Disconnect from screens for one hour. Notice the restlessness. Stay. It passes.'
    },
    'Ketu': {
        'seizure': 'Consciousness is seized by detachment, isolation, and spiritual bypassing.',
        'sakshi': 'True detachment is not rejection of the world, but freedom within it. Be in the world, not of it.',
        'mantra': 'ॐ केतवे नमः -- I am not the renunciate. I am the wholeness that includes both world and solitude.',
        'upanishad': 'When one realizes the Self, what sorrow, what delusion remains? -- Isha Upanishad',
        'practice': 'Sit alone. Then re-engage with the world. Notice: you were never separate.'
    },
    
    # House-specific Sakshi practices
    'house_1': {'area': 'Self, body, personality', 
                'sakshi': 'The body ages, the personality shifts. Who is the constant observer of these changes?'},
    'house_2': {'area': 'Speech, wealth, family', 
                'sakshi': 'Words arise and dissolve. True wealth is the silence from which speech emerges.'},
    'house_3': {'area': 'Communication, courage, siblings', 
                'sakshi': 'Every conversation is an opportunity to hear the silence between words.'},
    'house_4': {'area': 'Home, mother, inner peace', 
                'sakshi': 'Home is not a place. It is the heart resting in its own nature.'},
    'house_5': {'area': 'Creativity, children, intelligence', 
                'sakshi': 'Creation arises from emptiness. You are that emptiness.'},
    'house_6': {'area': 'Health, service, obstacles', 
                'sakshi': 'Illness teaches detachment. Serve without seeking reward.'},
    'house_7': {'area': 'Relationships, partnerships', 
                'sakshi': 'The other is a mirror. What you see in them is in you.'},
    'house_8': {'area': 'Transformation, secrets, death', 
                'sakshi': 'Death is the greatest teacher. Die to the past each moment.'},
    'house_9': {'area': 'Dharma, wisdom, guru', 
                'sakshi': 'The outer guru points to the inner. You are your own ultimate teacher.'},
    'house_10': {'area': 'Career, status, karma', 
                'sakshi': 'Work is worship when done without attachment to results.'},
    'house_11': {'area': 'Gains, community, aspirations', 
                'sakshi': 'True gain is knowing nothing can be added to or subtracted from the Self.'},
    'house_12': {'area': 'Loss, liberation, solitude', 
                'sakshi': 'The deepest loss reveals what can never be lost -- your true nature.'},
    
    # Aspect-specific wisdom
    'Conjunction': 'Union of energies. Both planets merge their lessons. Deep integration possible.',
    'Full Aspect': 'Intense engagement. The lesson is direct. Meet it fully, then release.',
    'Trine': 'Graceful flow. Spiritual support. Use this ease to deepen practice.',
    'Angular': 'Outer manifestation. The inner work shows up in life circumstances.',
    'Dusthana': 'Purification. Friction burns karma. These houses are the fastest path to liberation.',
    'Neutral': 'Quiet period. Consolidate. The silence between storms.',
    
    # Universal Sakshi teachings
    'root': {
        'essence': 'You are not the chart. You are the one who reads it. Planets move. Consciousness is unmoving.',
        'maha_vakya': 'Tat Tvam Asi -- That Thou Art. The planets are "that." You are the witness of "that."',
        'final_teaching': 'The one who seeks liberation is already free. The seeking itself is the last veil. Let it fall.'
    }
}


class SakshiJyotish:
    """Liberation-focused Jyotish interpreter with Sakshi Bhava teachings."""
    
    def __init__(self, birth_date="1993-12-24", birth_time="05:40", lat=24.83, lon=92.80):
        self.engine = JyotishTransit(birth_date, birth_time, lat, lon)
        self.transits = self.engine.compare_transit()
        self.knowledge = SAKSHI_KNOWLEDGE
    
    def get_sakshi_interpretation(self, transit):
        """Generate Sakshi-focused interpretation for a transit."""
        graha = transit['graha']
        house = transit['house_from_natal']
        aspect_type = transit['aspect'].split(' ')[0]  # Get base aspect type
        intensity = transit['intensity']
        
        # Get planet wisdom
        planet_wisdom = self.knowledge.get(graha, {})
        house_wisdom = self.knowledge.get(f'house_{house}', {})
        aspect_wisdom = self.knowledge.get(aspect_type, '')
        
        return {
            'graha': graha,
            'sanskrit': transit['sanskrit'],
            'house': house,
            'house_area': house_wisdom.get('area', ''),
            'transit_pattern': f"{graha} in house {house} ({aspect_type})",
            'seizure': planet_wisdom.get('seizure', 'The ego identifies with the energy of this planet.'),
            'sakshi_practice': planet_wisdom.get('sakshi', 'Observe the pattern without identification.'),
            'house_teaching': house_wisdom.get('sakshi', ''),
            'aspect_teaching': aspect_wisdom,
            'mantra': planet_wisdom.get('mantra', ''),
            'upanishad': planet_wisdom.get('upanishad', ''),
            'daily_practice': planet_wisdom.get('practice', ''),
            'intensity': intensity,
            'liberation_message': self._get_liberation_message(intensity, graha)
        }
    
    def _get_liberation_message(self, intensity, graha):
        """Generate liberation-focused message based on intensity."""
        if intensity == 'Challenging':
            return f"This {graha} transit is a fast path to liberation. The friction burns karma rapidly. Stay present."
        elif intensity == 'High':
            return f"Strong {graha} energy. The intensity is an invitation to deepen Sakshi Bhava."
        elif intensity in ['Benefic', 'Strong']:
            return f"Graceful {graha} transit. Use this ease to stabilize in the witness."
        else:
            return f"Quiet {graha} period. The silence between lessons. Rest in awareness."
    
    def generate_report(self):
        """Generate complete Sakshi Jyotish report."""
        print("╔══════════════════════════════════════════════════════╗")
        print("║  🕉️ SAKSHI JYOTISH -- Liberation Transit Report      ║")
        print("║  Not to predict, but to transcend                 ║")
        print("╚══════════════════════════════════════════════════════╝\n")
        
        # Root teaching
        root = self.knowledge['root']
        print("🌟 ROOT TEACHING")
        print("═" * 55)
        print(f"{root['essence']}\n")
        print(f"📿 {root['maha_vakya']}")
        print(f"🕉️ {root['final_teaching']}\n")
        
        # Individual transits
        print("🌙 CURRENT TRANSITS & SAKSHI PRACTICES")
        print("═" * 55)
        
        for transit in self.transits:
            interp = self.get_sakshi_interpretation(transit)
            
            # Symbol based on intensity
            symbol = {'Challenging': '⚠️', 'High': '🔥', 'Benefic': '✅', 'Strong': '✅',
                     'Moderate': '➖', 'Low': '💤'}.get(interp['intensity'], '➖')
            
            print(f"\n{symbol} {interp['graha']} ({interp['sanskrit']}) -- House {interp['house']}")
            print(f"   Natal: {transit['natal_rashi']} → Current: {transit['current_rashi']} | {transit['nakshatra']}")
            print(f"   Area: {interp['house_area']}")
            print(f"   Pattern: {interp['transit_pattern']}")
            print(f"\n   ⛓️ Seizure: {interp['seizure']}")
            print(f"   👁️ Sakshi: {interp['sakshi_practice']}")
            print(f"   🏠 House Teaching: {interp['house_teaching']}")
            print(f"   📿 Mantra: {interp['mantra']}")
            print(f"   📖 Upanishad: {interp['upanishad']}")
            print(f"   🧘 Practice: {interp['daily_practice']}")
            print(f"   🕉️ Message: {interp['liberation_message']}")
        
        # Summary
        print(f"\n{'═' * 55}")
        print("📊 SAKSHI SUMMARY")
        print("═" * 55)
        
        high_friction = [t for t in self.transits if t['intensity'] in ['High', 'Challenging']]
        benefic = [t for t in self.transits if t['intensity'] in ['Benefic', 'Strong']]
        
        if high_friction:
            print(f"\n🔥 High Friction Transits ({len(high_friction)}): Fast paths to liberation")
            for t in high_friction:
                interp = self.get_sakshi_interpretation(t)
                print(f"   • {t['graha']} in {t['house_from_natal']}H -- {interp['seizure'][:60]}...")
        
        if benefic:
            print(f"\n✅ Benefic Transits ({len(benefic)}): Grace for practice")
            for t in benefic:
                print(f"   • {t['graha']} in {t['house_from_natal']}H -- Use this ease to deepen.")
        
        print(f"\n🕉️ FINAL SAKSHI REMINDER:")
        print(f"   The planets do not bind you. They reveal where you already bind yourself.")
        print(f"   The chart is a mirror. The witness of the mirror is free.")
        print(f"   ॐ तत् सत् -- That alone is real.\n")
    
    def to_json(self):
        """Export as JSON with Sakshi interpretations."""
        return json.dumps([
            self.get_sakshi_interpretation(t) for t in self.transits
        ], indent=2, default=str)


# ============================================================
# REUSE JYOTISH TRANSIT ENGINE (imported or embedded)
# ============================================================
# Minimal embedded version to avoid import issues
class JyotishTransit:
    """Embedded transit calculator -- no external dependencies beyond ephem."""
    
    GRAHA_MAP = {
        'Sun': {'sanskrit': 'Surya'}, 'Moon': {'sanskrit': 'Chandra'},
        'Mars': {'sanskrit': 'Mangal'}, 'Mercury': {'sanskrit': 'Budha'},
        'Jupiter': {'sanskrit': 'Guru'}, 'Venus': {'sanskrit': 'Shukra'},
        'Saturn': {'sanskrit': 'Shani'}, 'Rahu': {'sanskrit': 'Rahu'}, 'Ketu': {'sanskrit': 'Ketu'},
    }
    
    RASHI_LIST = [
        'Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya',
        'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena'
    ]
    
    NAKSHATRA_LIST = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
        'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    def __init__(self, birth_date, birth_time, lat, lon):
        dt_str = f"{birth_date} {birth_time}"
        self.birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        self.observer = ephem.Observer()
        self.observer.lat = str(lat)
        self.observer.lon = str(lon)
        self.natal = self._calculate_positions(self.birth_dt)
    
    def _calculate_positions(self, dt):
        self.observer.date = ephem.Date(dt)
        positions = {}
        sidereal_time = float(self.observer.sidereal_time())
        lagna_deg = (sidereal_time * 15 + float(self.observer.lon)) % 360
        positions['Lagna'] = {'ra': lagna_deg, 'rashi': int(lagna_deg / 30),
                               'rashi_name': self.RASHI_LIST[int(lagna_deg / 30)], 'degree': lagna_deg % 30}
        
        planet_map = {'Sun': ephem.Sun(), 'Moon': ephem.Moon(), 'Mars': ephem.Mars(),
                     'Mercury': ephem.Mercury(), 'Jupiter': ephem.Jupiter(),
                     'Venus': ephem.Venus(), 'Saturn': ephem.Saturn()}
        
        for name, planet in planet_map.items():
            planet.compute(self.observer)
            ra_deg = degrees(float(planet.ra))
            rashi = int(ra_deg / 30)
            positions[name] = {'ra': ra_deg, 'rashi': rashi,
                              'rashi_name': self.RASHI_LIST[rashi], 'degree': ra_deg % 30,
                              'retrograde': getattr(planet, 'retrograde', False)}
        return positions
    
    def get_current_transit(self):
        now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        return self._calculate_positions(now)
    
    def _get_nakshatra(self, ra_deg):
        span = 360 / 27
        idx = int(ra_deg / span) % 27
        pada = int((ra_deg % span) / (span / 4)) + 1
        return {'name': self.NAKSHATRA_LIST[idx], 'pada': pada}
    
    def _vedic_aspects(self, planet, house):
        full = {'Sun': [7], 'Moon': [7], 'Mars': [4, 7, 8], 'Mercury': [7],
                'Jupiter': [5, 7, 9], 'Venus': [7], 'Saturn': [3, 7, 10]}
        aspects = full.get(planet, [7])
        if house == 1: return {'type': 'Conjunction (Yuti)', 'intensity': 'Strong'}
        elif house in aspects: return {'type': 'Full Aspect (Drishti)', 'intensity': 'High'}
        elif house in [5, 9]: return {'type': 'Trine Aspect (Trikona)', 'intensity': 'Benefic'}
        elif house in [1, 4, 7, 10]: return {'type': 'Angular (Kendra)', 'intensity': 'Moderate'}
        elif house in [6, 8, 12]: return {'type': 'Dusthana (Difficult)', 'intensity': 'Challenging'}
        else: return {'type': 'Neutral', 'intensity': 'Low'}
    
    def compare_transit(self):
        current = self.get_current_transit()
        report = []
        for name, natal_pos in self.natal.items():
            if name == 'Lagna': continue
            cur_pos = current.get(name)
            if not cur_pos: continue
            house = ((cur_pos['rashi'] - natal_pos['rashi']) % 12) + 1
            aspects = self._vedic_aspects(name, house)
            report.append({
                'graha': name,
                'sanskrit': self.GRAHA_MAP.get(name, {}).get('sanskrit', name),
                'natal_rashi': natal_pos['rashi_name'],
                'current_rashi': cur_pos['rashi_name'],
                'house_from_natal': house,
                'aspect': aspects['type'],
                'intensity': aspects['intensity'],
                'nakshatra': self._get_nakshatra(cur_pos['ra'])['name'],
                'retrograde': cur_pos.get('retrograde', False)
            })
        return report


if __name__ == "__main__":
    import sys
    
    birth_date = "1993-12-24"
    birth_time = "05:40"
    lat, lon = 24.83, 92.80
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--birth' and i+1 < len(args):
            parts = args[i+1].split()
            birth_date = parts[0]
            birth_time = parts[1] if len(parts) > 1 else "05:40"
            i += 2
        elif args[i] == '--json':
            sakshi = SakshiJyotish(birth_date, birth_time, lat, lon)
            print(sakshi.to_json())
            sys.exit(0)
        else:
            i += 1
    
    sakshi = SakshiJyotish(birth_date, birth_time, lat, lon)
    sakshi.generate_report()
