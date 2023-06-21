import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from repair import algorithms_config as ac
from injection.injectedDataContainer import InjectedDataContainer


def plot_data_part(data_part : InjectedDataContainer, path , file_name):
    injected_cols = data_part.injected_columns
    full_truth, full_injected = data_part.truth, data_part.injected
    axis = plt.gca()
    axis.set_rasterization_zorder(0)
    axis.set_title(f'{data_part.name}')

    n,m = full_injected.shape

    labels : np.array = data_part.labels.iloc[:,injected_cols].values
    truth = full_truth.iloc[:,injected_cols].values
    injected = full_injected.iloc[:,injected_cols].values


    mask = (injected != truth).astype(int)
    mask[1:] += mask[:-1]
    mask[:-1] += mask[1:]
    mask = np.invert(mask.astype(bool))
    masked_injected = np.ma.masked_where(mask, injected)

    non_label_mask = np.invert(labels.astype(bool))
    masked_labeled_truth = np.ma.masked_where(non_label_mask, truth)



    plt_ret = plt.plot(masked_injected, color="red", ls='--', marker=".", label="injected")
    line,*_= plt_ret

    lw = plt.getp(line, 'linewidth')
    plt.plot(truth, color="black", lw=lw, label="truth")

    add_labels = lambda : plt.plot(masked_labeled_truth, color="green", lw=0, label="labels", marker="." , ms = lw)

    axis.xaxis.set_major_locator(MaxNLocator(integer=True))

    for repair_name , repair  in data_part.repairs.items():
        alg_type = repair["type"]
        assert alg_type  in ac.ALGORITHM_TYPES
        if alg_type == ac.IMR:
            add_labels()
        repair_values = repair["repair"].iloc[:,injected_cols].values
        color = ac.ALGORITHM_COLORS[alg_type]
        n,m = truth.shape
        repair_mask = repair_values == truth
        repair_mask = repair_mask & np.roll(repair_mask,-1,axis=0) & np.roll(repair_mask,1,axis=0)
        lines = plt.plot(np.ma.masked_where(repair_mask,repair_values) , color = color ,label=repair_name +f"{sum(repair_values != truth)/(n*m)}")
        plt.legend()
        plt.savefig(path + "/" + file_name)
        l = lines.pop(0)
        l.remove()

    from pathlib import Path
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.savefig(path+"/" +file_name)
    plt.close('all')

