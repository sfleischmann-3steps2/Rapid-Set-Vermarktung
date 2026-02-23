# ARM Kampagne - Projektstatus

**Stand: 23. Februar 2026 (aktualisiert)**
**Kampagne:** "Kaufe 2 Paletten (2x48 Sack), davon 24 Sack ohne Berechnung! Laufzeit: Ende März (Option Ende April)."

---

## Zusammenfassung

| Kennzahl | Wert |
|----------|------|
| **Leads gesamt** | **1081** (nach Deduplizierung, 1120 roh aus 10 Regionen) |
| **A-Leads** (sofort anrufen) | **416** |
| **B-Leads** (zweite Welle) | **458** |
| **C-Leads** (optional) | **207** |
| **Regionen abgeschlossen** | **10 von 10** (alle PLZ-Regionen komplett!) |
| **Regionen in Arbeit** | 0 |
| **Regionen offen** | 0 |

---

## Status pro PLZ-Region

### Abgeschlossen (Report + high_relevance_names fertig, Script-Lauf ausstehend)

| Region | Gebiet | Leads (roh) | Report-Datei |
|--------|--------|-------------|--------------|
| PLZ 9 | Bayern / Thüringen | ~90 | `Recherche Tiefbauunternehmen PLZ 9 durch claude.md` |
| PLZ 0 | Sachsen / Sachsen-Anhalt / Thüringen | ~70 | `Recherche Tiefbauunternehmen PLZ 0 durch claude.md` |
| PLZ 8 | Bayern Süd (Oberbayern/Schwaben) | ~80 | `Recherche Tiefbauunternehmen PLZ 8 durch claude.md` |
| PLZ 6 | Hessen / Saarland / Rhein-Neckar | ~91 | `Recherche Tiefbauunternehmen PLZ 6 durch claude.md` |
| PLZ 7 | Baden-Württemberg | ~94 | `Recherche Tiefbauunternehmen PLZ 7 durch claude.md` |
| PLZ 5 | Köln / Bonn / Aachen / Koblenz / Trier | ~106 | `Recherche Tiefbauunternehmen PLZ 5 durch claude.md` |
| PLZ 2 | Hamburg / SH / Nds Nord / Bremen | ~100 | `Recherche Tiefbauunternehmen PLZ 2 durch claude.md` |

### Zuletzt abgeschlossen

| Region | Gebiet | Leads (roh) | Report-Datei |
|--------|--------|-------------|--------------|
| PLZ 4 | NRW Ruhrgebiet / Münsterland / Niederrhein | ~106 | `Recherche Tiefbauunternehmen PLZ 4 durch claude.md` |
| PLZ 1 | Berlin / Brandenburg / Mecklenburg-Vorpommern | ~133 | `Recherche Tiefbauunternehmen PLZ 1 durch claude.md` |
| PLZ 3 | Hannover / Braunschweig / Kassel / Göttingen / Magdeburg | ~162 | `Recherche Tiefbauunternehmen PLZ 3 durch claude.md` |

---

## Output-Dateien

| Datei | Beschreibung | Aktuell |
|-------|-------------|---------|
| `ARM_CRM_Import_Leads.csv` | Salesforce Lead-Import (UTF-8-BOM, Semikolon) | 1081 Leads (10 Regionen) |
| `ARM_Anrufliste_Priorisiert.csv` | Sortiert A→B→C für Telefonteam | 1081 Leads (10 Regionen) |
| `ARM_Leadliste_Komplett.xlsx` | Excel mit Tabs: Übersicht, A-Leads, B-Leads, C-Leads | 1081 Leads (10 Regionen) |
| `generate_leadlist.py` | Reproduzierbares Python-Script | Alle 10 Regionen konfiguriert + high_relevance_names |

---

## Workflow pro Region (Standardprozess)

1. **PLZ-Region konfigurieren** in `generate_leadlist.py`:
   - `PLZ_REGIONS` Dict-Eintrag
   - `detect_bundesland()` Mapping
2. **4 parallele Recherche-Agenten** starten:
   - Kommunale Tiefbauämter / Bauhöfe
   - Staatliche Straßenbaubehörden
   - Private Straßenbauunternehmen
   - Ingenieurbüros Straßenbau
3. **Markdown-Report** erstellen: `Recherche Tiefbauunternehmen PLZ X durch claude.md`
4. **high_relevance_names** ergänzen (regionale Spezialisten für A-Lead-Scoring)
5. **Script ausführen** → Output-Dateien aktualisieren

---

## Priorisierungs-Logik (A/B/C Scoring)

### A-Leads (sofort anrufen)
- Kommunale Tiefbauämter/Bauhöfe mit Telefon + E-Mail
- Kleine/mittlere Straßenbauer mit Fokus Instandsetzung
- Firmen aus der `high_relevance_names`-Liste

### B-Leads (zweite Welle)
- Größere private Bauunternehmen (Max Bögl, STRABAG etc.)
- Staatliche Bauämter (längere Beschaffungswege)
- Kommunen ohne vollständige Kontaktdaten

### C-Leads (optional/nachgelagert)
- Ingenieurbüros (indirekte Empfehlung)
- Autobahn GmbH (formale Beschaffung)
- Einträge ohne verwertbare Kontaktdaten

---

## Offene Aufgaben

### Kurzfristig (erledigt)
- [x] PLZ 5 Report fertigstellen (106 Einträge)
- [x] PLZ 2 Report fertigstellen (100 Einträge)
- [x] high_relevance_names für PLZ 5 ergänzen (16 Spezialisten)
- [x] high_relevance_names für PLZ 2 ergänzen (18 Spezialisten)
- [x] PLZ 4 recherchieren (NRW - Ruhrgebiet, 106 Einträge)
- [x] high_relevance_names für PLZ 4 ergänzen (26 Spezialisten)
- [x] PLZ 1 recherchieren (Berlin/Brandenburg/MV, 133 Einträge)
- [x] high_relevance_names für PLZ 1 ergänzen (24 Spezialisten)
- [x] PLZ 3 recherchieren (Hannover/Braunschweig/Kassel/Magdeburg, 162 Einträge)
- [x] high_relevance_names für PLZ 3 ergänzen (28 Spezialisten)
- [x] detect_bundesland() erweitert (MV, Berlin/Brandenburg getrennt, Sachsen-Anhalt PLZ 39, Hessen PLZ 36)
- [x] Script ausführen → 1081 Leads (416 A / 458 B / 207 C) aus allen 10 Regionen

### Optional / Verbesserungen
- [ ] Kontaktdaten-Verifikation (Stichproben telefonisch prüfen)
- [x] Ergänzung fehlender Ansprechpartner über Web-Recherche → 17 Kommunen + 1 Firma recherchiert (update_ansprechpartner.py)
- [x] Gesprächsleitfaden für Telefonteam erstellen → `Gespraechsleitfaden_ARM_Kampagne.md`
- [ ] Follow-up-Tracking in CRM einrichten

---

## Technische Hinweise

- **Python 3** + `openpyxl` benötigt für Excel-Export
- **Script-Aufruf:** `python generate_leadlist.py` im Ordner `Recherche Interessenten/`
- **Deduplizierung:** Stadtbasiert für Kommunen, namensbasiert mit Aliassen für Private
- **CRM-Format:** UTF-8-BOM, Semikolon-Delimiter, kompatibel mit Salesforce
