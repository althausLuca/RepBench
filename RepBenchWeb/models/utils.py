score_map = {"mae": "MAE",
             "mse": "MSE",
             "rmse": "RMSE",
             "partial_rmse": "RMSE on Anomaly"
             }


def granularity_to_time_interval(granularity):
    """
    Converts a time granularity string to a time interval in seconds.

    The time granularity string should be a string of the form "NUNIT", where N is a positive integer
    and UNIT is one of the following characters: 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days),
    or 'w' (weeks). For example, '10m' means a granularity of 10 minutes.

    If the time granularity string is not in the correct format or cannot be parsed, the function returns
    a default time interval of 1 hour.

    Returns:
    -------
    int:
        The time interval in seconds corresponding to the given time granularity string.
    """

    s = 1
    m = 60 * s
    h = 60 * m
    d = 24 * h
    w = 7 * d



    try:
        unit = granularity[-1]  # s,m,h,d,w
        amount = granularity[:-1]
    except:
        return h

    if granularity.endswith("ms"):
        unit = "ms"
        amount = granularity[:-2]

    gran_dict = {
        "s": s,
        "m": m,
        "h": h,
        "d": d,
        "w": w,
        "ms" : s/1000
    }

    if amount == "":
        amount = "1"
    amount = int(amount)

    return amount * gran_dict[unit]

