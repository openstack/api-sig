#!/usr/bin/env python

import argparse
import json
import logging
import subprocess
import sys

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Add the cross-project liaisons as reviewers " \
                    "on an API Special Interest Group review.")
    parser.add_argument('--debug', help="Print debugging information",
                        action='store_true')
    parser.add_argument("username", help="Your Gerrit username", type=str)
    parser.add_argument("review", help="An API-SIG Gerrit review", type=str)
    args = parser.parse_args()

    return (args.debug, args.username, args.review)

def get_liaisons():
    with open('doc/source/liaisons.json') as f:
        liaisons = json.load(f)['liaisons']

    names = [liaison['name'] for liaison in liaisons if liaison['name']]

    return names

def add_reviewers(debug, username, liaisons, review):
    gerrit = [
        'ssh',
        '-p',
        '29418',
        '{}@review.openstack.org'.format(username),
        'gerrit',
        'set-reviewers'
    ]

    for liaison in liaisons:
        # Hack to avoid six
        if sys.version_info.major < 3:
            liaison = liaison.encode('utf-8')
        gerrit.append('--add "{}"'.format(liaison))

    gerrit.append('{}'.format(review))

    logger.debug(' '.join(gerrit))

    subprocess.call(gerrit)

if __name__ == '__main__':
    debug, username, review = parse_args()

    level = logging.INFO
    if debug:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s')

    liaisons = get_liaisons()
    add_reviewers(debug, username, liaisons, review)

    print("Added {} reviewers to {}".format(len(liaisons), review))
