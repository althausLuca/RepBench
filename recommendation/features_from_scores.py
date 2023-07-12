import os
import sys
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.feature_extraction.load_features import compute_features

mode = "train"
data_folder = f"data/recommendation/{mode}"
load_file_path = f"recommendation/results/scores/scores_{mode}"
store_path = "recommendation/results/features"
store_file_name = f"features_{mode}"


compute_features(load_filename=load_file_path,
                 store_filename=f"{store_path}/{store_file_name}",
                 data_folder= data_folder)


