#!/usr/bin/env python

from say_youtube_comments import get_and_say_comments
from argparse import ArgumentParser
from datetime import datetime, timedelta
from time import sleep

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
    parser.add_argument('at', help='Time at which to say comments e.g. "07:30"')
    args = parser.parse_args()

    wait_until(next_time(args.at))
    get_and_say_comments(args.video_id)
