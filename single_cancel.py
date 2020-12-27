from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from datasets import *
from utils import *

# Initialization
dataset = Dataset("./data")
cancel_x, cancel_y, test_cancel_x = dataset.get_cancel_data()
groups = np.array(dataset.get_groups("train"))

models = [LogisticRegression(penalty="l1", solver="liblinear", random_state=0, max_iter=1e+8, tol=1e-6),
        LogisticRegression(max_iter=1e+8, tol=1e-6),
        Pipeline([("feature_selection", SelectFromModel(LogisticRegression(penalty="l1", solver="liblinear", \
                                                                random_state=0, max_iter=1e+8, tol=1e-6))), \
                        ("classifier", LogisticRegression(max_iter=1e+8, tol=1e-6))])
]

params = [{"C": [1e+2, 1e+1, 1, 1e-1]},
        {"C": [1e+2, 1e+1, 1, 1e-1]},
        {"feature_selection__estimator__C": [1e+2, 1e+1, 1, 1e-1], \
            "classifier__C": [1e+2, 1e+1, 1, 1e-1]}
]

# Start grid search
for model, params_ in zip(models, params):
    print(model, flush=True)
    cv = GroupTimeSeriesSplit(n_splits=5).split(cancel_x, groups=groups, select_splits=[2], return_group_i=False)
    clf = GridSearchCV(model, params_, cv=cv).fit(cancel_x, cancel_y)
    print(clf.best_score_, clf.best_params, flush=True)
    print('\n')