# Failure case logging template

Use this template for notable behavioral or latent-space anomalies.

## Case ID
- `fc_YYYYMMDD_<short_name>`

## Run metadata
- run_name:
- model_name:
- config_snapshot:
- generation_file:
- activation_file:

## Scenario
- task_type:
- variant_type:
- prompt_type(s):
- example_id / pair_id:

## Observed behavior
- parsed answers by prompt:
- expected synthetic label:
- key output snippets:

## Representation observations
- layers with largest drift:
- drift metric used:
- contrast type (prompt-pair / original-vs-variant):

## Hypotheses (tentative)
- possible superficial cues:
- possible prompt-framing sensitivity:
- alternative explanations:

## Follow-up experiment plan
- targeted config changes:
- additional controls:
- what would falsify current interpretation:

## Confidence statement
- confidence level:
- major uncertainties:
