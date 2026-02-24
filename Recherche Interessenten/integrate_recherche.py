#!/usr/bin/env python3
"""
Integriert alle Recherche-Ergebnisse in ARM_Kampagne_Gesamtliste.csv
"""
import csv
import re
import unicodedata
from collections import defaultdict

def normalize(s):
    """Normalize string for matching: lowercase, strip, remove umlauts/accents"""
    if not s:
        return ""
    s = s.strip().lower()
    # Common German city name normalizations
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = s.replace("/", " ").replace("-", " ").replace(".", " ")
    # Remove extra spaces
    s = re.sub(r'\s+', ' ', s)
    return s

def has_contact(ap):
    """Check if Ansprechpartner field has a real contact"""
    if not ap:
        return False
    ap = ap.strip()
    return ap and ap != "-" and ap.lower() != "nicht gefunden" and ap != ""

def extract_plz_from_text(text):
    """Extract PLZ from text like 'Stadt (PLZ)' or 'PLZ Stadt'"""
    m = re.search(r'\((\d{5})\)', text)
    if m:
        return m.group(1)
    m = re.search(r'(\d{5})', text)
    if m:
        return m.group(1)
    return ""

def extract_city_from_firma(firma_field, ort_field):
    """Extract normalized city name from Firma or Ort field"""
    # Try Ort field first
    if ort_field and ort_field.strip():
        city = ort_field.strip()
        # Remove "v.d. Höhe" etc.
        city = re.sub(r'\s+v\.d\.\s+.*$', '', city)
        return normalize(city)
    return ""

# ===== LOAD MAIN LIST =====
print("=" * 60)
print("INTEGRATION: Alle Recherche-Ergebnisse -> Hauptliste")
print("=" * 60)

main_file = "ARM_Kampagne_Gesamtliste.csv"
with open(main_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"\nHauptliste geladen: {len(rows)} Leads")
print(f"Spalten: {fieldnames}")

# Build indexes for matching
# For Kommunen: match by PLZ + normalized city name
# For private companies: match by PLZ + partial company name
kommun_by_plz = defaultdict(list)  # PLZ -> list of row indices
kommun_by_city = defaultdict(list)  # normalized city -> list of row indices
privat_by_plz = defaultdict(list)  # PLZ -> list of row indices

for i, r in enumerate(rows):
    cat = r.get('Kategorie', '')
    plz = r.get('PLZ', '').strip()
    ort = r.get('Ort', '').strip()
    firma = r.get('Firma', '').strip()

    if cat == 'Kommune':
        if plz:
            kommun_by_plz[plz].append(i)
        city_norm = normalize(ort)
        if city_norm:
            kommun_by_city[city_norm].append(i)
        # Also index by normalized firma parts
        firma_norm = normalize(firma)
        for part in firma_norm.split():
            if len(part) > 3:
                kommun_by_city[part].append(i)
    elif 'Privat' in cat or 'Straßenbau' in cat or 'GaLaBau' in cat:
        if plz:
            privat_by_plz[plz].append(i)

# ===== INTEGRATION FUNCTIONS =====
updates_count = 0
updates_detail = []

def update_lead(idx, ap, telefon, email, source_label):
    """Update a lead at index idx with new contact data"""
    global updates_count
    r = rows[idx]
    old_ap = r.get('Ansprechpartner', '')

    # Only update if we have a real new contact and current is empty
    if not has_contact(ap):
        return False
    if has_contact(old_ap):
        return False  # Don't overwrite existing contacts

    r['Ansprechpartner'] = ap
    if telefon and telefon.strip():
        r['Telefon'] = telefon.strip()
    if email and email.strip():
        r['Email'] = email.strip()

    updates_count += 1
    updates_detail.append(f"  [{source_label}] {r.get('Firma', '?')[:40]} ({r.get('Ort', '?')}) <- {ap}")
    return True

