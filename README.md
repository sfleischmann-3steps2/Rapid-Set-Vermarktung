# ARM Rapid Set Vermarktung

**Kampagne:** Frostschäden-Reparatur mit ARM Kaltasphalt (Rapid Set)
**Angebot:** Kaufe 2 Paletten (2x48 Sack), davon 24 Sack ohne Berechnung!
**Laufzeit:** Ende März (Option Ende April)

---

## Übersicht

| Kampagne | Leads | A-Leads | B-Leads | C-Leads |
|----------|-------|---------|---------|---------|
| **Tiefbau** | 1.081 | 416 | 458 | 207 |
| **GaLaBau** | 728 | 278 | 233 | 217 |
| **Gesamt** | **1.809** | **694** | **691** | **424** |

---

## Ordnerstruktur

```
Rapid-Set-Vermarktung/
├── README.md                          ← Du bist hier
├── Mailing 1 + 2 (PDFs)              ← Händler-Mailings
│
└── Recherche Interessenten/
    │
    ├── Gespraechsleitfaden_ARM_Kampagne_Gesamt.md  ← Telefonleitfaden (Tiefbau + GaLaBau)
    │
    ├── ── TIEFBAU-KAMPAGNE ──────────────────────────
    │
    ├── PROJEKTSTATUS_ARM_Kampagne.md          ← Status Tiefbau
    ├── generate_leadlist.py                   ← Script Tiefbau
    ├── ARM_Anrufliste_Priorisiert.csv         ← Anrufliste (A→B→C)
    ├── ARM_CRM_Import_Leads.csv               ← Salesforce Import
    ├── ARM_Leadliste_Komplett.xlsx             ← Excel A/B/C Tabs
    ├── Recherche Tiefbauunternehmen PLZ 0-9 durch claude.md
    │
    ├── ── GALABAU-KAMPAGNE ──────────────────────────
    │
    ├── PROJEKTSTATUS_GaLaBau_Kampagne.md      ← Status GaLaBau
    ├── generate_galabau_leadlist.py            ← Script GaLaBau
    ├── GaLaBau_Anrufliste_Priorisiert.csv     ← Anrufliste (A→B→C)
    ├── GaLaBau_CRM_Import_Leads.csv           ← Salesforce Import
    ├── GaLaBau_Leadliste_Komplett.xlsx         ← Excel A/B/C Tabs
    ├── Recherche GaLaBau PLZ 0-9 durch claude.md
    │
    └── ── SONSTIGE ──────────────────────────────────
        ├── deep-research-report chat GPT.md   ← ChatGPT Erstrecherche (PLZ 9)
        ├── Tiefbauämter Region 9_gemini.pdf   ← Gemini Erstrecherche (PLZ 9)
        ├── Datensatzbeispiele_Leadimport CRM.xlsx
        └── update_ansprechpartner.py          ← Ansprechpartner-Ergänzung
```

---

## Schnellstart für das Telefonteam

1. **Leitfaden lesen:** `Gespraechsleitfaden_ARM_Kampagne_Gesamt.md` (gilt für Tiefbau + GaLaBau)
2. **Anrufliste öffnen:**
   - Tiefbau: `ARM_Anrufliste_Priorisiert.csv`
   - GaLaBau: `GaLaBau_Anrufliste_Priorisiert.csv`
3. **Excel-Übersicht:** `ARM_Leadliste_Komplett.xlsx` / `GaLaBau_Leadliste_Komplett.xlsx`

---

## Technisches

- **Python-Scripts:** `python generate_leadlist.py` / `python generate_galabau_leadlist.py`
- **Abhängigkeit:** `pip install openpyxl` (für Excel-Export)
- **CRM-Format:** UTF-8-BOM, Semikolon-Delimiter (Salesforce-kompatibel)
