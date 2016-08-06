import sqlite3
import time

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

################################################################################

today = time.strftime("%x") + " " + time.strftime("%X")

ytDB = 'YouTube'
connection = sqlite3.connect(ytDB)
c = connection.cursor()

# ====================================

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

# ===========================Define Methods====================================

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

# ====================================

# Insert video record to YT_Video table
def video_to_sql(video_id, name, published_date, channel_id):

    try:
        c.execute("INSERT INTO YT_Video VALUES (?, ?, ?, ?, ?, ?)",
                  (video_id, name, published_date, today, today, channel_id))
    except sqlite3.IntegrityError:
        print('you done goofed: sqlite3.IntegrityError')

# ====================================

# Insert user record into YT_User table
def user_to_sql(user_id, name, create_date):

    try:
        c.execute("INSERT INTO YT_User VALUES (?, ?, ?, ?, ?)",
                  (user_id, name, create_date, today, today))
    except sqlite3.IntegrityError:
        print('you done goofed')

# ====================================

# Insert playlist record into YT_Playlist table
def playlist_to_sql(playlist_id, name, create_date, channel_id):

    try:
        c.execute("INSERT INTO YT_Playlist VALUES (?, ?, ?, ?)",
                  (playlist_id, name, create_date, today, today, channel_id))
    except sqlite3.IntegrityError:
        print('you done goofed')

# ====================================

# Insert channel record into YT_Channel table
def channel_to_sql(channel_id, name, create_date, owner_id):

    try:
        c.execute("INSERT INTO YT_Channel VALUES (?, ?, ?, ?, ?, ?",
                  (channel_id, name, create_date, today, today, owner_id))
    except sqlite3.IntegrityError:
        print('you done goofed')

# ====================================

# Get details for specific YouTube Video from YouTube API
def get_video_details(youtube, video_id):
    video_results = youtube.videos().list(
        part="snippet, contentDetails",
        id=video_id,
        maxResults=50
    )

    video_results_response = video_results.execute()

    video_details_dict = {
        'id':
            video_results_response["items"][0]["id"],
        'title':
            video_results_response["items"][0]["snippet"]["title"],
        'published_at':
            video_results_response["items"][0]["snippet"]["publishedAt"],
        'channel_id':
            video_results_response["items"][0]["snippet"]["channelId"],
        'description':
            video_results_response["items"][0]["snippet"]["description"],
        'channel_title':
            video_results_response["items"][0]["snippet"]["channelTitle"],
        'duration':
            video_results_response["items"][0]["contentDetails"]["duration"],
        'definition':
            video_results_response["items"][0]["contentDetails"]["definition"],
        'licensedContent':
            video_results_response["items"][0]["contentDetails"][
                "licensedContent"]}

    return video_details_dict

# ====================================

# Get details for specific YouTube Playlist from YouTube API
def get_playlist_details(youtube, playlist_id):
    list_results = youtube.playlists().list(
        part="snippet, contentDetails",
        id=playlist_id,
        maxResults=50
    )

    list_results_response = list_results.execute()

    list_details_dict = {
        'playlist_id':
            list_results_response["items"][0]["id"],
        'playlist_title':
            list_results_response["items"][0]["snippet"]["title"],
        'playlist_published_at':
            list_results_response["items"][0]["snippet"]["publishedAt"],
        'playlist_channel_id':
            list_results_response["items"][0]["snippet"]["channelId"],
        'playlist_description':
            list_results_response["items"][0]["snippet"]["description"],
        'playlist_channel_title':
            list_results_response["items"][0]["snippet"]["channelTitle"],
        'playlist_item_count':
            list_results_response["items"][0]["contentDetails"]["itemCount"]
            }

    return list_details_dict

# ====================================

# Get details for specific YouTube Channel from YouTube API
def get_channel_details(youtube, channel_id):
    channel_results = youtube.videos().list(
        part="snippet, contentDetails",
        id=channel_id,
        maxResults=50
    )

    channel_results_response = channel_results.execute()

    channel_details_dict = {
        'id':
            channel_results_response["items"][0]["id"],
        'title':
            channel_results_response["items"][0]["snippet"]["title"],
        'published_at':
            channel_results_response["items"][0]["snippet"]["publishedAt"],
        'description':
            channel_results_response["items"][0]["snippet"]["description"],
        'googlePlusUserId':
            channel_results_response[
                "items"][0]["contentDetails"]["googlePlusUserId"]
    }

    return channel_details_dict

# ====================================

