import os
import lib
import numpy as np
import pandas as pd

DATASETS = [
    "abalone",
    "adult",
    "buddy",
    "california",
    "cardio",
    "churn2",
    "default",
    "diabetes",
    "fb-comments",
    "gesture",
    "higgs-small",
    "house",
    "insurance",
    "king",
    "miniboone",
    "wilt"
]

_REGRESSION = [
    "abalone",
    "california",
    "fb-comments",
    "house",
    "insurance",
    "king",
]


method2exp = {
    "real": "exp/{}/ddpm_cb_best/",
    "tab-ddpm": "exp/{}/ddpm_cb_best/",
    "smote": "exp/{}/smote/",
    "ctabgan+": "exp/{}/ctabgan-plus/",
    "ctabgan": "exp/{}/ctabgan/",
    "tvae": "exp/{}/tvae/"
}

eval_file = "eval_catboost.json"
show_std = False
df = pd.DataFrame(columns=["method"] + [_[:3].upper() for _ in DATASETS])

for algo in method2exp: 
    algo_res = []
    for ds in DATASETS:
        if not os.path.exists(os.path.join(method2exp[algo].format(ds), eval_file)):
            algo_res.append("--")
            continue
        metric = "r2" if ds in _REGRESSION else "f1"
        res_dict = lib.load_json(os.path.join(method2exp[algo].format(ds), eval_file))

        if algo == "real":
            res = f'{res_dict["real"]["test"][metric + "-mean"]:.4f}' 
            if show_std: res += f'+-{res_dict["real"]["test"][metric + "-std"]:.4f}'
        else:
            res = f'{res_dict["synthetic"]["test"][metric + "-mean"]:.4f}'
            if show_std: res += f'+-{res_dict["synthetic"]["test"][metric + "-std"]:.4f}'

        algo_res.append(res)
    df.loc[len(df)] = [algo] + algo_res

df.to_csv("agg_results.csv", index=False)