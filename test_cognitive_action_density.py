import math
import unittest

from cognitive_action_density import (
    EXAMPLE_PROMPT_VECTORS,
    calculate_cognitive_action_density,
)


class CalculateCognitiveActionDensityTests(unittest.TestCase):
    def test_example_vectors_return_finite_metrics(self):
        for vector in EXAMPLE_PROMPT_VECTORS.values():
            with self.subTest(vector=vector):
                c_ad, a_out, e_comp = calculate_cognitive_action_density(vector)
                self.assertTrue(math.isfinite(c_ad))
                self.assertGreaterEqual(a_out, 0)
                self.assertGreater(e_comp, 0)

    def test_calculates_expected_values(self):
        c_ad, a_out, e_comp = calculate_cognitive_action_density(
            (0.3, 0.2, 0.1, 0.1, 0.1, 0.9), l_tau=10
        )
        self.assertAlmostEqual(a_out, 0.18)
        self.assertAlmostEqual(e_comp, 10 * (1 + math.sqrt(0.1) * 0.1) / 0.9)
        self.assertAlmostEqual(c_ad, a_out / e_comp)

    def test_rejects_vector_with_wrong_length(self):
        with self.assertRaisesRegex(ValueError, "exactly six"):
            calculate_cognitive_action_density((0.1,) * 5)

    def test_rejects_zero_semantic_mass(self):
        with self.assertRaisesRegex(ValueError, "P_Sigma"):
            calculate_cognitive_action_density((0.1, 0.1, 0.1, 0.1, 0.1, 0))

    def test_rejects_out_of_range_and_non_finite_components(self):
        for value in (-0.1, 1.1, math.nan, math.inf, 10**1000):
            vector = (0.1, 0.1, 0.1, 0.1, 0.1, value)
            with self.subTest(value=value), self.assertRaisesRegex(
                ValueError, "components"
            ):
                calculate_cognitive_action_density(vector)

    def test_rejects_non_positive_or_non_finite_budget(self):
        for budget in (0, -1, math.nan, math.inf, 10**1000):
            with self.subTest(budget=budget), self.assertRaisesRegex(
                ValueError, "l_tau"
            ):
                calculate_cognitive_action_density((0.1,) * 6, l_tau=budget)


if __name__ == "__main__":
    unittest.main()
