#!/usr/bin/env python3
"""
Anreicherung der ARM_ADM_Gesamtliste.csv mit Straßenadressen via Impressum-Scraping.

Extraktions-Strategie je Seite (in Priorität):
  1. JSON-LD (schema.org PostalAddress) — am zuverlässigsten
  2. <address> HTML-Tag
  3. PLZ-Kontext-Suche (Regex) — Fallback

URL-Kandidaten je Domain:
  - /impressum, /impressum.html, /impressum/
  - /kontakt, /kontakt.html, /kontakt/
  - /ueber-uns, /about
  - /datenschutz (enthält oft auch Adresse)
  - Kommunen: /rathaus/impressum, /service/impressum, /verwaltung/impressum
  - HTTP-Fallback für ältere Sites
  - Root-URL als letzter Versuch

CLI-Flags:
  --retry-failed   Setzt alle not_found im Checkpoint zurück → werden neu gescrapt
"""

import csv
import re
import json
import time
import os
import sys
import io
import html
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste_enriched.csv")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "enrich_checkpoint.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.5",
}

REQUEST_TIMEOUT = 10
RATE_LIMIT_DELAY = 1.0

# Generische E-Mail-Provider ohne Firmenwebsite → überspringen
GENERIC_PROVIDERS = {
    "t-online.de", "gmail.com", "googlemail.com",
    "gmx.de", "gmx.net", "gmx.at", "gmx.ch",
    "web.de", "yahoo.de", "yahoo.com",
    "hotmail.com", "hotmail.de", "outlook.com", "outlook.de",
    "freenet.de", "arcor.de", "icloud.com", "me.com",
    "live.de", "live.com", "aol.com", "aol.de",
}

# Straßen-Regex (keine generischen Ortsbestandteile wie berg, hof, markt)
STREET_PATTERN = re.compile(
    r"[A-ZÄÖÜ][a-zäöüß\-]+(?:straße|str\.|weg|gasse|allee|platz|ring|damm|chaussee|promenade|ufer|graben)\s+\d+[a-zA-Z]?",
    re.IGNORECASE,
)

# "Am/An der/Im/In der + Name + Hausnummer" z.B. "Am Markt 3"
STREET_PATTERN_AM = re.compile(
    r"\b(?:Am|An der|An den|Im|In der|In den|Auf dem|Auf der|Zum|Zur)\s+[A-ZÄÖÜ][a-zäöüß\-]+\s+\d+[a-zA-Z]?",
    re.IGNORECASE,
)

PLZ_PATTERN = re.compile(r"\b(\d{5})\b")


# ── Hilfsfunktionen ──────────────────────────────────────────────────────────

def extract_domain(email: str) -> str:
    email = email.strip().lower()
    if "@" not in email:
        return ""
    return email.split("@", 1)[1].strip()


def is_generic_provider(domain: str) -> bool:
    return domain in GENERIC_PROVIDERS


def fetch_url(url: str) -> str | None:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            content_type = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            ct_match = re.search(r"charset=([^\s;]+)", content_type)
            if ct_match:
                charset = ct_match.group(1).strip().strip('"')
            raw = resp.read()
            try:
                return raw.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                return raw.decode("utf-8", errors="replace")
    except (HTTPError, URLError, OSError):
        return None
    except Exception:
        return None


# ── Extraktions-Methoden ─────────────────────────────────────────────────────

def extract_json_ld_address(raw_html: str, plz: str) -> str:
    """
    Sucht schema.org PostalAddress in JSON-LD Blöcken.
    Gibt 'streetAddress' zurück wenn PLZ passt, sonst "".
    """
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        raw_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for script in scripts:
        try:
            data = json.loads(script.strip())
        except (json.JSONDecodeError, ValueError):
            continue

        # Rekursiv nach PostalAddress suchen
        addresses = _find_postal_addresses(data)
        for addr in addresses:
            postal = str(addr.get("postalCode", "")).strip()
            street = str(addr.get("streetAddress", "")).strip()
            if street and (not plz or postal == plz or not postal):
                return street
    return ""


