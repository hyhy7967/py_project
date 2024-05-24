import requests
from bs4 import BeautifulSoup

# YouTube에서 동영상 검색하여 제목과 링크 가져오는 함수
def search_youtube_video(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_link = soup.find('a', {'class': 'yt-simple-endpoint', 'id': 'video-title'})
    if video_link:
        video_title = video_link.get('title')
        video_href = video_link.get('href')
        video_url = f"https://www.youtube.com{video_href}"
        return video_title, video_url
    else:
        return None, None

# 멜론 차트 데이터 가져오는 함수
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

# 멜론 차트와 YouTube 링크를 통합한 정보 가져오기
def get_chart_with_youtube_links():
    chart = get_melon_chart()
    for entry in chart:
        query = f"{entry['title']} {entry['artist']}"
        youtube_title, youtube_url = search_youtube_video(query)
        entry['youtube_title'] = youtube_title
        entry['youtube_url'] = youtube_url
    return chart

# 템플릿 설정
def generate_html_template(chart):
    html_template = """
    <div class="container">
        <div class="section" id="chart">
            <h2>실시간 인기 차트 🎵</h2>
            <div class="chart-content">
                <ol>
                    {% for entry in chart %}
                    <li>{{ entry.rank }}: {{ entry.title }} - {{ entry.artist }} <a href="{{ entry.youtube_url }}">Watch on YouTube</a></li>
                    {% endfor %}
                </ol>
            </div>
    """
    return html_template

if __name__ == "__main__":
    # 멜론 차트와 YouTube 링크를 통합한 정보 가져오기
    chart_with_links = get_chart_with_youtube_links()
    
    # HTML 템플릿 생성
    html_template = generate_html_template(chart_with_links)
    
    # 생성한 HTML 템플릿 출력
    print(html_template)
