#!/usr/bin/env python
#
# Requires a Mac
# Be sure to install xmltodict using Pip

import requests
import xmltodict
import sys
import subprocess
from time import sleep
from argparse import ArgumentParser
from datetime import datetime, timedelta

def get_xml(url):
    req = requests.get(url)
    if req.status_code != 200:
        sys.exit('Error fetching %s (%d)' % (url, req.status.code))
    return xmltodict.parse(req.content)

def comments_url(vid_id):
    return 'https://gdata.youtube.com/feeds/api/videos/%s/comments' % vid_id

def say(text):
    print text
    subprocess.call(['say', text])

def say_comment(entry):
    if not entry['content'].has_key('#text'):
        return
    say('%s says' % entry['author']['name'])
    say(entry['content']['#text'])

def get_comments(vid_id):
    for entry in get_xml(comments_url(vid_id))['feed']['entry']:
        yield entry

def get_and_say_comments(vid_id):
    for c in get_comments(vid_id):
        say_comment(c)
        sleep(1)

def next_time(time_str):
    [h, m] = map(int, time_str.split(':'))
    now = datetime.now()
    when = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if h * 60 + m <= now.hour * 60 + now.minute:
        when += timedelta(days=1) # tomorrow
    return when

def wait_until(when):
    print('Waiting until {}'.format(when))
    sleep((when - datetime.now()).total_seconds())

if __name__ == '__main__':
    parser = ArgumentParser(description='Your YouTube comment alarm clock')
    parser.add_argument('video_id', help='YouTube video ID')
    parser.add_argument('--at', dest='time', help='Time at which to say comments. e.g. "07:30"')
    args = parser.parse_args()

    if args.time:
        wait_until(next_time(args.time))
    get_and_say_comments(args.video_id)
