import json
import numpy as np
from reference import removal_path, graded_tests, affine_minimum_removals
weights = np.array([[1., 1., .2], [0., 0., 0.]])
bias = np.array([-.5, 0.])
x = np.array([1., 1., 1.])
baseline = np.zeros(3)
groups = [[0], [1], [2]]
scores = lambda row: weights @ row + bias
print(json.dumps({"recomputed_path": removal_path(scores, x, baseline, groups),
                  "attenuation_tests": graded_tests(scores, x, baseline, groups),
                  "affine_minimum": affine_minimum_removals(weights, bias, x, baseline, groups)}, indent=2))
