# ARM Rapid Set Vermarktung

**Kampagne:** Frostschäden-Reparatur mit ARM Kaltasphalt (Rapid Set)
**Händler-Angebot:** 2 Paletten kaufen (2x48 Sack), davon 24 Sack ohne Berechnung (nur für Händler)
**Laufzeit:** Ende März (Option Ende April)

---

## Landing Page

Die Landing Page für Endkunden (Produktinformation, ohne Aktionsangebot) wird im separaten Repo gepflegt:

| | |
|---|---|
| **Repo** | [Marketing-Team-Skills](https://github.com/sfleischmann-3steps2/Marketing-Team-Skills) |
| **Live (v2)** | [ARM Produktseite](https://sfleischmann-3steps2.github.io/Marketing-Team-Skills/projekte/korodur-asphalt-repair-mix/landing-page/index.html) |
| **Archiv (v1)** | [Frühjahrsaktion Vollversion](https://sfleischmann-3steps2.github.io/Marketing-Team-Skills/projekte/korodur-asphalt-repair-mix/landing-page/archiv/index-v1-fruehjahrsaktion.html) |
| **Status** | v2 live, wartet auf Kollegen-Feedback |

**Konzept:** KORODUR schickt E-Mail an Händler (mit Aktionsangebot) → Händler schicken E-Mail an ihre Kunden (mit Link zur Landing Page) → Endkunde sieht Produktinfo und kauft beim Händler.

---

## Übersicht (Stand: 27.02.2026)

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

### ADM-Gebiete (Pilotstart)

Die Kampagne startet zunächst in den Gebieten von 4 Außendienstmitarbeitern:

| Fachberater | PLZ-Gebiete | Kampagnenbereit |
|---|---|---|
| Jens Sackmann | 20–29 | 38 |
| André Grahn | 40–49, 50–53, 57–59 | 109 |
| Jens Lang | 70–79, 86–89 | 64 |
| Daniel May | 80–85, 94 | 26 |
| Francesco Palese | 90–93, 95–97 | 49 |
| **TOTAL** | | **286** |

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
    ├── ARM_Kampagne_Gesamtliste.csv       ← CSV Master-Liste (1.705 Leads, bundesweit)
    ├── ARM_Tier1_Kampagnenbereit.csv       ← Nur Tier 1 (463 anrufbereite Leads)
    │
    ├── ── ADM-GEBIETE (PILOTSTART) ─────────────────
    │
    ├── ARM_ADM_Gesamtliste.csv            ← 286 kampagnenbereite Leads (mit Fachberater)
    ├── ARM_ADM_Kampagne.xlsx              ← Excel: Übersicht + 5 Fachberater-Tabs (286 Leads)
    ├── ARM_ADM_CRM_Import.csv             ← Salesforce-Import (286 Leads, Komma-Delimiter)
    ├── Verkaufsgebiete_ARM.md             ← PLZ → Fachberater Zuordnungstabelle
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
        ├── filter_adm_territories.py      ← ADM-Gebiete filtern + Export
        ├── integrate_recherche.py          ← Recherche-Integration
        ├── export_excel.py                 ← Excel-Export Script
        ├── convert_arm_to_crm.py           ← CRM-Konvertierung (bundesweit)
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
- **ADM-Filter:** `python filter_adm_territories.py` — filtert auf 4 Fachberater-Gebiete, erzeugt CSV + Excel + CRM-Import
- **Excel-Export:** `python export_excel.py` — bundesweite Leadliste als Excel
- **CRM-Import:** `ARM_Kampagne_Gesamtliste.csv` (UTF-8-BOM, Semikolon-Delimiter, Salesforce-kompatibel)
- **Recherche-Integration:** `python integrate_recherche.py` (alle Batch-CSVs → Hauptliste)
