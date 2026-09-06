# Wo wir stehen — Stand 6. September 2026

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

1. ~~Logo SV Straßlach~~ **erledigt.** Liegt als
   `assets/img/logo-sv-strasslach.png` und ist in `engagement.html` eingebaut.

2. ~~Kundenlogos B2B~~ **erledigt.** Elf Logos liegen in `assets/img/clients/`
   und stehen in `b2b.html` — in derselben Reihenfolge wie im Karussell der
   alten Seite. Die Kachel „und viele weitere" steht weiterhin am Ende.

   **Offen dabei:** ein zwölftes Logo — eine pink-orange gestreifte Kugel ohne
   Schriftzug — konnte keiner Firma zugeordnet werden. Es liegt als
   `assets/img/clients/unbekannt-globus.png` bereit; sobald der Name feststeht,
   Datei umbenennen und in `b2b.html` als weitere `<li>` einfügen (Kommentar
   steht dort).

   *Hinweis zum SMS-Logo:* der Schriftzug „STADT MARKT STARNBERG" ist in der
   Originaldatei weiß und deshalb auf der weißen Kachel kaum zu sehen — auf der
   alten Wix-Seite war das genauso. Falls störend, bei der Stadt eine Version mit
   dunklem Schriftzug anfragen.

   *So kamen die Logos doch noch von Wix* (die frühere Notiz „geht nicht" war
   falsch): das Karussell ist kein Wix-Widget, sondern ein selbst geschriebenes
   HTML-Embed. Dessen Adresse steht in der Seiten-JSON von Wix:

   ```
   # 1. Seiten-JSON-Dateinamen aus dem HTML der Live-Seite lesen
   curl -s https://www.ebsb.de/b2b | grep -o '"pageUriSEO":"[^"]*","pageJsonFileName":"[^"]*"'
   # 2. die zugehörige siteassets.parastorage.com/pages/pages/thunderbolt?…-URL
   #    aus demselben HTML holen (module=thunderbolt-features, pageId=<datei>.json)
   # 3. darin steht die Embed-URL:
   curl -s https://www-ebsb-de.filesusr.com/html/40a34f_56a8d6e2867c81cd79311fec172becda.html
   ```

   In derselben JSON stecken auch alle übrigen Bilder (`"uri"`) und die
   Vektorgrafiken (`"svgId"` → `https://static.wixstatic.com/shapes/<id>.svg`).
   Darüber sind u. a. das EBSB-Logo und das Special-Olympics-Logo als SVG
   verfügbar, falls die PNG-Fassungen einmal zu grob wirken.

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
