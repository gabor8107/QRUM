"""No external testing library: python -m unittest discover -s tests -v."""
import contextlib
import io
from pathlib import Path
import runpy
import unittest

import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / "QRUM_OpticalClock_Synthetic_Benchmark_v2.2.py"


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            cls.vars = runpy.run_path(str(SCRIPT))
        cls.stdout = buffer.getvalue()

    def test_preregistered_demo_values(self):
        v = self.vars
        self.assertEqual(v["SEED"], 20261027)
        self.assertEqual(v["FREQUENCY_HZ"], 0.01)
        self.assertEqual(v["DT_S"], 1.0)
        self.assertEqual(v["N"], 10000)
        self.assertEqual(v["NSIM_NULL"], 2000)
        self.assertEqual(v["NSIM_INJECTED"], 1000)
        np.testing.assert_allclose(v["DK"], [0.5, 1.5], rtol=0, atol=1e-12)

    def test_amplitudes_and_nonaliasing(self):
        v = self.vars
        np.testing.assert_allclose(np.abs(v["DK"]) * v["G_INJECTED"], [1e-17, 3e-17], rtol=1e-12)
        self.assertLess(v["FREQUENCY_HZ"], 0.5 / v["DT_S"])

    def test_covariance_and_unbiased_gls_projection(self):
        v = self.vars
        s = v["SIGMA_INDIVIDUAL_CLOCK"]
        np.testing.assert_allclose(v["C_ratio"] / s**2, [[2., 1.], [1., 2.]], atol=1e-12)
        np.testing.assert_allclose(v["ratio_weights"] @ v["DK"], 1.0, atol=1e-12)
        self.assertGreater(v["noise_std_of_projection"], 0.)

    def test_deterministic_recovery(self):
        v = self.vars
        self.assertAlmostEqual(v["fitted_g"] / 1e-17, 2.060, delta=0.001)
        self.assertAlmostEqual(v["fitted_phase"], 0.7010, delta=0.001)
        self.assertEqual(v["recovery_power"], 1.)

    def test_null_threshold_near_analytic_gaussian_expectation(self):
        v = self.vars
        # With sinusoid quadratures and orthogonal sampling, fitted null amplitudes
        # have Rayleigh scale sigma_g = sigma_projected * sqrt(2/N).
        scale = v["noise_std_of_projection"] * np.sqrt(2. / v["N"])
        analytic_q99 = scale * np.sqrt(-2. * np.log(0.01))
        self.assertAlmostEqual(v["threshold"] / analytic_q99, 1.0, delta=0.10)
        self.assertAlmostEqual(v["threshold"] / 1e-18, 3.869, delta=0.003)

    def test_no_physical_detection_claim(self):
        self.assertIn("NOT measured results", self.stdout)
        self.assertIn("No experimental upper limit or QRUM constraint", self.stdout)


if __name__ == "__main__":
    unittest.main()
