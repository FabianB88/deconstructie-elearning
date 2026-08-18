# Inhoud genereren

`build_course.py` is de bron van de cursusinhoud. Het schrijft de vijf
JSON-bestanden in `src/course/nl/` weg. Pas de tekst dus hier aan en niet
rechtstreeks in de JSON, anders raak je je wijziging kwijt bij de volgende run.

```bash
python tools/build_course.py
npx grunt build
```

Publiceren naar GitHub Pages:

```bash
rm -rf docs && cp -r build docs && touch docs/.nojekyll
git add -A && git commit -m "update" && git push
```

Voor Brightspace: zip de inhoud van `build/` (niet de map zelf) — `imsmanifest.xml`
moet in de root van het zipbestand staan.
