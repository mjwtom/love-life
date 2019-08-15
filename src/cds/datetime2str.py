from datetime import datetime


def str2datetime(time_str):
    return datetime.strptime(time_str, "%Y%m%d %H:%M:%S.%f")


def datetime2str(datetime):
    return  datetime.strftime("%Y%m%d %H:%M:%S.%f")
