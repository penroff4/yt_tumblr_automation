#!/usr/bin/python3

# Usage example:
# python3 yt_tumb.py --video_id='<int>'
#                    --tumblr_id='<str>'
#                    --tumblr_pw='<pw>'

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import ytdb_tools as ytdb
import pytumblr

################################################################################

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at https://console.developers.google.com/.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

################################################################################

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# ================================__main__=====================================

if __name__ == "__main__":

  # The "video_id" option specifies the ID of the selected YouTube video
  argparser.add_argument("--video_id",
    help="ID for video for which you wish to post to your tumblr.")

  args = argparser.parse_args()

  if not args.video_id:
    #exit("Please specify video id using the --video_id= parameter.")
    args.video_id = 'ntVV3dTo-qw'

  youtube = get_authenticated_service(args)

  print(youtube)

  """
  try:
    if args.action == 'set':
      set_playlist_localization(youtube, args.playlist_id, args.default_language, args.language, args.title, args.description)
    elif args.action == 'get':
      get_playlist_localization(youtube, args.playlist_id, args.language)
    elif args.action == 'list':
      list_playlist_localizations(youtube, args.playlist_id)
    else:
      exit("Please specify a valid action using the --action= parameter.")
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  else:
    print "Set and retrieved localized metadata for a playlist."
  """

  # Authenticate to Tumblr via OAuth
  tumblr_client = pytumblr.TumblrRestClient(
    'LGHFZEDgic6GqcUMSFp1BNfuWMgQVMNviB4U6BmvlgY04x0UBw',
    'TvUvbFAxOaMCKCelAemEUrQno6CZ2bwgT9ExIJfEaE1qN7p1In',
    'Pl4aUfcml0rtVsLeePjo9JNZwJ9SIPNae5s9i9fEarVn8qBYrQ',
    'VofLOPHbsIjC4PpdXxlzZ3Xhm0bJTgA1AveX4ymJFN3PYdBA4q'
  )

  # Make the request
  print(tumblr_client.info())

  # Post video
  tumblr_client.create_video('pragandcand'
                              , state='published'
                              , caption='<a style="font-weight:bold" href="https://www.youtube.com/watch?v=9P2w_hq8YTk&ab_channel=Metronomy">Metronomy - Everything Goes My Way (test video 1)</a>'
                              , embed='https://www.youtube.com/watch?v=9P2w_hq8YTk&ab_channel=Metronomy'
                              , format='html'
                              , tags=['test', 'tag', 'metronomy', 'private', 'music', 'video', 'Everything Goes My Way']
                                            )

# pragandcand

# Creating an upload from YouTube
# client.create_video('penroff4', caption="Jon Snow. Mega ridiculous sword.", embed="http://www.youtube.com/watch?v=40pUYLacrj4")

# DEFAULT POST PARAMS
# state - a string, the state of the post. Supported types are published, draft, queue, private
# tags - a list, a list of strings that you want tagged on the post. eg: ["testing", "magic", "1"]
# tweet - a string, the string of the customized tweet you want. eg: "Man I love my mega awesome post!"
# date - a string, the customized GMT that you want
# format - a string, the format that your post is in. Support types are html or markdown
# slug - a string, the slug for the url of the post you want

# VIDEO POST PARAMS (CANNOT USE EMBED AND DATA AT SAME TIME)
# caption - a string, the caption for your post
# embed - a string, the HTML embed code for the video
# data - a string, the path of the file you want to upload
