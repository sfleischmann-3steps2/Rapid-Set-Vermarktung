# ARM Kampagne - Projektstatus

**Stand: 24. Februar 2026**
**Kampagne:** "Kaufe 2 Paletten (2x48 Sack), davon 24 Sack ohne Berechnung! Laufzeit: Ende März (Option Ende April)."

---

## Zusammenfassung

| Kennzahl | Wert |
|----------|------|
| **Leads gesamt (dedupliziert)** | **1.705** |
| **A-Leads** | **621** |
| **davon Tier 1 (anrufbereit, AP+Telefon)** | **463** |
| **davon Tier 2 (ohne Ansprechpartner)** | **158** |
| **B-Leads** | **660** |
| **C-Leads** | **424** |
| **Ursprung** | 1.081 Tiefbau + 728 GaLaBau, zusammengeführt |

### AP-Abdeckung A-Leads

| Segment | A-Leads | Mit AP | Quote |
|---------|---------|--------|-------|
| Kommune (Bauhöfe/Straßenmeistereien) | 395 | 306 | **77%** |
| Privat (GaLaBau) | 139 | 119 | **86%** |
| Privat (Straßenbau) | 87 | 38 | **44%** |
| **Gesamt** | **621** | **463** | **75%** |

---

## Kampagnen-Dateien

### Hauptdateien (aktuell)

| Datei | Beschreibung |
|-------|-------------|
| `ARM_Kampagne_Leadliste.xlsx` | **Excel-Hauptdatei** mit 5 Tier-Tabs + Zusammenfassung |
| `ARM_Kampagne_Gesamtliste.csv` | CSV für CRM-Import (1.705 Leads, alle Kategorien) |
| `ARM_Tier1_Kampagnenbereit.csv` | Nur Tier 1 — 463 sofort anrufbare A-Leads |
| `Gespraechsleitfaden_ARM_Kampagne_Gesamt.md` | Telefonleitfaden für Tiefbau + GaLaBau |

### Excel-Tabs (ARM_Kampagne_Leadliste.xlsx)

| Tab | Inhalt | Leads |
|-----|--------|-------|
| Tier 1 Anrufbereit | A-Leads mit Ansprechpartner + Telefon | 463 |
| Tier 2 Kommunen o.AP | Kommunen ohne namentlichen AP (Bauhof anrufen) | 89 |
| Tier 2 Privat o.AP | Private Firmen ohne AP (meist Straßenbau) | 69 |
| B-Leads | Zweite Welle / E-Mail-Kampagne | 660 |
| C-Leads | Langfrist (Ingenieurbüros, Architekten) | 424 |
| Zusammenfassung | Statistik + Legende | — |

### Quelldaten (Original-Listen)

| Datei | Beschreibung |
|-------|-------------|
| `ARM_Anrufliste_Priorisiert.csv` | Original Tiefbau-Liste (1.081 Leads) |
| `GaLaBau_Anrufliste_Priorisiert.csv` | Original GaLaBau-Liste (728 Leads) |
| `ARM_CRM_Import_Leads.csv` | Salesforce Import Tiefbau |
| `GaLaBau_CRM_Import_Leads.csv` | Salesforce Import GaLaBau |

---

## Phase 1: Leadrecherche (abgeschlossen)

### Tiefbau-Kampagne (10 PLZ-Regionen)

| Region | Gebiet | Leads |
|--------|--------|-------|
| PLZ 0 | Sachsen / Sachsen-Anhalt / Thüringen | ~70 |
| PLZ 1 | Berlin / Brandenburg / Mecklenburg-Vorpommern | ~133 |
| PLZ 2 | Hamburg / SH / Nds Nord / Bremen | ~100 |
| PLZ 3 | Hannover / Braunschweig / Kassel / Magdeburg | ~162 |
| PLZ 4 | NRW Ruhrgebiet / Münsterland / Niederrhein | ~106 |
| PLZ 5 | Köln / Bonn / Aachen / Koblenz / Trier | ~106 |
| PLZ 6 | Hessen / Saarland / Rhein-Neckar | ~91 |
| PLZ 7 | Baden-Württemberg | ~94 |
| PLZ 8 | Bayern Süd (Oberbayern/Schwaben) | ~80 |
| PLZ 9 | Bayern / Thüringen | ~90 |

### GaLaBau-Kampagne (10 PLZ-Regionen)

Analog zur Tiefbau-Kampagne, 728 Leads aus allen PLZ-Regionen.

---

## Phase 2: Zusammenführung & AP-Recherche (abgeschlossen)

### Schritte

1. **Listen-Merge:** Tiefbau (1.081) + GaLaBau (728) zusammengeführt, nach PLZ+Ort dedupliziert → **1.705 unique Leads**
2. **B-Lead Bereinigung:** 234 als "Behörde" fehlklassifizierte Einträge korrigiert:
   - 39 → Privat (Straßenbau Konzern) — STRABAG, Eurovia, PORR etc.
   - 36 → Behörde (Landesbetrieb)
   - 49 → Behörde (Landkreis)
   - 114 → Privat (Straßenbau)
   - 33 → Kommune
3. **AP-Recherche Kommune** (8 Batches, ~330 Kommunen recherchiert):
   - Runde 1: 95/116 GaLaBau-Kommunen → Bauhofleiter gefunden
   - Batch A-C: 68/104 weitere Kommunen
   - Batch D-G: 83/115 Tiefbau-Kommunen
   - **Ergebnis: 306 von 395 Kommune-A-Leads mit AP (77%)**
4. **AP-Recherche GaLaBau** (2 Batches, 85 Firmen):
   - GF/Inhaber über Impressum, Handelsregister, Northdata
   - **Ergebnis: 119 von 139 GaLaBau-A-Leads mit AP (86%)**
5. **AP-Recherche Straßenbau** (5 Batches, 144 Firmen):
   - Massive Datenqualitätsprobleme: ~30 Firmen aufgelöst, ~10 falsche Standorte, ~5 falsche Branche
   - **Ergebnis: 38 von 87 Straßenbau-A-Leads mit AP (44%)**

### Bekannte Datenqualitätsprobleme (Straßenbau)

Die Tiefbau-Ursprungsliste enthält zahlreiche veraltete Firmennamen:
- Nachwendegründungen in Ostdeutschland (aufgelöst/insolvent)
- Niederlassungen ohne eigene Web-Präsenz (NL statt Hauptsitz)
- Falsche Branchenzuordnung (z.B. August Brötje = Heizungshersteller)
- Für ~49 nicht auffindbare Firmen empfiehlt sich manuelle Prüfung via handelsregister.de

---

## Offene Aufgaben

- [ ] Kontaktdaten-Verifikation (Stichproben telefonisch prüfen)
- [ ] Tier 2 Kommunen (89): Telefonisch Bauhofleiter erfragen
- [ ] Straßenbau-Firmenliste bereinigen (nicht-existente Firmen entfernen/ersetzen)
- [ ] Follow-up-Tracking in CRM einrichten
- [ ] B-Lead E-Mail-Kampagne vorbereiten

---

## Technische Hinweise

- **Python 3** + `openpyxl` benötigt (`pip install openpyxl`)
- **Excel-Export:** `python export_excel.py`
- **Recherche-Integration:** `python integrate_recherche.py` (alle Batch-CSVs → Hauptliste)
- **CRM-Format:** UTF-8-BOM, Semikolon-Delimiter, Salesforce-kompatibel
