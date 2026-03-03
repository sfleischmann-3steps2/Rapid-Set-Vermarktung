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

## Übersicht (Stand: 02.03.2026)

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
    ├── ARM_ADM_CRM_Import_v2.csv          ← Salesforce-Import (340 Leads, 173 mit Straße) ✔ erfolgreich
    ├── ARM_ADM_Gesamtliste_enriched.csv   ← Quelldaten + Straße + Adresse_Status
    ├── ARM_ADM_Gesamtliste.csv            ← Original-Basisdaten (340 Leads, ohne Straße)
    ├── ARM_ADM_Kampagne.xlsx              ← Excel: Übersicht + 5 Fachberater-Tabs
    ├── Verkaufsgebiete_ARM.md             ← PLZ → Fachberater Zuordnungstabelle
    ├── Gespraechsleitfaden_ARM_Kampagne_Gesamt.md  ← Telefonleitfaden
    │
    ├── ── MASTER-DATEN ─────────────────────────────
    │
    ├── ARM_Kampagne_Gesamtliste.csv       ← Master-Liste (1.759 Leads, bundesweit)
    ├── PROJEKTSTATUS_ARM_Kampagne.md       ← Projektstatus
    │
    └── ── SCRIPTS ────────────────────────────────────
        ├── convert_arm_to_crm.py           ← CRM-Konvertierung (enriched → Salesforce-Format)
        ├── enrich_addresses.py             ← Impressum-Scraping → Straßenadresse
        ├── filter_adm_territories.py       ← ADM-Gebiete filtern + Export
        └── export_excel.py                 ← Excel-Export Script
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
- **ADM-Filter:** `python filter_adm_territories.py` — filtert auf 5 Fachberater-Gebiete, erzeugt CSV + Excel
- **Adress-Anreicherung:** `python enrich_addresses.py` — scrapet Straßenadressen via Impressum (resume-fähig via Checkpoint). Fehlende Adressen danach manuell in `ARM_ADM_Gesamtliste_enriched.csv` nachtragen.
- **CRM-Import:** `python convert_arm_to_crm.py` → `ARM_ADM_CRM_Import_v2.csv` (Salesforce-Format, Komma-Delimiter, UTF-8 BOM). Liest automatisch enriched CSV wenn vorhanden.

---

## Salesforce Lead-Import: Learnings

Beim ersten Import (v1) sind alle 340 Leads fehlgeschlagen. Folgende Regeln gelten für künftige Imports:

### 1. Kein Industry-Feld / IBS_SC_Branchen__c
Das Salesforce-Feld `IBS_SC_Branchen__c` ist eine **eingeschränkte Auswahlliste**. Standard-Werte wie `"Construction"` oder `"Government"` werden abgelehnt. **Lösung:** Industry-Spalte komplett weglassen — das Feld wird in Salesforce manuell oder per Automation gesetzt.

### 2. City max. 40 Zeichen
Salesforce beschränkt das City-Feld auf **40 Zeichen**. Bei kommunalen Leads darf der Behördenname (z.B. "Fachbereich Tiefbau und Verkehr") **nicht** im City-Feld stehen, sondern gehört ins Company-Feld. `convert_arm_to_crm.py` erledigt das automatisch.

### 3. Encoding: UTF-8 mit BOM
Salesforce + Excel brauchen **UTF-8 mit BOM** (`utf-8-sig`) für korrekte Umlaute (ä, ö, ü, ß).

### 4. Spaltenformat
Komma-getrennt (Standard-CSV), **nicht** Semikolon. Salesforce-Standard-Feldnamen verwenden (`First Name`, `Last Name`, `Company`, `Street`, `City`, `Zip/Postal Code`, etc.).
