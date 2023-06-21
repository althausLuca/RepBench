import numpy as np
from pandas import DataFrame

#set directory to project root

def index_check(*dfs):
    df : DataFrame
    dfs[0] : DataFrame
    for df in dfs[1:]:
        assert dfs[0].index.equals(df.index)

def anomaly_check(class_df,injected_df,truth_df):
    for column in truth_df:
        ### labeled differ
        class_col = class_df[column]
        c = np.isclose(injected_df[column][class_col] ,  truth_df[column][class_col],rtol=0.001)

        assert not np.any(c) , "as injected labeled values are to close to be considered an anomaly"
        ### non labeled do not differ
        all_close = np.allclose(injected_df[column][np.invert(class_col)] ,  truth_df[column][np.invert(class_col)])
        assert all_close , "non marked entries do differ"



def anomaly_label_check(class_df,label_df):
     ### labeled anomalies
     for column in class_df:
         class_values = class_df[column].values
         label_values = label_df[column].values
         if np.any(class_values):
            labels_in_anomalies = label_values[class_values]
            #class_in_labels = np.where(label_values,class_values)
            assert np.any(labels_in_anomalies)  #, [(l,c) for l,c in zip(label_values,class_values)]
            assert np.any(np.invert(labels_in_anomalies))





