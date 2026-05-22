#!/usr/bin/env python3
"""
🕉️ JYOTISH TRANSIT ENGINE — Gochar (Planetary Transit) Calculator
Surya Siddhanta mathematics via ephem. Offline-first. ARM64 native.

Author: Joydeep Das
Location: Silchar, Assam, India 🇮🇳
License: MIT
"""

import ephem
import json
from datetime import datetime, timedelta
from math import degrees
from typing import Dict, List, Optional, Tuple

# ============================================================
# VEDIC CONSTANTS
# ============================================================
GRAHA_MAP = {
    'Sun':       {'sanskrit': 'Surya',    'significance': 'Atman, Self, Authority, Father, Health'},
    'Moon':      {'sanskrit': 'Chandra',  'significance': 'Manas, Mind, Emotions, Mother, Public'},
    'Mars':      {'sanskrit': 'Mangal',   'significance': 'Energy, Courage, Aggression, Land, Siblings'},
    'Mercury':   {'sanskrit': 'Budha',    'significance': 'Buddhi, Intellect, Speech, Commerce'},
    'Jupiter':   {'sanskrit': 'Guru',     'significance': 'Jnana, Wisdom, Fortune, Children, Dharma'},
    'Venus':     {'sanskrit': 'Shukra',   'significance': 'Kama, Love, Beauty, Arts, Luxury'},
    'Saturn':    {'sanskrit': 'Shani',    'significance': 'Karma, Discipline, Delay, Hardship, Longevity'},
    'Rahu':      {'sanskrit': 'Rahu',     'significance': 'Maya, Illusion, Obsession, Foreign, Technology'},
    'Ketu':      {'sanskrit': 'Ketu',     'significance': 'Moksha, Detachment, Past Life, Spirituality'},
}

NAKSHATRA_LIST = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

RASHI_LIST = [
    'Mesha (Aries)', 'Vrishabha (Taurus)', 'Mithuna (Gemini)', 'Karka (Cancer)',
    'Simha (Leo)', 'Kanya (Virgo)', 'Tula (Libra)', 'Vrishchika (Scorpio)',
    'Dhanu (Sagittarius)', 'Makara (Capricorn)', 'Kumbha (Aquarius)', 'Meena (Pisces)'
]


