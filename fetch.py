#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import codecs
import sys

import json

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDTjtlPmMX2vhAa4vfVon4Yh0ZfqCM7lsk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="snippet",
    type="channel",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []


  # Add each result to the appropriate list
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s" % (search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s" % (search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s" % (search_result["id"]["playlistId"]))

  # For now, only bother with channels (should be the only data returned anyway)
  channelObjects = []
  for i in range(len(channels)):
    channelObjects.append(youtube.channels().list(
      part="snippet,contentDetails,statistics,topicDetails,brandingSettings,invideoPromotion",
      id=channels[i]
    ).execute()["items"][0])

    channelObjects[i]["videos"]=[]
    playlist=youtube.playlistItems().list(
      part="snippet",
      playlistId=channelObjects[i]["contentDetails"]["relatedPlaylists"]["uploads"],
      maxResults=options.max_results
    ).execute()["items"]

    for video in playlist:
      channelObjects[i]["videos"].append(youtube.videos().list(
        part="snippet,contentDetails,statistics,topicDetails",
        id=video["snippet"]["resourceId"]["videoId"]
      ).execute()["items"][0])

  f = codecs.open(options.output, 'w', "utf-8")
  output=json.dumps(channelObjects, f, indent=4, separators=(',', ' : '))
  # Now adjust starting and ending characters for Weka, because Weka is silly
  output='{'+output[1:-1]+'}'
  # Now write to the file
  f.write(output)

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="let's play")
  argparser.add_argument("--max-results", help="Max results", default=25)
  argparser.add_argument("--output", help="Output filename", default="output.json")
  args = argparser.parse_args()

  UTF8Writer = codecs.getwriter('utf8')
  sys.stdout = UTF8Writer(sys.stdout)

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)