# Retrieve playlist info and relevant channel info
def get_channel_playlists(youtube, channel_id):

    channel_dict= {channel_id:get_channel_details(youtube, channel_id)}

    # Set up API call for Channel details
    channel_results = youtube.channels().list(
        part='snippet, contentDetails, contentOwnerDetails',
        id=channel_id
    )

    # Execute API Call for channel details
    channel_results_response = channel_results.execute()

    # Set up Channel Details
    yt_details = channel_results_response["items"][0]

    yt_channel_id = yt_details["id"]
    yt_channel_name = yt_details["snippet"]["title"]
    yt_channel_owner_id = yt_details["contentDetails"]["googlePlusUserId"]
    yt_channel_create_date = yt_details["snippet"]["publishedAt"]

    # Add channel to channel dictionary
    channel_dict = {yt_channel_id:yt_channel_name}

    # Print
    # 'Channel ID - Channel Name - Channel Owner ID - Channel Create Date'

    print("Channel: {1} ({0})\nOwner: {2}\nCreated On: {3}\n".format(
        yt_channel_id,
        yt_channel_name,
        yt_channel_owner_id,
        yt_channel_create_date))

    # Set up API call for Playlist details

    channel_results = youtube.playlists().list(
        part="snippet, contentDetails",
        channelId=channel_id,
        maxResults=50
    )

    # Execute API call for Playlist details
    channel_results_response = channel_results.execute()
    loop_number = 0

    # Loop through API call results for playlist details
    for playlist in channel_results_response["items"]:

        # Loop counter
        loop_number += 1

        # Grab playlist title
        playlist_title = playlist["snippet"]["title"]

        # Grab playlist ID
        playlist_id = playlist["id"]

        #
        playlist_dict[playlist_id] = playlist_title
        print("%s -- %s (%s)" % (loop_number, playlist_title, playlist_id))

# ====================================

# Retrieve and combine multiple playlists into a single list
def combine_channel_playlist(youtube, channel_id):

    # Set up API call
    channel_playlist_results = youtube.playlists().list(
        part="snippet, contentDetails",
        channelId=channel_id,
        maxResults=50
    )

    # Execute API call
    channel_playlist_results_response = channel_playlist_results.execute()

    # Set up method loop counter
    loop_number = 0

    # Set up array to record # of playlists in channel.
    # This is used later for print and playlist selection purposes.
    returned_playlists = []

    for playlist in channel_playlist_results_response["items"]:

        # Increment loop counter
        loop_number += 1

        # Add current loop counter value to returned playlist dictionary
        # This will act as a 'hacky' record id for the playlist
        returned_playlists.append(loop_number)

        # Set up playlist title and playlist id variables from API call return
        playlist_title = playlist["snippet"]["title"]
        playlist_id = playlist["id"]

        # List playlist on screen
        print("%s -- %s (%s)" % (loop_number, playlist_title, playlist_id))

    # Ask user for comma delimited input showing which playlists to pick based
    # on playlist record number (i.e. returned_playlists dictionary.
    picked_playlist = input("\nWhich playlist would you like to combine?\n"
                            "Enter numbers separated by commas\n")
    # Formatting line break
    print("\n")

    # Formats picked_playlist values; does work to convert string to list of
    # ints
    picked_playlist = picked_playlist.split(',')
    picked_playlist = filter(None, picked_playlist)
    picked_playlist = list(map(int, picked_playlist))

    # Validating user input to ensure picked values are within bounds of
    # available returned_playlist dict values
    if min(picked_playlist) < min(returned_playlists) or \
                    max(picked_playlist) > max(returned_playlists):
        exit('You specified a playlist that wasn\'t on the list!\n')

    # Reset loop counter
    loop_number = 0

    # Loops through returned playlist from API call and calls
    # get_playlist_videos method to return items in those playlists
    for playlist in channel_playlist_results_response["items"]:

        # Increment loop counter
        loop_number += 1

        # If current loop matches a number in the picked_playlist list, then
        # it runs get_playlist_videos method to return items in that playlist
        if loop_number in picked_playlist:
            get_playlist_videos(youtube, playlist["id"])

# ====================================

# Get list of videos in specific YouTube Playlist from YouTube API
# Record YouTube API response and return it
def get_playlist_videos(youtube, playlist_id):

    # Grab overall playlist details (e.g. title, channel, published date, ect)
    playlist_details = get_playlist_details(youtube, playlist_id)

    # Stick playlist details in dict.  We'll stick video info here late as well.
    playlist_dict = {'playlist_details':playlist_details}

    playlist_results = youtube.playlistItems().list(
        part="snippet, contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )

    playlist_results_response = playlist_results.execute()

    # Record information about each video.  Continue looping through each page
    # of playlist repsonse until out of pages, then break loop.
    while True:

        for playlist_item in playlist_results_response["items"]:

            video_dict = {
                'video_title':
                    playlist_item["snippet"]["title"],
                'video_id':
                    playlist_item["snippet"]["resourceId"]["videoId"],
                'video_published_date':
                    playlist_item["snippet"]["publishedAt"],
                'video_description':
                    playlist_item["snippet"]["description"],
                'video_playlist_position':
                    playlist_item["snippet"]["position"]
            }

            playlist_dict[video_dict['video_playlist_position']] = video_dict

        # If reached end of response list, exit loop
        if "nextPageToken" not in playlist_results_response:
            break

        # Otherwise set things up to move to the next page in playlist response
        next_page = playlist_results_response["nextPageToken"]

        playlist_results = youtube.playlistItems().list(
            part="snippet, contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
            )
        playlist_results_response = playlist_results.execute()

    return playlist_dict

# ================================__main__=====================================

# if __name__ == "__main__":
