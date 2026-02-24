# ARM Rapid Set Vermarktung

**Kampagne:** Frostschäden-Reparatur mit ARM Kaltasphalt (Rapid Set)
**Angebot:** Kaufe 2 Paletten (2x48 Sack), davon 24 Sack ohne Berechnung!
**Laufzeit:** Ende März (Option Ende April)

---

## Übersicht (Stand: 24.02.2026)

Die Tiefbau- und GaLaBau-Listen wurden zu einer **gemeinsamen ARM-Kampagnenliste** zusammengeführt, dedupliziert und mit Ansprechpartner-Recherche angereichert.

| Kennzahl | Wert |
|----------|------|
| **Leads gesamt** | **1.705** (dedupliziert aus 1.081 Tiefbau + 728 GaLaBau) |
| **A-Leads** | **621** |
| **davon Tier 1 (anrufbereit, AP+Tel)** | **463** |
| **davon Tier 2 (ohne AP)** | **158** |
| **B-Leads** | **660** |
| **C-Leads** | **424** |

### AP-Abdeckung A-Leads

| Segment | A-Leads | Mit AP | Quote |
|---------|---------|--------|-------|
| Kommune (Bauhöfe/Straßenmeistereien) | 395 | 306 | **77%** |
| Privat (GaLaBau) | 139 | 119 | **86%** |
| Privat (Straßenbau) | 87 | 38 | **44%** |
| **Gesamt** | **621** | **463** | **75%** |

---

## Ordnerstruktur

```
Rapid-Set-Vermarktung/
├── README.md                              ← Du bist hier
├── Kampagnenkonzept_Frühjahrsaktion_ARM.md
├── Mailing 1 + 2 (PDFs)                  ← Händler-Mailings
│
└── Recherche Interessenten/
    │
    ├── ── KAMPAGNEN-HAUPTDATEIEN ─────────────────────
    │
    ├── ARM_Kampagne_Leadliste.xlsx        ← EXCEL Hauptdatei (5 Tier-Tabs + Zusammenfassung)
    ├── ARM_Kampagne_Gesamtliste.csv       ← CSV für CRM-Import (1.705 Leads)
    ├── ARM_Tier1_Kampagnenbereit.csv       ← Nur Tier 1 (463 anrufbereite Leads)
    ├── Gespraechsleitfaden_ARM_Kampagne_Gesamt.md  ← Telefonleitfaden
    │
    ├── ── QUELLDATEN (TIEFBAU) ───────────────────────
    │
    ├── PROJEKTSTATUS_ARM_Kampagne.md       ← Projektstatus (aktuell)
    ├── ARM_Anrufliste_Priorisiert.csv      ← Original Tiefbau-Liste (1.081)
    ├── ARM_CRM_Import_Leads.csv            ← Salesforce Import Tiefbau
    ├── Recherche Tiefbauunternehmen PLZ 0-9 durch claude.md
    │
    ├── ── QUELLDATEN (GALABAU) ───────────────────────
    │
    ├── PROJEKTSTATUS_GaLaBau_Kampagne.md   ← Status GaLaBau
    ├── GaLaBau_Anrufliste_Priorisiert.csv  ← Original GaLaBau-Liste (728)
    ├── GaLaBau_CRM_Import_Leads.csv        ← Salesforce Import GaLaBau
    ├── Recherche GaLaBau PLZ 0-9 durch claude.md
    │
    ├── ── AP-RECHERCHE-ERGEBNISSE ────────────────────
    │
    ├── GaLaBau_Kommunen_Ansprechpartner_Recherche.csv
    ├── Kommunen_Recherche_Batch7.csv ... BatchG.csv  ← Kommune-Batches
    ├── Tiefbau_GF_Recherche_Batch1-3.csv              ← Straßenbau GF-Recherche
    ├── GaLaBau_GF_Recherche_Batch_K-M.csv / N-Z.csv   ← GaLaBau GF-Recherche
    ├── Strassenbau_GF_Recherche_Batch_A-J.csv / K-Z.csv
    │
    └── ── SCRIPTS & SONSTIGES ────────────────────────
        ├── integrate_recherche.py          ← Recherche-Integration
        ├── export_excel.py                 ← Excel-Export Script
        ├── generate_leadlist.py            ← Original Tiefbau-Script
        ├── generate_galabau_leadlist.py    ← Original GaLaBau-Script
        └── Datensatzbeispiele_Leadimport CRM.xlsx
```

---

## Schnellstart für das Telefonteam

1. **Leitfaden lesen:** `Gespraechsleitfaden_ARM_Kampagne_Gesamt.md`
2. **Excel öffnen:** `ARM_Kampagne_Leadliste.xlsx` — Tab "Tier 1 Anrufbereit" starten
3. **Farbcode:** Blau = Kommune, Grün = GaLaBau, Orange = Straßenbau
4. **Tier 2 Kommunen:** Bauhof anrufen, nach Leiter/Straßenmeister fragen

---

## Technisches

- **Python 3** + `openpyxl` benötigt (`pip install openpyxl`)
- **Excel-Export:** `python export_excel.py` im Ordner `Recherche Interessenten/`
- **CRM-Import:** `ARM_Kampagne_Gesamtliste.csv` (UTF-8-BOM, Semikolon-Delimiter, Salesforce-kompatibel)
- **Recherche-Integration:** `python integrate_recherche.py` (alle Batch-CSVs → Hauptliste)
