# GQ-ASC Adult Women Source Reference

Source reviewed:

- `GQ-ASC Modified for adult females` PDF, hosted by Tony Attwood: https://tonyattwood.com.au/wp-content/uploads/2023/08/GQ-ASC-Modified-for-adult-females-LATEST-calibri-1.pdf
- Brown, C. M., Attwood, T., Garnett, M., & Stokes, M. A. (2020). `Am I Autistic? Utility of the Girls Questionnaire for Autism Spectrum Condition as an Autism Assessment in Adult Women.` Autism in Adulthood, 2(3), 216-226. https://doi.org/10.1089/aut.2019.0054

This file is a developer reference, not a reproduction of the questionnaire. Do not copy the full item text into this repository unless licensing and permissions are clear.

## Instrument Structure

The source form uses a 4-point agree/disagree response scale and organizes retained items into five components:

- Imagination and play.
- Camouflaging.
- Sensory sensitivities.
- Socializing.
- Interests.

The linked form presents 21 retained items. The paper describes the modified adult-women analysis and reports that the five-component solution accounted for 40.40% of variance.

## Scoring Summary

The source form uses direct item response values, with specified reverse-scored items. The total score is compared to a threshold above 56, equivalent to a cutoff score of 57. The paper reports that this cutoff correctly identified 80.0% of cases in the study sample.

The paper also cautions that the total-score cutoff should be interpreted carefully because the instrument did not establish a higher-order unidimensional structure. That supports Lantern Tide's current choice to show a profile range rather than treating one number as definitive.

## Lantern Tide Alignment

| Source component | Lantern Tide status | Current implementation notes |
|---|---|---|
| Imagination and play | Weak / mostly missing | The game has fantasy setting and object play, but it does not currently measure fantasy, fiction interest, or childhood imaginative play. |
| Camouflaging | Partial | `masking_adaptation`, `social_monitoring_cost`, and observation-before-engagement choices cover some camouflaging-adjacent behavior. |
| Sensory sensitivities | Partial | `sensory_accumulation`, `regulation_dependency`, quiet spaces, bell load, comfort objects, and recovery loops cover some sensory-regulation behavior. |
| Socializing | Partial | Social approach, watching before joining, social fatigue/load, support requests, and repair-like routing are represented indirectly. |
| Interests | Partial but transformed | `focused_loop_depth`, `systemizing_structure`, `context_switch_friction`, and `novelty_breadth` cover focused/systemizing behavior, not the source's exact age-advanced or gender-nonstereotyped interest items. |

## Non-Alignment With Validated Scoring

Lantern Tide does not currently implement the source instrument's validated scoring:

- It does not present the 21 retained questionnaire items.
- It does not collect 4-point agree/disagree item responses.
- It does not reverse-score the source's specified items.
- It does not sum a source-equivalent total score.
- It does not use the validated cutoff as a player-facing score.
- It uses a behavioral evidence vector and hand-tuned projection instead.

Therefore the app must continue to describe itself as `GQ-ASC-inspired`, not as a GQ-ASC administration or validated GQ-ASC score.

## Design Implications

Useful changes if source alignment becomes a priority:

- Add an explicit optional questionnaire mode that presents licensed/source-approved items and calculates the original total separately.
- Add more play situations for imagination/play and interest content, because those source components are underrepresented in the current game.
- Keep behavioral play scoring separate from questionnaire scoring unless a validation study shows that the game trace predicts the source scores.
- Keep profile output and uncertainty visible; do not replace it with a single cutoff-based label.
