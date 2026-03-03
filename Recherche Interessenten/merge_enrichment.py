#!/usr/bin/env python3
"""
Merged bestehende Adress-Anreicherungen (Straße + Adresse_Status) aus der alten
enriched CSV in die neu gefilterte ARM_ADM_Gesamtliste.csv.

Lookup-Key: Email (case-insensitive). Neue Leads ohne Match bekommen Status "pending".

Eingabe:
  - ARM_ADM_Gesamtliste.csv           (neu gefiltert, ohne Straße)
  - ARM_ADM_Gesamtliste_enriched_backup.csv  (alte enriched CSV als Lookup)

Ausgabe:
  - ARM_ADM_Gesamtliste_enriched.csv  (merged: alte Adressen + neue Leads mit "pending")
"""

import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_CSV = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste.csv")
OLD_ENRICHED = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste_enriched_backup.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste_enriched.csv")


def main():
    # 1. Alte enriched CSV als Lookup laden (Email → Straße + Status)
    lookup = {}
    if os.path.exists(OLD_ENRICHED):
        with open(OLD_ENRICHED, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                email = row.get("Email", "").strip().lower()
                if email:
                    lookup[email] = {
                        "Straße": row.get("Straße", "").strip(),
                        "Adresse_Status": row.get("Adresse_Status", "").strip(),
                    }
        print(f"Lookup geladen: {len(lookup)} Einträge aus {os.path.basename(OLD_ENRICHED)}")
    else:
        print(f"WARNUNG: {os.path.basename(OLD_ENRICHED)} nicht gefunden — alle Leads bekommen 'pending'")

    # 2. Neue gefilterte CSV lesen
    with open(NEW_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)
    print(f"Eingabe: {len(rows)} Leads aus {os.path.basename(NEW_CSV)}")

    # 3. Merge
    out_fieldnames = list(fieldnames) + ["Straße", "Adresse_Status"]
    merged_rows = []
    matched = 0
    pending = 0

    for row in rows:
        email = row.get("Email", "").strip().lower()
        enriched = dict(row)

        if email in lookup:
            enriched["Straße"] = lookup[email]["Straße"]
            enriched["Adresse_Status"] = lookup[email]["Adresse_Status"]
            matched += 1
        else:
            enriched["Straße"] = ""
            enriched["Adresse_Status"] = "pending"
            pending += 1

        merged_rows.append(enriched)

    # 4. Schreiben
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged_rows)

    # 5. Report
    found = sum(1 for r in merged_rows if r["Adresse_Status"] == "found")
    not_found = sum(1 for r in merged_rows if r["Adresse_Status"] == "not_found")
    print()
    print(f"Ergebnis:")
    print(f"  Matched (aus Backup):  {matched}")
    print(f"    davon found:         {found}")
    print(f"    davon not_found:     {not_found}")
    print(f"  Neu (pending):         {pending}")
    print(f"  Gesamt:                {len(merged_rows)}")
    print(f"→ Ausgabe: {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
