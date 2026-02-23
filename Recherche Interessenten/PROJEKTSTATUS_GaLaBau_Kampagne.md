# ARM GaLaBau Kampagne - Projektstatus

**Stand: 23. Februar 2026 (aktualisiert)**
**Kampagne:** "Kaufe 2 Paletten (2x48 Sack), davon 24 Sack ohne Berechnung! Laufzeit: Ende März (Option Ende April)."
**Zielgruppe:** Garten- und Landschaftsbauunternehmen (GaLaBau)

---

## Zusammenfassung

| Kennzahl | Wert |
|----------|------|
| **Leads gesamt** | **728** (nach Deduplizierung, 739 roh aus 10 Regionen) |
| **A-Leads** (sofort anrufen) | **278** |
| **B-Leads** (zweite Welle) | **233** |
| **C-Leads** (optional) | **217** |
| **Regionen abgeschlossen** | **10 von 10** (alle PLZ-Regionen komplett!) |
| **Regionen in Arbeit** | 0 |
| **Regionen offen** | 0 |

---

## Status pro PLZ-Region

### Abgeschlossen

| Region | Gebiet | Leads (roh) | Report-Datei |
|--------|--------|-------------|--------------|
| PLZ 9 | Bayern / Thüringen | 78 | `Recherche GaLaBau PLZ 9 durch claude.md` |
| PLZ 8 | Bayern Süd (Oberbayern/Schwaben) | 63 | `Recherche GaLaBau PLZ 8 durch claude.md` |
| PLZ 7 | Baden-Württemberg | 68 | `Recherche GaLaBau PLZ 7 durch claude.md` |
| PLZ 6 | Hessen / Saarland / Rhein-Neckar | 66 | `Recherche GaLaBau PLZ 6 durch claude.md` |
| PLZ 5 | Köln / Bonn / Aachen / Koblenz / Trier | 72 | `Recherche GaLaBau PLZ 5 durch claude.md` |
| PLZ 4 | NRW Ruhrgebiet / Münsterland / Niederrhein | 90 | `Recherche GaLaBau PLZ 4 durch claude.md` |
| PLZ 3 | Hannover / Braunschweig / Kassel / Göttingen / Magdeburg | 80 | `Recherche GaLaBau PLZ 3 durch claude.md` |
| PLZ 2 | Hamburg / SH / Nds Nord / Bremen | 75 | `Recherche GaLaBau PLZ 2 durch claude.md` |
| PLZ 1 | Berlin / Brandenburg / Mecklenburg-Vorpommern | 81 | `Recherche GaLaBau PLZ 1 durch claude.md` |
| PLZ 0 | Sachsen / Sachsen-Anhalt / Thüringen | 66 | `Recherche GaLaBau PLZ 0 durch claude.md` |

---

## Output-Dateien

| Datei | Beschreibung | Aktuell |
|-------|-------------|---------|
| `GaLaBau_CRM_Import_Leads.csv` | Salesforce Lead-Import (UTF-8-BOM, Semikolon) | 728 Leads (10 Regionen) |
| `GaLaBau_Anrufliste_Priorisiert.csv` | Sortiert A→B→C für Telefonteam | 728 Leads (10 Regionen) |
| `GaLaBau_Leadliste_Komplett.xlsx` | Excel mit Tabs: Übersicht, A-Leads, B-Leads, C-Leads | 728 Leads (10 Regionen) |
| `generate_galabau_leadlist.py` | Reproduzierbares Python-Script | Alle 10 Regionen konfiguriert + high_relevance_names |
| `Gespraechsleitfaden_ARM_GaLaBau_Kampagne.md` | Telefonleitfaden GaLaBau-Zielgruppe | Erstellt |

---

## Workflow pro Region (Standardprozess)

1. **4 Recherche-Kategorien** pro Region:
   - Kommunale Grünflächenämter / Gartenämter
   - Landesbetriebe / Staatliche Gartenverwaltungen
   - Private GaLaBau-Betriebe
   - Landschaftsarchitekten / Planungsbüros
