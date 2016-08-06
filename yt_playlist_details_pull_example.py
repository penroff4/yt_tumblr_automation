#!/usr/bin/python3

# Usage example:
# python3 yt_playlist_details_pull_example.py --playlist_id='<str>'

import ytdb_tools as ytdb

################################################################################

# ================================__main__=====================================

if __name__ == "__main__":

  # The "video_id" option specifies the ID of the selected YouTube video
  ytdb.argparser.add_argument("--playlist_id",
    help="ID for playlist for which you wish to pull details.")

  args = ytdb.argparser.parse_args()

  if not args.playlist_id:
    #exit("Please specify video id using the --video_id= parameter.")
    args.playlist_id = 'PLvj39SJsV11qI7lDGM2y-Y88h_qANN7Gc'

  youtube = ytdb.get_authenticated_service(args)
  yt_playlist = ytdb.get_playlist_videos(youtube, args.playlist_id)
  print(yt_playlist)
