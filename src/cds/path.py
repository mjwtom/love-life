import sys
import os


def add_path():
    cur_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(cur_path)