class JyotishTransit:
    """Calculates Gochar (transit) of all 9 Grahas against natal positions."""
    
    def __init__(self, birth_date: str = "1993-12-24", birth_time: str = "05:40",
                 lat: float = 24.83, lon: float = 92.80, elevation: float = 35):
        """
        Initialize with birth data.
        
        Args:
            birth_date: 'YYYY-MM-DD'
            birth_time: 'HH:MM' (24hr, IST)
            lat: Latitude (default: Silchar)
            lon: Longitude (default: Silchar)
            elevation: Elevation in meters
        """
        self.lat = lat
        self.lon = lon
        
        dt_str = f"{birth_date} {birth_time}"
        self.birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
        self.observer = ephem.Observer()
        self.observer.lat = str(lat)
        self.observer.lon = str(lon)
        self.observer.elevation = elevation
        
        self.natal = self._calculate_positions(self.birth_dt)
        self.natal_nakshatras = {
            p: self._get_nakshatra(pos['ra'])
            for p, pos in self.natal.items() if p != 'Lagna'
        }
    
    def _get_planet_obj(self, name: str):
        """Map planet name to ephem object."""
        mapping = {
            'Sun': ephem.Sun(), 'Moon': ephem.Moon(), 'Mars': ephem.Mars(),
            'Mercury': ephem.Mercury(), 'Jupiter': ephem.Jupiter(),
            'Venus': ephem.Venus(), 'Saturn': ephem.Saturn(),
            'Rahu': ephem.Neptune(), 'Ketu': ephem.Uranus()
        }
        return mapping.get(name)
    
    def _calculate_positions(self, dt: datetime) -> Dict:
        """Calculate planetary positions for a given datetime."""
        self.observer.date = ephem.Date(dt)
        positions = {}
        
        # Lagna (Ascendant)
        sidereal_time = float(self.observer.sidereal_time())
        lagna_deg = (sidereal_time * 15 + self.lon) % 360
        lagna_rashi = int(lagna_deg / 30)
        positions['Lagna'] = {
            'ra': lagna_deg, 'rashi': lagna_rashi,
            'rashi_name': RASHI_LIST[lagna_rashi], 'degree': lagna_deg % 30
        }
        
        # All 9 Grahas
        for name in GRAHA_MAP:
            planet = self._get_planet_obj(name)
            if planet:
                planet.compute(self.observer)
                ra_deg = degrees(float(planet.ra))
                rashi = int(ra_deg / 30)
                positions[name] = {
                    'ra': ra_deg, 'rashi': rashi,
                    'rashi_name': RASHI_LIST[rashi], 'degree': ra_deg % 30,
                    'retrograde': hasattr(planet, 'retrograde') and planet.retrograde
                }
        
        return positions
    
    def _get_nakshatra(self, ra_deg: float) -> Dict:
        """Determine Nakshatra and Pada from right ascension."""
        nakshatra_span = 360 / 27
        index = int(ra_deg / nakshatra_span) % 27
        pada = int((ra_deg % nakshatra_span) / (nakshatra_span / 4)) + 1
        return {'name': NAKSHATRA_LIST[index], 'pada': pada}
    
    def get_current_transit(self) -> Dict:
        """Get current planetary positions (Gochar)."""
        now = datetime.now(datetime.UTC) + timedelta(hours=5, minutes=30)
        return self._calculate_positions(now)
    
    def _vedic_aspects(self, planet: str, house: int) -> Dict:
        """Determine Vedic aspect type based on house position."""
        full_aspects = {
            'Sun': [7], 'Moon': [7], 'Mars': [4, 7, 8],
            'Mercury': [7], 'Jupiter': [5, 7, 9], 'Venus': [7],
            'Saturn': [3, 7, 10], 'Rahu': [7], 'Ketu': [7],
        }
        kendras = [1, 4, 7, 10]
        trikonas = [1, 5, 9]
        dusthanas = [6, 8, 12]
        
        aspects_for_planet = full_aspects.get(planet, [7])
        
        if house == 1:
            return {'type': 'Conjunction (Yuti)', 'intensity': 'Strong'}
        elif house in aspects_for_planet:
            return {'type': 'Full Aspect (Drishti)', 'intensity': 'High'}
        elif house in trikonas:
            return {'type': 'Trine Aspect (Trikona)', 'intensity': 'Benefic'}
        elif house in kendras:
            return {'type': 'Angular (Kendra)', 'intensity': 'Moderate'}
        elif house in dusthanas:
            return {'type': 'Dusthana (Difficult)', 'intensity': 'Challenging'}
        else:
            return {'type': 'Neutral', 'intensity': 'Low'}
    
    def compare_transit(self) -> List[Dict]:
        """Compare current transit with natal chart."""
        current = self.get_current_transit()
        report = []
        
        for name, natal_pos in self.natal.items():
            if name == 'Lagna':
                continue
            
            cur_pos = current.get(name)
            if not cur_pos:
                continue
            
            natal_rashi = natal_pos['rashi']
            cur_rashi = cur_pos['rashi']
            house_from_natal = ((cur_rashi - natal_rashi) % 12) + 1
            aspects = self._vedic_aspects(name, house_from_natal)
            
            graha_info = GRAHA_MAP.get(name, {})
            
            report.append({
                'graha': name,
                'sanskrit': graha_info.get('sanskrit', name),
                'significance': graha_info.get('significance', ''),
                'natal_rashi': natal_pos['rashi_name'],
                'current_rashi': cur_pos['rashi_name'],
                'house_from_natal': house_from_natal,
                'aspect': aspects['type'],
                'intensity': aspects['intensity'],
                'nakshatra': self._get_nakshatra(cur_pos['ra'])['name'],
                'retrograde': cur_pos.get('retrograde', False)
            })
        
        return report
    
    def get_friction_report(self) -> List[Dict]:
        """Generate plain-language friction report."""
        transits = self.compare_transit()
        
        print("╔══════════════════════════════════════════════╗")
        print("║  🕉️ JYOTISH GOCHAR REPORT                    ║")
        print("╚══════════════════════════════════════════════╝\n")
        
        high_friction, benefic = [], []
        
        for t in transits:
            graha = t['graha']
            sanskrit = t['sanskrit']
            aspect = t['aspect']
            intensity = t['intensity']
            house = t['house_from_natal']
            
            if intensity in ['High', 'Challenging']:
                high_friction.append(t)
                symbol = "⚠️"
            elif intensity in ['Benefic', 'Strong'] and house in [1, 5, 9]:
                benefic.append(t)
                symbol = "✅"
            else:
                symbol = "➖"
            
            retrograde = " ℞" if t['retrograde'] else ""
            print(f"{symbol} {graha} ({sanskrit}) — House {house} from natal")
            print(f"   Natal: {t['natal_rashi']} → Current: {t['current_rashi']} | {t['nakshatra']}{retrograde}")
            print(f"   Aspect: {aspect} ({intensity})")
            print(f"   Domain: {t['significance']}\n")
        
        print("═" * 50)
        print("📊 SUMMARY")
        print("═" * 50)
        print(f"  ⚠️  High Friction: {len(high_friction)} areas")
        print(f"  ✅ Benefic: {len(benefic)} areas")
        print(f"\n🕉️ Sakshi Bhava: Observe without attachment.\n")
        
        return transits
    
    def to_json(self) -> str:
        """Export transit report as JSON."""
        return json.dumps(self.compare_transit(), indent=2, default=str)


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
        elif args[i] == '--lat' and i+1 < len(args):
            lat = float(args[i+1]); i += 2
        elif args[i] == '--lon' and i+1 < len(args):
            lon = float(args[i+1]); i += 2
        elif args[i] == '--json':
            engine = JyotishTransit(birth_date, birth_time, lat, lon)
            print(engine.to_json())
            sys.exit(0)
        else:
            i += 1
    
    engine = JyotishTransit(birth_date, birth_time, lat, lon)
    engine.get_friction_report()
