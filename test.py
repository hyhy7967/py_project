# print("나니")
# print("안녕")

import os
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# Google API 키 설정
YOUTUBE_API_KEY = 'YOUR_API_KEY'

def get_melon_chart():
    url = "https://www.melon.com/chart/index.htm"
    headers = {"User-Agent": "Mozilla/5.0 ..."}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    chart = []
    songs = soup.select('div.ellipsis.rank01 span a')
    artists = soup.select('div.ellipsis.rank02 span')

    for rank, (song, artist) in enumerate(zip(songs, artists), start=1):
        chart.append({'rank': rank, 'title': song.text, 'artist': artist.text})

    return chart

def search_youtube_video(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=1,
        type='video'
    )
    response = request.execute()
    
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    else:
        return None

def get_chart_with_youtube_links():
    chart = get_melon_chart()
    for entry in chart:
        query = f"{entry['title']} {entry['artist']}"
        youtube_link = search_youtube_video(query)
        entry['youtube_link'] = youtube_link
    return chart

if __name__ == "__main__":
    chart_with_links = get_chart_with_youtube_links()
    for entry in chart_with_links:
        print(f"Rank {entry['rank']}: {entry['title']} by {entry['artist']}")
        print(f"YouTube Link: {entry['youtube_link']}")