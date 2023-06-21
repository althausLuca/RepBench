import os
import numpy as np
import pandas as pd
import json
from json2html import *

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py


file_paths = "recommendation/automl_files"
result_file = "flaml_classifier_accuracy_time_10_5_results.json"


with open(f'{file_paths}/{"flaml_classifier_accuracy_time_30_results.json"}', "r") as json_file:
    json_str = json.load(json_file)
    conf_array= json_str["train"]["confusion_matrix"]
    train_mat_html = pd.DataFrame(np.array(conf_array)).to_html().replace("\n","")
    json_str["train"]["confusion_matrix"] = "train_math_html"

    conf_array_test = json_str["test"]["confusion_matrix"]
    test_mat_html = pd.DataFrame(np.array(conf_array_test)).to_html().replace("\n","")
    json_str["test"]["confusion_matrix"] = "test_math_html"

html = json2html.convert(json = json_str)\
    .replace("train_math_html",train_mat_html)\
   .replace("test_math_html",test_mat_html)\
    .replace("\n","<br>")

import webbrowser
import os

f = open('class_results.html', 'w')

f.write(html)

# close the file
f.close()

# 1st method how to open html files in chrome using
filename = 'file:///' + os.getcwd() + '/' + 'GFG.html'
webbrowser.open_new_tab(filename)

os.rmdir(filename)


