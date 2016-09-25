import numpy as np
import urllib
import requests
import sys
import os
import signal
from time import time
from joblib import Parallel, delayed
import argparse


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError()


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
    return result


def import_pdf(args):
    url, fname = args
    #t0 = time()
    _, status = timeout(urllib.urlretrieve, (url, fname), timeout_duration=10, default=(fname, None))
    if (status is None or status.typeheader != 'application/pdf') and os.path.exists(fname):
        os.remove(fname)
    #print time() - t0


def get_jobs(files):
    jobs = []    
    for url in files:
        fname = os.path.basename(url)
        jobs.append((url, fname))
    return jobs


def get_files(path):
    with open(path, 'r') as f:
        files = f.read().split('\n')
        print '---', path
        print '---', len(files)
    return files


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-j', '--jobs', default=24, type=int)
    parser.add_argument('-v', '--verbose', default=2, type=int)
    parser.add_argument('-l', '--limit', type=int)
    args = parser.parse_args()
    
    files = get_files(args.input)
    jobs = get_jobs(files)    
    if args.limit is not None:    
        jobs = jobs[:args.limit]
    Parallel(n_jobs=args.jobs, verbose=args.verbose)(delayed(import_pdf)(job) for job in jobs)
    print 'Done'
