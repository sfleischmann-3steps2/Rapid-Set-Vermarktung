#!/usr/bin/env python3
"""
Konvertiert ARM_Tier1_Kampagnenbereit.csv in das Salesforce CRM Lead-Import-Format.

Quell-Spalten (Semikolon-getrennt):
  Priorität;Firma;Kategorie;Ansprechpartner;Telefon;Email;PLZ;Ort;Gesprächsaufhänger;Notiz;Quelle

Ziel-Spalten (Komma-getrennt, Salesforce-Standard):
  First Name,Last Name,Company,Title,Phone,Email,Lead Status,Rating,Street,City,
  State/Province,Zip/Postal Code,Country,Website,No. Of Employees,Annual Revenue,
  Lead Source,Industry,Description
"""

import csv
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_Tier1_Kampagnenbereit.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_Tier1_CRM_Import.csv")

# Salesforce header
CRM_HEADERS = [
    "First Name", "Last Name", "Company", "Title", "Phone", "Email",
    "Lead Status", "Rating", "Street", "City", "State/Province",
    "Zip/Postal Code", "Country", "Website", "No. Of Employees",
    "Annual Revenue", "Lead Source", "Industry", "Description"
]

# Priorität -> Salesforce Rating
PRIORITY_TO_RATING = {
    "A": "Hot",
    "B": "Warm",
    "C": "Cold",
}

# Kategorie -> Salesforce Industry
KATEGORIE_TO_INDUSTRY = {
    "Kommune": "Government",
    "Privat (GaLaBau)": "Construction",
    "Privat (Straßenbau)": "Construction",
}

# Titles/salutations to strip from name
SALUTATIONS = {"herr", "frau", "dr.", "prof.", "ing.", "dipl.-ing."}


def parse_ansprechpartner(name_raw):
    """Parse Ansprechpartner into (first_name, last_name, title)."""
    if not name_raw or not name_raw.strip():
        return "", "", ""

    name = name_raw.strip()

    # Extract parenthetical info as title hint
    title = ""
    paren_match = re.search(r'\(([^)]+)\)', name)
    if paren_match:
        paren_content = paren_match.group(1).strip()
        # Filter out non-title hints
        non_titles = {"Kontakt", "Vertretung", "Sample"}
        if paren_content not in non_titles:
            title = paren_content
        name = name[:paren_match.start()].strip()

    # Split into parts
    parts = name.split()
    if not parts:
        return "", "", title

    # Remove salutations from beginning
    cleaned_parts = []
    for part in parts:
        if part.lower().rstrip(".") + "." in SALUTATIONS or part.lower() in SALUTATIONS:
            continue
        cleaned_parts.append(part)

    if not cleaned_parts:
        # Only salutations, use original parts
        cleaned_parts = parts

    if len(cleaned_parts) == 1:
        return "", cleaned_parts[0], title
    else:
        first_name = cleaned_parts[0]
        last_name = " ".join(cleaned_parts[1:])
        return first_name, last_name, title


def build_description(row):
    """Build Description from Gesprächsaufhänger, Notiz, and Quelle."""
    parts = []
    if row.get("Gesprächsaufhänger", "").strip():
        parts.append(f"Gesprächsaufhänger: {row['Gesprächsaufhänger'].strip()}")
    if row.get("Notiz", "").strip():
        parts.append(f"Notiz: {row['Notiz'].strip()}")
    if row.get("Quelle", "").strip():
        parts.append(f"Quelle: {row['Quelle'].strip()}")
    return " | ".join(parts)


def convert():
    rows_written = 0

    # Read source CSV (semicolon-separated, UTF-8 with BOM)
    with open(INPUT_FILE, "r", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile, delimiter=";")

        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=CRM_HEADERS)
            writer.writeheader()

            for row in reader:
                first_name, last_name, title = parse_ansprechpartner(
                    row.get("Ansprechpartner", "")
                )

                prioritaet = row.get("Priorität", row.get("\ufeffPriorität", "")).strip()
                kategorie = row.get("Kategorie", "").strip()

                crm_row = {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Company": row.get("Firma", "").strip(),
                    "Title": title,
                    "Phone": row.get("Telefon", "").strip(),
                    "Email": row.get("Email", "").strip(),
                    "Lead Status": "New",
                    "Rating": PRIORITY_TO_RATING.get(prioritaet, ""),
                    "Street": "",
                    "City": row.get("Ort", "").strip(),
                    "State/Province": "",
                    "Zip/Postal Code": row.get("PLZ", "").strip(),
                    "Country": "Germany",
                    "Website": "",
                    "No. Of Employees": "",
                    "Annual Revenue": "",
                    "Lead Source": "ARM Kampagne",
                    "Industry": KATEGORIE_TO_INDUSTRY.get(kategorie, kategorie),
                    "Description": build_description(row),
                }

                writer.writerow(crm_row)
                rows_written += 1

    print(f"Konvertierung abgeschlossen: {rows_written} Leads geschrieben nach {OUTPUT_FILE}")


if __name__ == "__main__":
    convert()