def find_kommune_match(city_name, plz=""):
    """Find matching Kommune in main list by city name and/or PLZ"""
    city_norm = normalize(city_name)

    # Remove common suffixes for matching
    city_clean = city_norm
    for suffix in [' saale', ' saar', ' pfalz', ' schwarzwald', ' taunus', ' allgaeu',
                   ' oberbayern', ' i ob', ' im allgaeu', ' a d pegnitz']:
        city_clean = city_clean.replace(suffix, '')
    city_clean = city_clean.strip()

    candidates = set()

    # Match by PLZ (most reliable)
    if plz:
        for idx in kommun_by_plz.get(plz, []):
            candidates.add(idx)

    # Match by city name
    for idx in kommun_by_city.get(city_norm, []):
        candidates.add(idx)
    for idx in kommun_by_city.get(city_clean, []):
        candidates.add(idx)

    # Try matching individual words of city name
    for word in city_norm.split():
        if len(word) > 4:
            for idx in kommun_by_city.get(word, []):
                # Verify PLZ match if available
                if plz and rows[idx].get('PLZ', '').strip() == plz:
                    candidates.add(idx)

    # Filter to only Kommune entries without existing AP
    result = []
    for idx in candidates:
        if rows[idx].get('Kategorie', '') == 'Kommune':
            result.append(idx)

    return list(set(result))

def find_privat_match(firma_text, plz=""):
    """Find matching private company in main list"""
    candidates = set()

    # Extract PLZ from firma text if not provided
    if not plz:
        plz = extract_plz_from_text(firma_text)

    if plz:
        for idx in privat_by_plz.get(plz, []):
            candidates.add(idx)

    if not candidates:
        return []

    # Narrow by company name similarity
    firma_norm = normalize(firma_text)
    firma_words = set(w for w in firma_norm.split() if len(w) > 2)

    best_matches = []
    for idx in candidates:
        main_firma = normalize(rows[idx].get('Firma', ''))
        main_words = set(w for w in main_firma.split() if len(w) > 2)
        overlap = firma_words & main_words
        if len(overlap) >= 2 or (len(overlap) >= 1 and len(firma_words) <= 3):
            best_matches.append((idx, len(overlap)))

    # Sort by overlap count
    best_matches.sort(key=lambda x: -x[1])
    return [idx for idx, _ in best_matches]

# ===== PROCESS KOMMUNE RESEARCH FILES =====
print("\n--- Kommune-Recherche Integration ---")

