# Social Media APIs

A collection of social media APIs including:

- [X API v2](<https://developer.x.com/en/docs/x-api>)
- [YouTube Data API](<https://developers.google.com/youtube/v3>)

---

## Usage

### Installation and Usage

You can install this package directly from GitHub.

```bash
pip install git+https://github.com/isom-ds/social-media-api-sdk.git
```

### Usage - YouTube

```python
import uoa_isom_ds_sm_api_sdk.youtube as yt

# Set query and parameters
query = 'FTX'
search_params = {
    'key': key,
    'part': 'snippet',
    'type': 'video',
    'maxResults': 50,
    'relevanceLanguage': 'en',
    'publishedAfter': '2022-12-01' + 'T00:00:00Z',
    'publishedBefore': '2022-12-01' + 'T23:59:59Z',
    'order': 'viewCount'
}
video_params = {
    'key': key,
    'part': 'id,statistics,topicDetails'
}
comments_params = {
    'key': key,
    'part': 'id,replies,snippet',
    'order': 'time'
}

# Search API -> Videos API -> CommentThreads API
svc_pipeline_results = await yt.search_videos_comments(
    query,
    search_params,
    video_params,
    comments_params
)
```


---

## Data Models

### X API v2

```mermaid
erDiagram
  TWEETS
  TIMELINES
  SEARCHTWEETS
  TWEETCOUNTS
  FILTEREDSTREAM
  VOLUMESTREAMS
  RETWEETS
  QUOTETWEETS
  LIKES
  BOOKMARKS
  USERSLOOKUP
  FOLLOWS
  SEARCH
  TRENDS
  LISTSLOOKUP
  LISTTWEETSLOOKUP
  LISTMEMBERS
```

Endpoints not for data collection:

- `Manage Tweets`
- `Spaces`
- `Direct Messages`
- `Usage`
- `Hide Replies`
- `Blocks`
- `Mutes`

---

### YouTube Data API v3

```mermaid
%%{init: {
  "themeCSS": [
    "[id^=entity-SEARCH] .er.entityBox { fill: green;} ",
    "[id^=entity-VIDEOS] .er.entityBox { fill: green;} ",
    "[id^=entity-COMMENTTHREADS] .er.entityBox { fill: green;} ",
    "[id^=entity-API] .er.entityBox { fill: blue;} ",
    "[id^=entity-API] .er.entityBox { fill: orange;} ",
    "[id^=entity-API] .er.entityBox { fill: red;} "
    ]
}}%%
erDiagram
    SEARCH }|--o{ CHANNELS : channelId
    SEARCH }|--o{ VIDEOS : videoId
    SEARCH }|--o{ PLAYLISTS : playlistId
    CHANNELS ||--o{ CHANNELSECTIONS : channelId
    CHANNELS ||--o{ COMMENTTHREADS : channelId
    CHANNELS ||--o{ SUBSCRIPTIONS : channelId
    CHANNELS ||--o{ VIDEOCATEGORIES : channelId
    CHANNELS ||--o{ ACTIVITIES : channelId
    VIDEOS ||--o{ COMMENTTHREADS : videoId
    VIDEOS ||--|| CHANNELS : channelId
    VIDEOS ||--o{ VIDEOCATEGORIES : categoryId
    VIDEOS ||--o{ CAPTIONS : videoId
    PLAYLISTS ||--o{ PLAYLISTIMAGES : playlistId
    PLAYLISTS ||--o{ PLAYLISTITEMS : playlistId
    PLAYLISTS ||--|| CHANNELS : channelId
    COMMENTTHREADS ||--|| COMMENTS : commentId
```

🟩 Available
🟦 WIP
🟧 Fixing
🟥 Error
⬜ Not available

Endpoints not for data collection:

- `Captions`
- `ChannelBanners`
- `Members`
- `MembershipsLevels`
- `Thumbnails`
- `VideoAbuseReportReasons`
- `Watermarks`
