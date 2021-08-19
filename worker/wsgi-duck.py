import os
import subprocess
import time

from flask import Flask, jsonify, request
from parse import parse

app = Flask(__name__)
ROUND = 3
TIMEOUT = 60


@app.route('/')
def hw():
    return '你好像有点过于乐观了'


@app.route('/sync')
def sync():
    os.chdir('compiler2021')
    ret = os.system('git pull') >> 8
    os.chdir('..')
    return jsonify({'ret': ret})


@app.route('/judge', methods=['POST'])
def judge():
    data = request.form
    open('asm.s', 'w').write(data['asm'] + '\n')
    base = os.path.join('testcase', data['base'])
    in_file = f'{base}.in'
    ans_file = f'{base}.out'
    os.system(f'touch {in_file}')
    # open('in.txt', 'w').write(data['input'] + '\n')
    os.system('gcc -march=armv7 asm.s libsysy.a -o main')
    avg = 0
    for _ in range(ROUND):
        p = subprocess.Popen(f'./main', stdin=open(in_file),
                             stdout=open('out.txt', 'w'), stderr=open('time.txt', 'w'))
        try:
            p.wait(TIMEOUT)
        except subprocess.TimeoutExpired:
            p.kill()
        ret = p.returncode
        # ret = os.system('./main < in.txt > out.txt 2>time.txt') >> 8
        with open('out.txt') as f:
            output = f.read().strip()
        with open('time.txt') as f:
            timing = list(filter(None, f.read().strip().split('\n')))
        if timing:
            h, m, s, us = map(int, parse(
                'TOTAL: {}H-{}M-{}S-{}us', timing[-1]))
            timing = ((h * 60 + m) * 60 + s) * 1000000 + us
            timing /= 1000000
        else:
            timing = 0.0
        avg += timing
    avg /= ROUND
    result = f'{output}\n{ret}'.strip()
    with open('out.txt', 'w') as f:
        f.write(f'{result}\n')
    ret = os.system(f'diff -wq out.txt {ans_file} 1>&2') >> 8
    return jsonify({'timing': round(avg, 6), 'return': ret})