# 1. GaLaBau_Kommunen_Ansprechpartner_Recherche.csv (first round)
source1_count = 0
with open("GaLaBau_Kommunen_Ansprechpartner_Recherche.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        stadt = r.get('Stadt', '')
        plz = r.get('PLZ', '').strip()
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')
        status = r.get('Status', '')

        if not has_contact(ap):
            continue

        matches = find_kommune_match(stadt, plz)
        for idx in matches:
            if update_lead(idx, ap, telefon, email, "Kommunen-Runde1"):
                source1_count += 1
print(f"  Kommunen Runde 1: {source1_count} Updates")

# 2. Kommunen_Recherche_Batch7.csv (Batch A: Altenburg-Jena)
source2_count = 0
with open("Kommunen_Recherche_Batch7.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        stadt_raw = r.get('Stadt', '')
        # Format: "Stadt (PLZ)"
        plz = extract_plz_from_text(stadt_raw)
        stadt = re.sub(r'\s*\(\d{5}\)', '', stadt_raw).strip()
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_kommune_match(stadt, plz)
        for idx in matches:
            if update_lead(idx, ap, telefon, email, "Kommunen-BatchA"):
                source2_count += 1
print(f"  Kommunen Batch A: {source2_count} Updates")

# 3. Kommunen_Ansprechpartner_Recherche_K-S.csv (Batch B)
source3_count = 0
with open("Kommunen_Ansprechpartner_Recherche_K-S.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        stadt = r.get('Stadt', '').strip()
        plz = r.get('PLZ', '').strip()
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_kommune_match(stadt, plz)
        for idx in matches:
            if update_lead(idx, ap, telefon, email, "Kommunen-BatchB"):
                source3_count += 1
print(f"  Kommunen Batch B: {source3_count} Updates")

# 4. Recherche_Bauhof_Kommunen_Batch3.csv (Batch C)
source4_count = 0
with open("Recherche_Bauhof_Kommunen_Batch3.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        stadt_raw = r.get('Stadt', '')
        plz = extract_plz_from_text(stadt_raw)
        stadt = re.sub(r'\s*\(\d{5}\)', '', stadt_raw).strip()
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_kommune_match(stadt, plz)
        for idx in matches:
            if update_lead(idx, ap, telefon, email, "Kommunen-BatchC"):
                source4_count += 1
print(f"  Kommunen Batch C: {source4_count} Updates")

# ===== PROCESS STRAENBAU RESEARCH FILES =====
print("\n--- Straßenbau-Recherche Integration ---")

# 5. Strassenbau_GF_Recherche_Batch_A-J.csv
source5_count = 0
with open("Strassenbau_GF_Recherche_Batch_A-J.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        firma_raw = r.get('Firma', '')
        plz = extract_plz_from_text(firma_raw)
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_privat_match(firma_raw, plz)
        for idx in matches[:1]:  # Only update first match
            if update_lead(idx, ap, telefon, email, "Strassenbau-A-J"):
                source5_count += 1
print(f"  Straßenbau Batch A-J: {source5_count} Updates")

# 6. Strassenbau_GF_Recherche_Batch_K-Z.csv
source6_count = 0
with open("Strassenbau_GF_Recherche_Batch_K-Z.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        firma_raw = r.get('Firma', '')
        plz = extract_plz_from_text(firma_raw)
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_privat_match(firma_raw, plz)
        for idx in matches[:1]:
            if update_lead(idx, ap, telefon, email, "Strassenbau-K-Z"):
                source6_count += 1
print(f"  Straßenbau Batch K-Z: {source6_count} Updates")

# ===== PROCESS GALABAU RESEARCH FILES =====
print("\n--- GaLaBau-Recherche Integration ---")

# 7. GaLaBau_GF_Recherche_Batch_K-M.csv
source7_count = 0
with open("GaLaBau_GF_Recherche_Batch_K-M.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        firma_raw = r.get('Firma', '')
        plz = extract_plz_from_text(firma_raw)
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_privat_match(firma_raw, plz)
        for idx in matches[:1]:
            if update_lead(idx, ap, telefon, email, "GaLaBau-Batch1"):
                source7_count += 1
print(f"  GaLaBau Batch 1 (K-M): {source7_count} Updates")

# 8. GaLaBau_GF_Recherche_Batch_N-Z.csv
source8_count = 0
with open("GaLaBau_GF_Recherche_Batch_N-Z.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        firma_raw = r.get('Firma', '')
        plz = extract_plz_from_text(firma_raw)
        ap = r.get('Ansprechpartner', '')
        telefon = r.get('Telefon', '')
        email = r.get('Email', '')

        if not has_contact(ap):
            continue

        matches = find_privat_match(firma_raw, plz)
        for idx in matches[:1]:
            if update_lead(idx, ap, telefon, email, "GaLaBau-Batch2"):
                source8_count += 1
print(f"  GaLaBau Batch 2 (N-Z): {source8_count} Updates")

# ===== SAVE UPDATED LIST =====
print(f"\n{'=' * 60}")
print(f"GESAMT-UPDATES: {updates_count}")
print(f"{'=' * 60}")

# Show all updates
if updates_detail:
    print("\nAlle Updates:")
    for d in updates_detail:
        print(d)

# Save
with open(main_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f"\nDatei gespeichert: {main_file}")

# ===== FINAL STATISTICS =====
print(f"\n{'=' * 60}")
print("FINALE STATISTIK nach Integration")
print(f"{'=' * 60}")

cats = defaultdict(lambda: {"total": 0, "with_ap": 0, "without_ap": 0, "A": 0, "B": 0, "C": 0})
for r in rows:
    cat = r.get('Kategorie', '?')
    prio = r.get('Priorität', '?')
    ap = r.get('Ansprechpartner', '').strip()

    cats[cat]["total"] += 1
    if prio in ('A', 'B', 'C'):
        cats[cat][prio] += 1

    if has_contact(ap):
        cats[cat]["with_ap"] += 1
    else:
        cats[cat]["without_ap"] += 1

total_with = 0
total_without = 0
for cat in sorted(cats.keys()):
    d = cats[cat]
    pct = round(100 * d["with_ap"] / d["total"]) if d["total"] > 0 else 0
    total_with += d["with_ap"]
    total_without += d["without_ap"]
    print(f"{cat:30s} | {d['total']:4d} | AP: {d['with_ap']:4d} ({pct:3d}%) | ohne: {d['without_ap']:4d} | A:{d['A']:3d} B:{d['B']:3d} C:{d['C']:3d}")

print(f"{'─' * 90}")
total = total_with + total_without
pct_total = round(100 * total_with / total) if total > 0 else 0
print(f"{'GESAMT':30s} | {total:4d} | AP: {total_with:4d} ({pct_total:3d}%) | ohne: {total_without:4d}")
