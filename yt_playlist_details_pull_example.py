#!/usr/bin/python3

# Usage example:
# python3 yt_playlist_details_pull_example.py --playlist_id='<str>'

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import ytdb_tools as ytdb

###############################################################################

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
  argparser.add_argument("--playlist_id",
    help="ID for playlist for which you wish to pull details.")

  args = argparser.parse_args()

  if not args.playlist_id:
    #exit("Please specify video id using the --video_id= parameter.")
    args.playlist_id = 'PLvj39SJsV11qI7lDGM2y-Y88h_qANN7Gc'

  youtube = get_authenticated_service(args)
  yt_playlist = ytdb.get_playlist_videos(youtube, args.playlist_id)
  print(yt_playlist)
