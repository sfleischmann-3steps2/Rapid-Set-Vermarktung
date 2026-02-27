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

Die Master-Liste (`ARM_Kampagne_Gesamtliste.csv`) enthält **1.759 Leads** bundesweit. Für den Pilotstart wurde auf die Gebiete von 5 Außendienstmitarbeitern gefiltert — nur Leads mit vollständigen Kontaktdaten (AP + Telefon + Email).

### ADM-Gebiete (Pilotstart)

| Fachberater | PLZ-Gebiete | Kampagnenbereit |
|---|---|---|
| Jens Sackmann | 20–29 | 92 |
| André Grahn | 40–49, 50–53, 57–59 | 109 |
| Jens Lang | 70–79, 86–89 | 64 |
| Daniel May | 80–85, 94 | 26 |
| Francesco Palese | 90–93, 95–97 | 49 |
| **TOTAL** | | **340** |

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
    ├── ── ADM-KAMPAGNE (AKTIV) ─────────────────────
    │
    ├── ARM_ADM_Gesamtliste.csv            ← 340 kampagnenbereite Leads (mit Fachberater)
    ├── ARM_ADM_Kampagne.xlsx              ← Excel: Übersicht + 5 Fachberater-Tabs
    ├── ARM_ADM_CRM_Import.csv             ← Salesforce-Import (340 Leads)
    ├── Verkaufsgebiete_ARM.md             ← PLZ → Fachberater Zuordnungstabelle
    ├── Gespraechsleitfaden_ARM_Kampagne_Gesamt.md  ← Telefonleitfaden
    │
    ├── ── MASTER-DATEN ─────────────────────────────
    │
    ├── ARM_Kampagne_Gesamtliste.csv       ← Master-Liste (1.759 Leads, bundesweit)
    ├── PROJEKTSTATUS_ARM_Kampagne.md       ← Projektstatus
    ├── PROJEKTSTATUS_GaLaBau_Kampagne.md   ← Status GaLaBau
    │
    ├── ── AP-RECHERCHE-ERGEBNISSE ────────────────────
    │
    ├── GaLaBau_Kommunen_Ansprechpartner_Recherche.csv
    ├── Kommunen_Recherche_Batch7.csv ... BatchG.csv
    ├── Tiefbau_GF_Recherche_Batch1-3.csv
    ├── GaLaBau_GF_Recherche_Batch_K-M.csv / N-Z.csv
    ├── Strassenbau_GF_Recherche_Batch_A-J.csv / K-Z.csv
    ├── Recherche Tiefbauunternehmen PLZ 0-9 durch claude.md
    ├── Recherche GaLaBau PLZ 0-9 durch claude.md
    │
    └── ── SCRIPTS ────────────────────────────────────
        ├── filter_adm_territories.py      ← ADM-Gebiete filtern + Export
        ├── integrate_recherche.py          ← Recherche-Integration
        ├── export_excel.py                 ← Excel-Export Script
        ├── convert_arm_to_crm.py           ← CRM-Konvertierung
        ├── generate_leadlist.py            ← Original Tiefbau-Script
        └── generate_galabau_leadlist.py    ← Original GaLaBau-Script
```

---

## Schnellstart für das Telefonteam

1. **Leitfaden lesen:** `Gespraechsleitfaden_ARM_Kampagne_Gesamt.md`
2. **Excel öffnen:** `ARM_ADM_Kampagne.xlsx` — eigenen Fachberater-Tab öffnen
3. **Farbcode:** Grün = A-Lead (Hot), Hellblau = B-Lead (Warm)
4. **Status-Spalte** rechts ausfüllen für Anruf-Tracking

---

## Technisches

- **Python 3** + `openpyxl` benötigt (`pip install openpyxl`)
- **ADM-Filter:** `python filter_adm_territories.py` — filtert auf 5 Fachberater-Gebiete, erzeugt CSV + Excel + CRM-Import
- **CRM-Import:** `ARM_ADM_CRM_Import.csv` (Salesforce-Format, Komma-Delimiter)
- **Recherche-Integration:** `python integrate_recherche.py` (alle Batch-CSVs → Hauptliste)
