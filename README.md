# Lantern Tide

Lantern Tide is a static, frontend-only prototype for a short cozy village game. The player walks around Harborwake, talks with villagers, notices objects, and helps prepare for a lantern festival. Choices and route behavior update an internal evidence vector that is reduced into a short end-of-route play profile.

This is an exploratory prototype, not a diagnostic tool and not a validated GQ-ASC administration.

## Run Locally

```bash
node server.js
```

Open `http://127.0.0.1:4173/`.

For phone testing on the same network:

```bash
HOST=0.0.0.0 PORT=4173 node server.js
```

Then open `http://<machine-ip>:4173/` on the phone.

`mobile_preview.html` is a desktop phone-frame preview.

## Test

```bash
node --check app.js
node scenario_runner.js
```

`scenario_runner.js` executes the hidden scenario checks, scripted playthroughs, simulated player profiles, and content audit. A clean run has no `auditIssues` and no failed checks.

## Main Files

- `index.html` - page shell and dialogue/profile containers.
- `styles.css` - layout, responsive behavior, dialogue tray, and visual UI styling.
- `app.js` - game state, canvas rendering, interactions, scoring, summary, and hidden scenario checks.
- `scenario_runner.js` - Node-based regression harness for scoring and content consistency.
- `server.js` - tiny no-cache static server for local testing.
- `mobile_preview.html` - iframe wrapper for checking a phone-sized viewport.
- `DESIGN.md` - current developer rationale and implementation notes.
- `GQ_ASC_ADULT_WOMEN_REFERENCE.md` - source-alignment notes for the adult-women GQ-ASC paper/form.

## Public Demo

The public demo is deployed as static files to GitHub Pages:

https://sergei-dev-to.github.io/Projects/

Keep the public URL clean. If browser caching becomes a problem, update the internal `?build=` asset tags in `index.html`, not the page URL.
