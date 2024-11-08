# APISM

A collection of async methods for social media APIs including:

- [YouTube Data API](<https://developers.google.com/youtube/v3>)
- [X API v2](<https://developer.x.com/en/docs/x-api>)

---

## Usage

### Installation and Usage

You can install this package directly from GitHub.

```bash
pip install git+https://github.com/isom-ds/apism.git
```

### YouTube

```python
from apism import YouTubeAPI

# Initialise the YouTube API
yt = YouTubeAPI(key)

# Results are stored in the object: yt.results
await yt.search('FTX')
await yt.videos()
await yt.comment_threads()
await yt.transcript()

# Save to JSON or CSV
yt.to_json()
yt.to_csv()
```

### X

```python
from apism import xAPI

# Initialise the X API
params = {
    'search_tweets': {
        "query": "OpenAI",
        "max_results": 10
    }
}
x = xAPI(token, params)

# Results are stored in the object: x.results
await x.search_tweets(type='recent')
```

---

## Data Models


### YouTube Data API v3

```mermaid
%%{init: {
  "themeCSS": [
    "[id^=entity-SEARCH] .er.entityBox { fill: green;} ",
    "[id^=entity-VIDEOS] .er.entityBox { fill: green;} ",
    "[id^=entity-COMMENTTHREADS] .er.entityBox { fill: green;} ",
    "[id^=entity-TRANSCRIPTS] .er.entityBox { fill: green;} ",
    "[id^=entity-API] .er.entityBox { fill: blue;} ",
    "[id^=entity-API] .er.entityBox { fill: orange;} ",
    "[id^=entity-API] .er.entityBox { fill: red;} "
    ]
}}%%
erDiagram
    SEARCH }|--o{ CHANNELS : channelId
    SEARCH }|--o{ VIDEOS : videoId
    SEARCH }|--o{ PLAYLISTS : playlistId
    SEARCH }|--o{ TRANSCRIPTS : videoId
    CHANNELS ||--o{ CHANNELSECTIONS : channelId
    CHANNELS ||--o{ COMMENTTHREADS : channelId
    CHANNELS ||--o{ SUBSCRIPTIONS : channelId
    CHANNELS ||--o{ VIDEOCATEGORIES : channelId
    CHANNELS ||--o{ ACTIVITIES : channelId
    VIDEOS ||--o{ COMMENTTHREADS : videoId
    VIDEOS ||--|| CHANNELS : channelId
    VIDEOS ||--o{ VIDEOCATEGORIES : categoryId
    VIDEOS ||--o{ TRANSCRIPTS : videoId
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

⚠️ `Transcripts` uses an undocumented part of the YouTube API.
This package wraps around the [YouTube Transcript API](<https://github.com/jdepoix/youtube-transcript-api/>).

Endpoints not for data collection:

- `Captions`
- `ChannelBanners`
- `Members`
- `MembershipsLevels`
- `Thumbnails`
- `VideoAbuseReportReasons`
- `Watermarks`

### X API v2

```mermaid
%%{init: {
  "themeCSS": [
    "[id^=entity-SEARCHTWEETS] .er.entityBox { fill: green;} ",
    "[id^=entity-API] .er.entityBox { fill: blue;} ",
    "[id^=entity-API] .er.entityBox { fill: orange;} ",
    "[id^=entity-API] .er.entityBox { fill: red;} "
    ]
}}%%
erDiagram
  SEARCHTWEETS }|--|{ TWEETSLOOKUP : tweet_id
  SEARCHTWEETS }|--|{ TWEETCOUNTS : tweet_id
  SEARCHTWEETS }|--|{ RETWEETS : tweet_id
  SEARCHTWEETS }|--|{ LIKES : tweet_id
  SEARCHTWEETS }|--|{ QUOTETWEETS : tweet_id
  SEARCHTWEETS }|--|{ USERSLOOKUP : user_id
  USERSLOOKUP }|--|{ BOOKMARKS: user_id
  USERSLOOKUP }|--|{ TIMELINES: user_id
  SEARCH }|--|{ BOOKMARKS: user_id
  SEARCH }|--|{ TIMELINES: user_id
  LISTSLOOKUP
  LISTTWEETSLOOKUP
  LISTMEMBERS
```

🟩 Available
🟦 WIP
🟧 Fixing
🟥 Error
⬜ Not available

Endpoints to define rules for stream data collection
- `Filtered Stream`
- `Volume Stream`

Endpoints not for data collection:

- `Manage Tweets`
- `Spaces`
- `Direct Messages`
- `Usage`
- `Hide Replies`
- `Follows`
- `Blocks`
- `Mutes`