def _find_postal_addresses(obj, depth=0) -> list:
    """Rekursive Suche nach PostalAddress-Objekten im JSON-LD."""
    if depth > 6:
        return []
    results = []
    if isinstance(obj, dict):
        type_val = obj.get("@type", "")
        if isinstance(type_val, str) and "PostalAddress" in type_val:
            results.append(obj)
        elif isinstance(type_val, list) and any("PostalAddress" in t for t in type_val):
            results.append(obj)
        for v in obj.values():
            results.extend(_find_postal_addresses(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_find_postal_addresses(item, depth + 1))
    return results


def extract_address_tag(raw_html: str, plz: str) -> str:
    """
    Sucht <address>...</address> Tags und extrahiert Straße darin.
    """
    address_blocks = re.findall(
        r"<address[^>]*>(.*?)</address>",
        raw_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for block in address_blocks:
        text = html.unescape(re.sub(r"<[^>]+>", " ", block))
        text = re.sub(r"\s+", " ", text).strip()

        # PLZ-Validierung
        if plz and plz not in text:
            continue

        street = _extract_street_from_text(text)
        if street:
            return street
    return ""


def strip_html_tags(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_street_from_text(text: str) -> str:
    """Sucht Straßenmuster im Text, gibt ersten Treffer zurück."""
    m = STREET_PATTERN.search(text)
    if m:
        return m.group(0).strip()
    m = STREET_PATTERN_AM.search(text)
    if m:
        return m.group(0).strip()
    return ""


def find_address_in_text(text: str, plz: str) -> str:
    """Sucht Straße in der Nähe der bekannten PLZ (500 Zeichen Kontext)."""
    found_pos = -1
    for m in PLZ_PATTERN.finditer(text):
        if m.group(1) == plz:
            found_pos = m.start()
            break

    if found_pos == -1:
        return ""

    context_start = max(0, found_pos - 500)
    context = text[context_start: found_pos + 80]
    return _extract_street_from_text(context)


def extract_address(raw_html: str, plz: str) -> str:
    """
    Versucht alle Extraktionsmethoden in Priorität:
    1. JSON-LD  2. <address>-Tag  3. PLZ-Kontext
    """
    street = extract_json_ld_address(raw_html, plz)
    if street:
        return street

    street = extract_address_tag(raw_html, plz)
    if street:
        return street

    text = strip_html_tags(raw_html)
    return find_address_in_text(text, plz)


# ── URL-Kandidaten ────────────────────────────────────────────────────────────

def build_url_candidates(domain: str) -> list[str]:
    """URL-Kandidaten in Prioritätsreihenfolge."""
    # Basis-Pfade (allgemein)
    paths = [
        "/impressum",
        "/impressum.html",
        "/impressum/",
        "/kontakt",
        "/kontakt.html",
        "/kontakt/",
        "/ueber-uns",
        "/ueber-uns/",
        "/about",
        "/datenschutz",
        # Kommunen-typische Pfade
        "/rathaus/impressum",
        "/service/impressum",
        "/verwaltung/impressum",
        "/buergerservice/impressum",
        "/stadtinfo/impressum",
        "/de/impressum",
        "",  # Root
    ]

    candidates = []
    for path in paths:
        candidates.append(f"https://www.{domain}{path}")

    # https ohne www
    for path in ["/impressum", "/impressum.html", "/impressum/", ""]:
        candidates.append(f"https://{domain}{path}")

    # HTTP-Fallback (ältere Sites)
    for path in ["/impressum", "/impressum.html", ""]:
        candidates.append(f"http://www.{domain}{path}")
        candidates.append(f"http://{domain}{path}")

    # Deduplizieren, Reihenfolge beibehalten
    seen = set()
    result = []
    for url in candidates:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


# ── Haupt-Scraping ────────────────────────────────────────────────────────────

def scrape_address(email: str, plz: str) -> tuple[str, str]:
    domain = extract_domain(email)
    if not domain or is_generic_provider(domain):
        return "", "not_found"

    fetched_domains = set()

    for url in build_url_candidates(domain):
        # Nicht denselben Pfad zweimal holen (http/https Duplikate)
        url_key = re.sub(r"^https?://", "", url)
        if url_key in fetched_domains:
            continue
        fetched_domains.add(url_key)

        raw_html = fetch_url(url)
        if not raw_html:
            time.sleep(0.15)
            continue

        street = extract_address(raw_html, plz)
        time.sleep(RATE_LIMIT_DELAY)

        if street:
            return street, "found"

        time.sleep(0.2)

    return "", "not_found"


# ── Checkpoint ────────────────────────────────────────────────────────────────

def load_checkpoint() -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_checkpoint(checkpoint: dict) -> None:
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def reset_not_found(checkpoint: dict) -> int:
    """Setzt alle not_found-Einträge zurück. Gibt Anzahl zurück."""
    keys = [k for k, v in checkpoint.items() if v.get("status") == "not_found"]
    for k in keys:
        del checkpoint[k]
    return len(keys)


# ── Hauptlauf ─────────────────────────────────────────────────────────────────

def enrich(retry_failed: bool = False) -> None:
    checkpoint = load_checkpoint()

    if retry_failed:
        n = reset_not_found(checkpoint)
        save_checkpoint(checkpoint)
        print(f"--retry-failed: {n} not_found-Einträge zurückgesetzt → werden neu gescrapt")

    print(f"Checkpoint: {len(checkpoint)} bereits verarbeitet "
          f"({sum(1 for v in checkpoint.values() if v.get('status')=='found')} gefunden)")

    with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    print(f"Eingabe: {len(rows)} Zeilen aus {os.path.basename(INPUT_FILE)}")

    out_fieldnames = list(fieldnames) + ["Straße", "Adresse_Status"]
    found_count = 0
    not_found_count = 0
    total = len(rows)
    enriched_rows = []

    for i, row in enumerate(rows, start=1):
        email = row.get("Email", "").strip()
        plz = row.get("PLZ", "").strip()
        firma = row.get("Firma", "").strip()
        ck_key = email if email else f"row_{i}"

        if ck_key in checkpoint:
            cached = checkpoint[ck_key]
            straße = cached.get("straße", "")
            status = cached.get("status", "not_found")
            symbol = "✓" if status == "found" else "✗"
            print(f"  [{i:3d}/{total}] {symbol} [cache] {firma[:35]:<35} → {straße or '—'}")
        else:
            domain = extract_domain(email)
            skip = is_generic_provider(domain) if domain else True
            if skip and domain:
                print(f"  [{i:3d}/{total}] — [skip]  {firma[:35]:<35} ({domain})")
                straße, status = "", "not_found"
            else:
                print(f"  [{i:3d}/{total}]   [scrape] {firma[:35]:<35} ({email})", end="", flush=True)
                if not email or "@" not in email:
                    straße, status = "", "not_found"
                else:
                    straße, status = scrape_address(email, plz)
                symbol = "✓" if status == "found" else "✗"
                print(f"\r  [{i:3d}/{total}] {symbol} [scrape] {firma[:35]:<35} → {straße or '—'}")

            checkpoint[ck_key] = {"straße": straße, "status": status}
            save_checkpoint(checkpoint)

        if status == "found":
            found_count += 1
        else:
            not_found_count += 1

        enriched_row = dict(row)
        enriched_row["Straße"] = straße
        enriched_row["Adresse_Status"] = status
        enriched_rows.append(enriched_row)

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(enriched_rows)

    print()
    pct = found_count / total * 100 if total > 0 else 0
    print(f"✓  Gefunden:       {found_count:3d} / {total} ({pct:.0f}%)")
    print(f"✗  Nicht gefunden: {not_found_count:3d} / {total} ({100-pct:.0f}%)")
    print(f"→  Ausgabe: {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    retry = "--retry-failed" in sys.argv
    enrich(retry_failed=retry)
