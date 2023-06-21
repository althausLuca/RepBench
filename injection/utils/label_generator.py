import injection.injection_config as ic
import numpy as np

from injection.utils.injection_checks import anomaly_label_check


def get_anomaly_ranges(ts_class):
    in_anomaly = False
    ranges = []
    current_range = []
    for i, v in enumerate(ts_class):
        if v:
            in_anomaly = True
            current_range.append(i)
        if not v:
            if in_anomaly:
                in_anomaly = False
                ranges.append(current_range)
                current_range = []
    return [np.array(range_) for range_ in ranges]


def generate_df_labels(class_df, seed=None):

    label_df = class_df.copy()

    for (i, column) in enumerate(label_df):
        label_df[column] = generate_column_labels(class_df[column], seed=i + (0 if seed is None else seed))

    anomaly_label_check(label_df=label_df,class_df=class_df)
    return label_df


def generate_column_labels(class_column, seed=None):
    label_rate = ic.label_rate
    label_anom_start = ic.anomstartlabelrate
    state = np.random.get_state()
    np.random.seed(ic.label_seed + (seed if seed is not None else 0))
    labels = None


    max_iter = 10000
    for i in range(max_iter):
        m = len(class_column)
        r_number = np.random.uniform(size=m)
        r_number = r_number < label_rate
        labels = r_number.astype(bool)

        if np.any(class_column.astype(int)):
            labels_in_anomalies = labels[class_column]
            labeled_anoms = np.any(np.invert(labels_in_anomalies))
            non_labeled_anoms=  np.any(labels_in_anomalies)

            if (labeled_anoms and non_labeled_anoms):
                break
        else:
            #print("non anomalous column")
            break

    if  i >  max_iter - 2:
        raise ValueError(f" imr labeling failed {class_column}, anoms : {class_column.sum()} ")

    np.random.set_state(state)
    return labels
