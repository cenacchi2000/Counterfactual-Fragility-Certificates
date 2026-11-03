import itertools
from pathlib import Path
import sys
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reference import removal_path, graded_tests, affine_minimum_removals

class ReferenceChecks(unittest.TestCase):
    def test_affine_matches_exhaustive_subsets(self):
        rng = np.random.default_rng(42)
        for _ in range(150):
            weights = rng.normal(size=(3, 5)); bias = rng.normal(size=3)
            x = rng.normal(size=5); baseline = rng.normal(size=5)
            groups = [[0, 1], [2], [3], [4]]
            original = int(np.argmax(weights @ x + bias))
            expected = None
            for k in range(1, 5):
                for subset in itertools.combinations(range(4), k):
                    row = x.copy()
                    for g in subset: row[groups[g]] = baseline[groups[g]]
                    if int(np.argmax(weights @ row + bias)) != original:
                        expected = k; break
                if expected is not None: break
            found = affine_minimum_removals(weights, bias, x, baseline, groups)
            self.assertEqual(None if found is None else found['depth'], expected)
            if found:
                row = x.copy()
                for g in found['groups']: row[groups[g]] = baseline[groups[g]]
                self.assertNotEqual(int(np.argmax(weights @ row + bias)), original)
    def test_recomputation_changes_second_choice(self):
        # Full-row one-step order starts a,b,c. After a, b has no effect; c wins.
        def scores(row):
            a, b, c = row
            value = 5*a + 4*a*b + 3*c
            return np.array([value, -1.])
        path = removal_path(scores, np.ones(3), np.zeros(3), [[0], [1], [2]])
        self.assertEqual([r['removed'] for r in path[1:]], [0, 2, 1])
    def test_all_groups_receive_each_severity(self):
        records = graded_tests(lambda x: np.array([x.sum(), 0]), np.ones(3), np.zeros(3), [[0], [1], [2]])
        self.assertEqual(len(records), 15)
    def test_affine_class_tie_rule(self):
        weights = np.array([[0.], [1.]])
        result = affine_minimum_removals(weights, np.zeros(2), np.ones(1), np.zeros(1), [[0]])
        self.assertEqual(result['depth'], 1)
