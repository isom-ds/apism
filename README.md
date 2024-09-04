# Social Media APIs

A collection of social media APIs including:

- [X API v2](<https://developer.x.com/en/docs/x-api>)
- [YouTube Data API](<https://developers.google.com/youtube/v3>)

---
## X API v2

### Data Model
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

### Endpoints not for data collection 
- `Manage Tweets`
- `Spaces`
- `Direct Messages`
- `Usage`
- `Hide Replies`
- `Blocks`
- `Mutes`

### Requirements

---

## YouTube Data API

### Data Model
```mermaid
%%{init: {
  "themeCSS": [
    "[id^=entity-SEARCH] .er.entityBox { fill: green;} ",
    "[id^=entity-VIDEOS] .er.entityBox { fill: green;} ",
    "[id^=entity-COMMENTTHREADS] .er.entityBox { fill: green;} ",
    "[id^=entity-CAPTIONS] .er.entityBox { fill: blue;} ",
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

### Endpoints not for data collection 
- `ChannelBanners`
- `Members`
- `MembershipsLevels`
- `Thumbnails`
- `VideoAbuseReportReasons`
- `Watermarks`

### Requirements
`aiogoogle`
`googleapiclient`
