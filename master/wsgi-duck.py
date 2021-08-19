import json
import os
import time
from collections import defaultdict
from glob import glob

import requests
from flask import Flask, abort, jsonify, request
from redis import Redis

app = Flask(__name__)
PASSWD = 'passwd'



@app.route('/')
def hw():
    return '小林家的编译器'


@app.route('/hook', methods=['GET', 'POST'])
@app.route('/hook/<commit>', methods=['GET', 'POST'])
def hook(commit='master'):
    fargs = ' '.join(filter(lambda x: x.startswith(
        '--'), request.args.getlist('f')))
    if fargs:
        passwd = request.args.get('p', None)
        if passwd != PASSWD:
            abort(403)
    r = Redis(decode_responses=True)
    r.set('fargs', fargs)
    if os.path.exists('lock'):
        return jsonify({'result': 'pending last judge'})
    os.mknod('lock')
    uid = len(glob('results/*')) - 5 # clang.json clang.txt gcc.json gcc.txt best.json
    os.system(f'bash judge.sh {commit} {uid}')
    best(silent=True)
    r.set('fargs', '')
    return jsonify({'result': uid})


@app.route('/best')
def best(silent=False):
    timing = defaultdict(list)
    for path in glob('results/*'):
        if not os.path.isdir(path):
            continue
        with open(os.path.join(path, 'commit.txt')) as f:
            commit = f.read().strip()
        try:
            perf = glob(os.path.join(path, 'performance*.json'))[0]
            with open(perf) as f:
                data = json.load(f)
            for k, v in data.items():
                timing[k].append((v, commit))
        except:
            pass
    records = {k: min(v) for k, v in timing.items()}
    with open('results/best.json', 'w') as f:
        json.dump(records, f, indent='\t')
    if not silent:
        return jsonify(records)
