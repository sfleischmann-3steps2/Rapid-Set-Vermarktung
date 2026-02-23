#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Ansprechpartner in der ARM Anrufliste.
Fügt recherchierte Ansprechpartner zu Leads hinzu, die bisher keinen haben.
Unterscheidet zwischen Kommunen (Match per Stadt) und Privat (Match per Firma).
"""

import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# === KOMMUNEN: Match per Ort, nur Kategorie "Kommune" ===
KOMMUNEN_UPDATES = {
    "Stuttgart": "Jürgen Mutz (Amtsleiter)",
    "München": "Horst Schiller (Hauptabteilungsleiter Tiefbau)",
    "Dortmund": "Sylvia Uehlendahl (Amtsleiterin)",
    "Düsseldorf": "Katharina Metzker (Amtsleiterin)",
    "Frankfurt am Main": "Michaela Kraft (Leiterin ASE)",
    "Bochum": "Birgit Muéll (Amtsleiterin)",
    "Wuppertal": "Daniel Warwas (Ressortleiter)",
    "Karlsruhe": "Heike Weißer (Amtsleiterin)",
    "Münster": "Gerhard Rüller (Amtsleiter)",
    "Freiburg im Breisgau": "Frank Uekermann (Amtsleiter)",
    "Heidelberg": "Klaus-Peter Hofbauer (Amtsleiter)",
    "Chemnitz": "Thomas Blankenhagel (amt. Amtsleiter)",
    "Saarbrücken": "Werner Maurer (Amtsleiter)",
    "Wiesbaden": "Gerald Berg (Amtsleiter)",
    "Gießen": "Peter Ravizza (Amtsleiter)",
    "Rüsselsheim am Main": "Manuela Metzsch (Amtsleiterin)",
}

# === PRIVATE UNTERNEHMEN: Match per Teilstring im Firmennamen ===
FIRMEN_UPDATES = {
    "Donauasphalt": "Anna Kollmer (Geschäftsführerin)",
}


def update_csv():
    input_file = os.path.join(SCRIPT_DIR, "ARM_Anrufliste_Priorisiert.csv")
    output_file = os.path.join(SCRIPT_DIR, "ARM_Anrufliste_Priorisiert_updated.csv")

    # First: re-read from the ORIGINAL generated file to undo wrong updates
    # Re-run generate_leadlist.py would be safest, but let's just fix what we have
    updated_kommune = 0
    updated_firma = 0
    total_count = 0
    already_has_original = 0
    cleared = 0

    with open(input_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        total_count += 1
        ort = row.get("Ort", "").strip()
        kategorie = row.get("Kategorie", "").strip()
        firma = row.get("Firma", "").strip()
        existing = row.get("Ansprechpartner", "").strip()

        # First: Clear wrongly assigned Kommune-Ansprechpartner from private firms
        # (from the previous buggy run)
        if kategorie != "Kommune" and existing and ort in KOMMUNEN_UPDATES:
            if existing == KOMMUNEN_UPDATES[ort]:
                row["Ansprechpartner"] = ""
                cleared += 1
                existing = ""

        if existing:
            already_has_original += 1
            continue

        # Kommune: Match per Ort
        if kategorie == "Kommune" and ort in KOMMUNEN_UPDATES:
            row["Ansprechpartner"] = KOMMUNEN_UPDATES[ort]
            updated_kommune += 1
            continue

        # Privat: Match per Firmenname (Teilstring)
        for key, name in FIRMEN_UPDATES.items():
            if key.lower() in firma.lower():
                row["Ansprechpartner"] = name
                updated_firma += 1
                break

    # Write files
    for filepath in [output_file, input_file]:
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)

    print(f"=== Ansprechpartner-Update (korrigiert) ===")
    print(f"Leads gesamt: {total_count}")
    print(f"Falsche Zuordnungen bereinigt: {cleared}")
    print(f"Bereits mit Ansprechpartner: {already_has_original}")
    print(f"Kommunen aktualisiert: {updated_kommune}")
    print(f"Firmen aktualisiert: {updated_firma}")
    print(f"Weiterhin ohne: {total_count - already_has_original - updated_kommune - updated_firma}")
    print(f"\n=== Kommunen-Updates ({updated_kommune}) ===")
    for ort, name in sorted(KOMMUNEN_UPDATES.items()):
        print(f"  {ort}: {name}")
    print(f"\n=== Firmen-Updates ({updated_firma}) ===")
    for key, name in sorted(FIRMEN_UPDATES.items()):
        print(f"  {key}: {name}")


if __name__ == "__main__":
    update_csv()
