#!/usr/bin/env python

import json
from cinder import Cinder


def snap2json():
    cinder = Cinder()
    snaps = cinder.list_snapshot()
    with open('snapshots.json', 'w') as f:
        json.dump(snaps, f)

if __name__ == '__main__':
    snap2json()