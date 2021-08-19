#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from glob import glob

import requests
from redis import Redis

BASE = 'https://r.nya.rs:8987'
COMPILER = '/var/www/duck/thu-cs-compiler/build/main'

WA = 1919
CE = 114
TLE = 514


def judge(asm_file, base):
    data = {}

    with open(asm_file) as f:
        data['asm'] = f.read().strip()

    # with open(in_file) as f:
    #     data['input'] = f.read().strip()
    data['base'] = base

    res = requests.post(url=BASE + '/judge', data=data)

    if res.status_code != 200:
        print(res.status_code, file=sys.stderr)
        if res.status_code == 504:
            print('Timeout!', file=sys.stderr)
        return None

    recv = res.json()
    return recv['timing'], recv['return']


res = requests.get(f'{BASE}/sync')
# assert(res.json()['ret'] == 0)

duck = dict()
with Redis(decode_responses=True) as r:
    fargs = r.get('fargs')
print(f'fargs: {fargs}', file=sys.stderr)


for file in sorted(glob(os.path.join(sys.argv[1], '*.sy'))):
    uid = os.path.splitext(file)[0]
    duck[uid] = WA
    print(uid, file=sys.stderr)
    # os.system(f'touch {uid}.in')
    if os.path.exists(f'{uid}.s'):
        os.remove(f'{uid}.s')
    if len(sys.argv) == 2:
        os.system(
            f'{COMPILER} {uid}.sy -o {uid}.s {fargs} > /dev/null')
    elif sys.argv[2] == 'clang':
        os.system(
            f'clang -S -x c {uid}.sy -include kslib.h -std=gnu99 --target=armv7-unknown-linux-eabi -march=armv7a -mcpu=cortex-a72 -mfpu=neon -mfloat-abi=hard -O3 -Ofast -fvectorize -no-integrated-as > /dev/null 2> /dev/null')
    elif sys.argv[2] == 'gcc':
        os.system(
            f'arm-linux-gnueabihf-g++ -S -x c++ {uid}.sy -include kslib.h -mcpu=cortex-a72 -mfpu=neon -mfloat-abi=hard -O3 -Ofast > /dev/null 2> /dev/null')
    if not os.path.exists(f'{uid}.s'):
        duck[uid] = CE
        print('Build failed.', file=sys.stderr)
        continue
    if (result := judge(f'{uid}.s', f'{uid}')) is None:
        duck[uid] = TLE
        print('Judge failed.', file=sys.stderr)
        continue
    timing, ret = result
    if ret == 0:
        print('Passed.', file=sys.stderr)
        print(timing, file=sys.stderr)
        duck[uid] = timing
    else:
        print('Failed', file=sys.stderr)

print(json.dumps(duck, indent='\t'))
