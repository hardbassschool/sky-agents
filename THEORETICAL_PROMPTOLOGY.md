# Theoretical Promptology: A Proposed Framework

## Abstract

Theoretical Promptology (TP) is a proposed framework for describing prompt
construction as a constrained optimization problem. It represents a prompt
with a six-component state vector and defines Cognitive Action Density
(C_AD) as a heuristic ratio of useful action output to modeled computational
cost. This document formalizes the proposal and states its assumptions; the
metric is not an empirically validated measure of model inference or answer
quality.

## Prompt state

Represent a prompt by

`P = [P_C, P_S, P_D, P_lambda, P_A, P_Sigma]`,

where each component is normalized to `[0, 1]`:

| Component | Meaning |
| --- | --- |
| `P_C` | Complexity: structural and logical load of the requested work. |
| `P_S` | Specificity: how precisely the request defines its boundaries. |
| `P_D` | Context depth: how much relevant prior or supplied context is needed. |
| `P_lambda` | Constraint density: the load imposed by simultaneous constraints. |
| `P_A` | Aspiration: the requested degree of novelty or synthesis. |
| `P_Sigma` | Semantic mass: the useful information carried by the prompt, relative to its wording. |

These dimensions are conceptual ratings, not quantities a program can infer
reliably from text without an independently defined measurement procedure.
In particular, semantic mass is not simply token count.

## Proposed objective

For a positive latent-thought budget `L_tau`, define useful action output and
modeled cost as

```text
A_out = 0.5 P_A + 0.3 P_C + 0.2 P_S
E_comp = L_tau (1 + sqrt(P_D) P_lambda) / P_Sigma
C_AD = A_out / E_comp
```

The objective is to maximize `C_AD`, subject to producing an answer that
satisfies the user's actual goals and constraints. A zero `P_Sigma` is
undefined under this model and must be rejected. The budget is an arbitrary
positive scale factor: it changes the numerical value of C_AD, not the ranking
of prompts under a common budget.

## Interpretation and limitations

The equations encode hypotheses, not established laws. The weights and cost
function are illustrative; the model does not observe a language model's
internal computation, predict answer quality, or show that a vague prompt is
preferable. The components can trade off, and ratings may be subjective.
Consequently, C_AD is useful here for making assumptions explicit and
comparing example ratings, not as a standalone score for prompt quality or
system performance.

Validation would require operational definitions for each component,
independent raters or reproducible measurements, and experiments comparing
predicted scores with outcomes such as task success, user satisfaction, and
measured inference cost across models and task types. The proposed prompt
engine, prompt-entropy model, and failure predictor are future research
directions, not capabilities implemented by this prototype. There is also a
numerical mismatch in the motivating examples: with the supplied vectors,
weights, and `L_tau = 5000`, the scores are approximately `0.00003141` for
`VAGUE_QUERY`, `0.00005691` for `MEP_QUERY_HIGH_LOAD`, and `0.00006403` for
`FORMAL_ESSAY_TASK`. Thus the vague query has the lowest score, not the highest
as the original observation claims. The calculator reports the formula's
results without assuming the claimed ranking.
