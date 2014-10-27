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
    say('%s says' % entry['author']['name'])
    say(entry['content']['#text'])

if __name__ == '__main__':
    for c in get_xml(comments_url(sys.argv[1]))['feed']['entry']:
        say_comment(c)
        sleep(1)
