#!/usr/bin/env python
#
# Requires a Mac
# Be sure to install xmltodict using Pip

import requests
import xmltodict
import sys
import subprocess
from time import sleep

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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage:\n\t%s VIDEO_ID' % sys.argv[0]
        sys.exit(1)
    get_and_say_comments(sys.argv[1])