2. **Markdown-Report** erstellen: `Recherche GaLaBau PLZ X durch claude.md`
3. **high_relevance_names** ergänzen (regionale GaLaBau-Spezialisten für A-Lead-Scoring)
4. **Script ausführen** → Output-Dateien aktualisieren

---

## Priorisierungs-Logik (A/B/C Scoring — GaLaBau-angepasst)

### A-Leads (sofort anrufen)
- Kommunale Grünflächenämter mit Telefon + E-Mail
- Kleine/mittlere GaLaBau-Betriebe mit Fokus Wegebau/Pflaster
- Firmen aus der `high_relevance_names`-Liste

### B-Leads (zweite Welle)
- Größere GaLaBau-Ketten (längere Entscheidungswege)
- Staatliche Gartenverwaltungen (formale Beschaffung)
- Kommunen ohne vollständige Kontaktdaten

### C-Leads (optional/nachgelagert)
- Landschaftsarchitekten (indirekte Empfehlung)
- Einträge ohne verwertbare Kontaktdaten

---

## Erledigt

- [x] Script `generate_galabau_leadlist.py` erstellt
- [x] Gesprächsleitfaden GaLaBau erstellt (`Gespraechsleitfaden_ARM_GaLaBau_Kampagne.md`)
- [x] Projektstatus-Datei erstellt
- [x] PLZ 9 Report (Bayern/Thüringen) — 78 Einträge
- [x] PLZ 8 Report (Bayern Süd) — 63 Einträge
- [x] PLZ 7 Report (Baden-Württemberg) — 68 Einträge
- [x] PLZ 6 Report (Hessen/Saarland/Rhein-Neckar) — 66 Einträge
- [x] PLZ 5 Report (Köln/Bonn/Aachen/Koblenz/Trier) — 72 Einträge
- [x] PLZ 4 Report (NRW Ruhrgebiet/Münsterland/Niederrhein) — 90 Einträge
- [x] PLZ 3 Report (Hannover/Braunschweig/Kassel/Göttingen/Magdeburg) — 80 Einträge
- [x] PLZ 2 Report (Hamburg/SH/Nds Nord/Bremen) — 75 Einträge
- [x] PLZ 1 Report (Berlin/Brandenburg/MV) — 81 Einträge
- [x] PLZ 0 Report (Sachsen/Sachsen-Anhalt/Thüringen) — 66 Einträge
- [x] high_relevance_names pro Region ergänzt
- [x] Script ausgeführt → 728 Leads (278 A / 233 B / 217 C) aus allen 10 Regionen

## Optional / Verbesserungen

- [ ] Kontaktdaten-Verifikation (Stichproben telefonisch prüfen)
- [ ] Ergänzung fehlender Ansprechpartner über Web-Recherche
- [ ] Follow-up-Tracking in CRM einrichten

---

## Technische Hinweise

- **Python 3** + `openpyxl` benötigt für Excel-Export
- **Script-Aufruf:** `python generate_galabau_leadlist.py` im Ordner `Recherche Interessenten/`
- **Deduplizierung:** Stadtbasiert für Kommunen, namensbasiert für Private
- **CRM-Format:** UTF-8-BOM, Semikolon-Delimiter, kompatibel mit Salesforce

---

## Vergleich mit Tiefbau-Kampagne

| | Tiefbau | GaLaBau |
|---|---------|---------|
| **Leads gesamt** | 1.081 | 728 |
| **A-Leads** | 416 | 278 |
| **B-Leads** | 458 | 233 |
| **C-Leads** | 207 | 217 |
| **Zielgruppe** | Tiefbauämter, Straßenbauer | Grünflächenämter, GaLaBau-Betriebe |
| **Use-Case** | Schlaglöcher, Straßenschäden | Wege, Einfahrten, Terrassen, Parkplätze |
| **Kategorien** | Kommune/Behörde/Privat/Ing.-Büro | Kommune/Behörde/Privat GaLaBau/Landschaftsarchitekt |
| **Script** | `generate_leadlist.py` | `generate_galabau_leadlist.py` |
| **Beide Kampagnen zusammen** | | **1.809 Leads** |
