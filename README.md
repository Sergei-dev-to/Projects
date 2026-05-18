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
node construct_audit.js
node adversarial_benchmark.js
node summary_review.js
node scenario_runner.js
```

`scenario_runner.js` executes the hidden scenario checks, scripted playthroughs, simulated player profiles, and content audit. A clean run has no `auditIssues` and no failed checks.

`construct_audit.js` writes `CONSTRUCT_AUDIT.md`, which checks which source constructs the playable choices actually touch. `adversarial_benchmark.js` writes `ADVERSARIAL_BENCHMARK.md`, which checks that common confounds such as social anxiety, sensory-only load, novelty seeking, and completionism do not become higher ASD-axis profiles by themselves.

`summary_review.js` writes `SUMMARY_REVIEW.md`, which previews the end-of-day wording for synthetic player profiles.

The harness also includes route-order reliability checks and confound simulations. These are regression tests for the prototype, not validation of the assessment.

## Main Files

- `index.html` - page shell and dialogue/profile containers.
- `styles.css` - layout, responsive behavior, dialogue tray, and visual UI styling.
- `app.js` - game state, canvas rendering, interactions, scoring, summary, and hidden scenario checks.
- `scenario_runner.js` - Node-based regression harness for scoring and content consistency.
- `construct_audit.js` - construct coverage report for the playable interaction set.
- `adversarial_benchmark.js` - false-positive benchmark for scoring confounds.
- `summary_review.js` - synthetic end-summary wording review.
- `server.js` - tiny no-cache static server for local testing.
- `mobile_preview.html` - iframe wrapper for checking a phone-sized viewport.
- `DESIGN.md` - current developer rationale and implementation notes.
- `GQ_ASC_ADULT_WOMEN_REFERENCE.md` - source-alignment notes for the adult-women GQ-ASC paper/form.
- `VALIDATION_PLAN.md` - practical validation path and minimum study checks.
- `CALIBRATION.md` - record format and offline calibration workflow.
- `PILOT_STUDY.md` - lightweight protocol for collecting first paired records.
- `calibration_runner.js` - Node-based runner for fitting/checking weights against comparator data.
- `PUBLIC_DATA.md` - public AQ-10 proxy-data workflow and female-presentation gap notes.
- `public_data_prior.js` - adapter that maps UCI adult AQ-10 data into Lantern Tide's source domains.

## Assessment Notes

The current assessment target is a play-based reflection of adult-women autism-trait domains. The game keeps source-domain coverage separate from the scalar range, records explicit confound guards, and exposes an `assessmentRecord()` shape in `app.js` for future calibration work.

The ending reflection can copy or download a game record. Pair those records with a separate normalized comparator score and run:

```bash
node calibration_runner.js validation-records.jsonl
```

That produces calibration diagnostics and suggested ridge-regression weights. It is a tuning aid, not validation by itself.

For pilot collection, use the collapsed `Pilot study export` panel in the ending reflection and follow `PILOT_STUDY.md`.

To dry-run the pipeline with synthetic routes:

```bash
node pilot_dry_run.js
node calibration_runner.js validation-records.dry-run.jsonl
```

This writes `validation-records.dry-run.jsonl` and should produce an explicit overfitting warning because five synthetic records are too few for fitted weights.

To stress-test the pipeline with a larger seeded synthetic population:

```bash
node synthetic_population.js 1000 validation-records.synthetic.jsonl 1729
node calibration_runner.js validation-records.synthetic.jsonl
```

Synthetic records test the calibration machinery under known artificial assumptions. They do not validate the game.

To generate the public-data proxy prior from the UCI Adult Autism Screening dataset after downloading/unpacking it:

```bash
node public_data_prior.js data/uci_autism_adult/Autism-Adult-Data.arff calibration_prior.public.json
```

The derived prior is useful as a weak adult AQ-10 anchor. `PUBLIC_DATA.md` documents why this still leaves the adult-female presentation gap open.

## Public Demo

The public demo is deployed as static files to GitHub Pages:

https://sergei-dev-to.github.io/Projects/

Keep the public URL and asset URLs clean. For local testing, use `server.js`, which sends no-cache headers so the latest files appear without query-string build tags.
