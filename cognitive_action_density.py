"""Calculate the proposed Cognitive Action Density prompt heuristic."""

from collections.abc import Sequence
import math


LATENT_THOUGHT_BUDGET = 5000.0
W_A = 0.5
W_C = 0.3
W_S = 0.2

EXAMPLE_PROMPT_VECTORS = {
    "VAGUE_QUERY": (0.3, 0.2, 0.1, 0.1, 0.1, 0.9),
    "MEP_QUERY_HIGH_LOAD": (0.9, 0.9, 0.7, 0.8, 1.0, 0.5),
    "FORMAL_ESSAY_TASK": (0.7, 0.8, 0.5, 0.6, 0.4, 0.8),
}


def calculate_cognitive_action_density(
    p_vector: Sequence[float],
    l_tau: float = LATENT_THOUGHT_BUDGET,
) -> tuple[float, float, float]:
    """Return ``(C_AD, A_out, E_comp)`` for a normalized six-value vector.

    The vector order is ``[P_C, P_S, P_D, P_lambda, P_A, P_Sigma]``.
    All components must be finite and in ``[0, 1]``; ``P_Sigma`` and ``l_tau``
    must be greater than zero.
    """
    if len(p_vector) != 6:
        raise ValueError("p_vector must contain exactly six components")

    components = tuple(p_vector)
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0 <= value <= 1
        or not math.isfinite(value)
        for value in components
    ):
        raise ValueError("all vector components must be finite numbers in [0, 1]")

    if isinstance(l_tau, bool) or not isinstance(l_tau, (int, float)):
        raise ValueError("l_tau must be a positive finite number")
    try:
        l_tau = float(l_tau)
    except OverflowError:
        raise ValueError("l_tau must be a positive finite number") from None
    if not math.isfinite(l_tau) or l_tau <= 0:
        raise ValueError("l_tau must be a positive finite number")

    p_c, p_s, p_d, p_lambda, p_a, p_sigma = components
    if p_sigma == 0:
        raise ValueError("P_Sigma must be greater than zero")

    a_out = W_A * p_a + W_C * p_c + W_S * p_s
    e_comp = l_tau * (1 + math.sqrt(p_d) * p_lambda) / p_sigma
    c_ad = a_out / e_comp
    return c_ad, a_out, e_comp


if __name__ == "__main__":
    print(f"Theoretical Promptology Analysis (L_tau={LATENT_THOUGHT_BUDGET})\n")
    for name, vector in EXAMPLE_PROMPT_VECTORS.items():
        c_ad, a_out, e_comp = calculate_cognitive_action_density(vector)
        print(f"--- {name} ---")
        print(f"P Vector: {list(vector)}")
        print(f"Action Output (A_out): {a_out:.4f}")
        print(f"Comp Cost (E_comp): {e_comp:.2f}")
        print(f"Cognitive Action Density (C_AD): {c_ad:.8f}")
        print("-" * 20)
