#
#
#
# def split_data_set(df, split=0.5):
#     split = int(len(df[df.columns[0]]) * split)
#     train, test = df.iloc[:split, :], df.iloc[split:, :]
#     return train.copy(), test.copy()
#
# def split_data_dict(data_dict , split = 0.5):
#     train_dict = {}
#     test_dict  = {}
#
#     for name , df in data_dict.items():
#         train_dict[name] , test_dict[name] = split_data_set(df,split)
#
#     return train_dict, test_dict
#
#
