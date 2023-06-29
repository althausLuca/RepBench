default_set = "BAFU"

data_sets_info = {
    "BAFU": {
        "title": "BAFU",
        "path": "train/bafu5k.csv",
        "ref_url": "https://www.bafu.admin.ch/bafu/en/home.html",
        "url_text":"Federal Office for the Environment",
        "description" : "Measurement of the water level in different rivers in Switzerland",
        "granularity": "1d"
    },
    "Humidity": {
        "title": "Humidity",
        "path": "train/humidity.csv",
        "ref_url": "https://www.meteoswiss.admin.ch/",
        "url_text" : "MeteoSwiss",
        "description": "Humidity in different cities",
        "granularity" : "1h"
    },
    "SMD": {
        "title": "Server Machine Dataset",
        "path": "train/smd1_5.csv",
        "ref_url": "https://github.com/NetManAIOps/OmniAnomaly",
        "url_text": "Omni Anomaly",
        "description": "Measurement of different metrics like  the CPU and memory usage of a server machine",
        "granularity": "1s"

    },
    "Electricity": {
        "title": "Electricity",
        "path": "train/elec.csv",
        "ref_url": "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014",
        "url_text": "UCI Machine Learning Repository",
        "granularity": "1d"

    },

    "MotorImagery_finger": {
        "title": "Tiny",
        "path": "train/MotorImagery_finger.csv",
        "ref_url": "https://timeseriesclassification.com/description.php?Dataset=MotorImagery",
        "url_text": "UCI classification Repository",
        "description": "Imagined movements of the left small finger.",
        "granularity": "1ms"
    },

    "MotorImagery_tongue": {
        "title": "Tiny",
        "path": "train/MotorImagery_tongue.csv",
        "ref_url": "https://timeseriesclassification.com/description.php?Dataset=MotorImagery",
        "url_text": "UCI classification Repository",
        "description": "Imagined movements of the tongue.",
        "granularity": "1ms"

    },
    "Cricket": { ## cricket 1 dataset
        "title": "Cricket",
        "path": "train/Cricket.csv",
        "ref_url": "https://timeseriesclassification.com/description.php?Dataset=ArticularyWordRecognition",
        "url_text": "UCI classification Repository",
        "description": """Cricket requires an umpire to signal different events in the game to a distant scorer/bookkeeper.
         The signals are communicated with motions of the hands.""",
        "granularity": "5ms"
    },
    "Tiny": {
        "title": "Tiny",
        "path": "train/tiny.csv",
        "ref_url": "-",
        "url_text": "",
        "description": "test data",
    },
}
