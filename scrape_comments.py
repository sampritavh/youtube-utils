import os
import sys
import json

import googleapiclient.discovery
import googleapiclient.errors


from googleapiclient.discovery import build

api_key = os.environ.get('API_KEY')
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def search_videos_by_keyword(keyword, num_items=10):
	videos = []
	youtube = build('youtube', 'v3',
					developerKey=api_key)
	request = youtube.search().list(
		part='id',
		maxResults=num_items,
		q=keyword
	)
	response = request.execute()
	for video in response["items"]:
		if video["id"]["kind"] == "youtube#video":
			videos.append(video["id"]["videoId"])
	return videos

def video_comments(video_id):
    result = {
        "url": "https://youtube.com/watch?v={0}".format(video),
        "comments": []
    }
	# empty list for storing reply
    replies = []

	# creating youtube resource object
    youtube = build('youtube', 'v3',
					developerKey=api_key)

	# retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id
    ).execute()

	# iterate video response
    while video_response:

        print(video_response)
        # extracting required info
        # from each result object
        for item in video_response['items']:
            
            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            
            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            # if reply is there
            if replycount>0:
                
                # iterate through all reply
                for reply in item['replies']['comments']:
                    
                    # Extract reply
                    reply = reply['snippet']['textDisplay']
                    
                    # Store reply is list
                    replies.append(reply)

            # print comment with list of reply
            #print(comment, replies, end = '\n\n')

            # empty reply list
            replies = []

        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                    pageToken = video_response["nextPageToken"]
                ).execute()
            print(video_response)
        else:
            break
		   


if __name__ == "__main__":
    keyword = sys.argv[1]

    results = list()
    videos = search_videos_by_keyword(keyword,num_items=10)
    for video in videos:
        result = video_comments(video)
        results.append(result)
