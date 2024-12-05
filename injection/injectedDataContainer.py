import numpy as np

from injection.utils.injection_checks import anomaly_check, anomaly_label_check, index_check
from injection.utils.label_generator import generate_df_labels
import hashlib
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class InjectedDataContainer:
    def __init__(self, injected, truth, *, class_df=None, labels, name="injected_container" , is_checked=False):
        assert injected.shape == truth.shape

        self.truth_ = truth  # contains the Original Series
        self.injected_ = injected
        self.labels_ = labels
        self.repairs = {}
        self.repair_metrics = {}
        self.repair_names = []
        self.name = name
        self.relabeled = 0
        if not is_checked:
            self.check = lambda: None

        if class_df is None:
            class_df = pd.DataFrame(np.invert(np.isclose(injected, truth))).reindex_like(truth)
        self.class_df = class_df
        self.injected_columns = [i for i, v in enumerate(class_df.any(axis=0).values) if v]
        self.check()

    @property
    def repair_inputs(self):
        self.check()
        return {"injected": self.injected,
                "truth": self.truth,
                "labels": self.labels,
                "columns_to_repair": self.injected_columns.copy(),
                }


    def get_normalized_version(self):
        mean , std = self.injected.mean() , self.injected.std()
        normalized_injected = (self.injected - mean) / std
        normalized_truth = (self.truth - mean) / std

        return InjectedDataContainer(injected=normalized_injected,truth=normalized_truth,
                                        class_df=self.class_df,labels=self.labels,name=self.name)


    def check(self):
        index_check(self.klass, self.injected, self.truth, self.labels_)
        anomaly_check(self.klass, self.injected, self.truth)
        anomaly_label_check(class_df=self.class_df, label_df=self.labels_)

    def __repr__(self):
        return f"{self.name}"

    @property
    def truth(self):
        return self.truth_.copy()

    @property
    def injected(self):
        return self.injected_.copy()

    def get_none_filled_injected(self):
        injected = self.injected.copy()
        for col in self.injected.columns:
            # convolve over class df setting each entry next to a true entry to true
            class_col = self.class_df[col].values
            class_col = np.convolve(class_col, [1, 1, 1], mode="same") > 0
            injected.loc[~class_col, col] = np.nan
        return injected

    @property
    def klass(self):
        return self.class_df.copy()

    @property
    def labels(self):
        self.check()
        return self.labels_.copy()

    @property
    def labels_rate(self):
        return self.labels_.iloc[:, self.injected_columns].mean().mean()

    @property
    def a_perc(self):
        return np.mean(self.klass.iloc[:, self.injected_columns].values)

    @property
    def injected_columns_names(self):
        return self.injected.columns[self.injected_columns]

    def add_repair(self, repair_results, repair_type, repair_name=None):
        self.check()
        repair_name = repair_type if repair_name is None else repair_name
        self.repair_names.append(repair_name)
        assert repair_name not in self.repairs, f" {repair_name} already in {self.repairs.keys()}"
        f"such a repair already exists:{repair_name}"

        repair = repair_results["repair"]
        assert repair.shape == self.labels.shape, (
            repair_name, repair.shape, self.labels.shape, self.truth.shape, self.injected.shape)

        repair_dict = {
            "repair": repair_results["repair"],
            "name": repair_name,
            "type": repair_type,
            "parameters": repair_results["params"]
        }

        self.repairs[repair_name] = repair_dict

        repair_metrics = repair_results["scores"]
        repair_metrics["runtime"] = repair_results["runtime"]
        self.repair_metrics[(repair_name, repair_type)] = repair_metrics

    def hash(self, additional_input=""):
        m = hashlib.md5(self.injected.values.flatten())
        m.update(self.labels.values.flatten())
        m.update(additional_input.encode())
        result = m.hexdigest()
        return result

    @property
    def original_scores(self):
        from repair.estimator import Estimator
        return Estimator().scores(self.injected, self.truth, self.injected_columns, self.labels,
                                  predicted=self.injected)

    def get_a_rate_per_col(self, rounding=3):
        result = {}
        cols = self.injected.columns
        for col in cols:
            result[col] = round(np.mean(self.class_df[col].values), rounding)
        return result

    def get_n_anomalies_per_col(self):
        result = {}
        cols = self.injected.columns
        for col in cols:
            result[col] = np.sum(np.diff(self.class_df[col].values.astype(int)) > 0)
        return result

    @property
    def truth_corr(self):
        return self.truth_.corr()

    @property
    def injected_corr(self):
        return self.injected_.corr()

    def randomize_labels(self):
        self.check()
        self.relabeled += 1
        self.labels_ = generate_df_labels(self.class_, seed=self.relabeled)
        self.check()

    def set_to_original_scale(self, mean, std):
        self.injected_ = self.injected_ * std + mean
        self.truth_ = self.truth_ * std + mean
        close = np.isclose(self.truth.values, self.injected.values)
        assert np.allclose(~close, self.class_df.values)

    # dump to json
    def to_json(self):
        import json
        result = {
            "name": self.name,
            "truth": self.truth.to_json(),
            "injected": self.injected.to_json(),
            "labels": self.labels.to_json(),
            "class_df": self.class_df.to_json(),
            "repairs": {k: v.to_json() for k, v in self.repairs.items()},
            "repair_metrics": self.repair_metrics,
            "repair_names": self.repair_names,
        }
        return json.dumps(result)

    @staticmethod
    def from_json(json_string):
        import json
        result = json.loads(json_string)
        return InjectedDataContainer(
            injected=pd.read_json(result["injected"]),
            truth=pd.read_json(result["truth"]),
            labels=pd.read_json(result["labels"]),
            class_df=pd.read_json(result["class_df"]),
            name=result["name"],
        )

    def save(self, folder="data"):
        import os
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.truth.to_csv(f"{folder}/{self.name}_truth.csv")
        self.injected.to_csv(f"{folder}/{self.name}_injected.csv")
        # self.labels.to_csv(f"{folder}/{self.name}_labels.csv")
        self.class_df.to_csv(f"{folder}/{self.name}_class_df.csv")
        # dict to csv
        import csv
        with open(f"{folder}/{self.name}_repairs.csv", 'w') as f:
            w = csv.writer(f)
            # w.writerows(self.repairs.items())
            for key, value in self.repairs.items():
                if isinstance(value, pd.DataFrame):
                    f.write(value.to_string(index=False))  # Write full DataFrame as a string
                else:
                    w.writerow([key, value])
            w.writerow('\n')

    def plot(self, injected_ts_only=True, show=True):
        return plot_injected_container(self, injected_ts_only, show)


def plot_injected_container(injected_container: InjectedDataContainer, injected_ts_only=True, show=True):
    import matplotlib.pyplot as plt
    plt.plot(injected_container.injected.iloc[:500, injected_container.injected_columns].values, color="red")
    plt.plot(injected_container.truth.iloc[:500, injected_container.injected_columns].values)
    plt.title(f"{injected_container.name} injected { { ts: rate for ts,rate in injected_container.get_a_rate_per_col().items() if rate > 0.0 }}")

    plt.show()
