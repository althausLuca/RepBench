import numpy as np


encodings = {}

def encode(y:np.array):
    len_encodings = len(encodings)
    for i,label in enumerate(set(y)):
        if label not in encodings:
            encodings[label] = i+len_encodings
    return np.array([encodings[label] for label in y])

def get_reverse_mapping():
    return {v:k for k,v in encodings.items()}

def decode(y_or_int):
    if isinstance(y_or_int, int) or isinstance(y_or_int, np.int64):
        if y_or_int in encodings:
            return y_or_int
        return get_reverse_mapping()[y_or_int]
    else:
        return [get_reverse_mapping()[i] for i in y_or_int]
