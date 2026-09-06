# Wo wir stehen — Stand 5. September 2026

Die Seite ist fertig gebaut und getestet: 9 Seiten, alle Links geprüft, deutscher
Text wörtlich aus der alten Wix-Seite übernommen, responsive bis 375 px, keine
externen Requests. **Noch nicht online** — kein GitHub-Repo, DNS unverändert
(ebsb.de zeigt weiter auf Wix).

## Sofort weitermachen

```
cd "C:\Users\mathi\OneDrive\Documents\09_Cursor\EBSB website"
node scripts/serve.js 8080
```
→ http://localhost:8080

## Offen — inhaltlich

1. **Logo SV Straßlach** fehlt noch. Datei in `missing images/` legen, dann in
   `engagement.html` den `<div class="logo-slot">` durch das Bild ersetzen
   (die genaue Zeile steht als Kommentar direkt darüber).

2. **Kundenlogos B2B** („Auswahl unser Kunden"). Fünf Platzhalter-Kacheln in
   `b2b.html` warten. Logos nach `assets/img/clients/`, dann
   `<li class="empty">…</li>` ersetzen durch
   `<li><img src="assets/img/clients/NAME.png" alt="NAME" /></li>`.
   Die Kachel „und viele weitere" bleibt am Ende stehen.
   *Hinweis:* diese Logos ließen sich nicht von Wix laden — Wix baut die Galerie
   per JavaScript, die Bild-URLs stehen nicht im HTML.

3. **Datenschutzerklärung überarbeiten.** Der Text ist 1:1 von
   ebsb.de/datenschutz übernommen und beschreibt Google Analytics sowie
   Xing-/LinkedIn-/X-/Facebook-Plugins — **nichts davon existiert auf der neuen
   Seite**. Außerdem fehlt der Verantwortliche nach Art. 13 DSGVO.
   Vorschlag: Analytics- und Social-Abschnitte streichen, Verantwortlichen-Block
   an den Anfang. Wortlaut vorher abstimmen.

4. **Teamfotos gegenprüfen.** Die Zuordnung Foto → Name auf `team.html` wurde aus
   der DOM-Reihenfolge der Wix-Seite abgeleitet und ist plausibel, aber nicht
   bestätigt. Einmal durchsehen.

## Offen — technisch

5. **Kontaktformular scharf schalten.** Kostenlosen Access Key auf
   <https://web3forms.com> holen, dann an **zwei** Stellen eintragen:
   - `assets/js/main.js` → `const WEB3FORMS_KEY = "…"`
   - `kontakt.html` → `<input type="hidden" name="access_key" value="…">`

   Danach einmal echt absenden und prüfen, ob die Mail ankommt.
   Solange kein Key gesetzt ist, öffnet das Formular das Mailprogramm des
   Besuchers — es läuft also nie ins Leere.

6. **Online stellen.**
   ```
   git add -A
   git commit -m "…"
   gh repo create ebsb-website --private --source=. --push
   ```
   Dann im Repo: Settings → Pages → Branch `master`, Ordner `/`.
   `CNAME` enthält bereits `ebsb.de`.
   **DNS erst umstellen, wenn die Seite auf der Pages-Preview-URL geprüft ist** —
   damit geht ebsb.de von Wix weg.

## Gut zu wissen

- Header und Footer stehen in jeder Seite. Bearbeitet wird `index.html`, danach
  `python scripts/sync-chrome.py` — das kopiert sie in alle anderen Seiten.
- `missing images/` ist per `.gitignore` ausgenommen (Ablage, kein Seiteninhalt).
- `.raw/` enthält die Originaldownloads von Wix, ebenfalls ignoriert.
- Alle Bilder liegen als WebP + JPEG/PNG-Fallback vor. Neu erzeugen mit
  `python scripts/fetch-assets.py`.
