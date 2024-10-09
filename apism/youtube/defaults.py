import datetime

_default_params = {
    'search': {
        'part': 'snippet',
        'type': 'video',
        'maxResults': 50,
        'relevanceLanguage': 'en',
        'publishedAfter': datetime.date.today().strftime('%Y-%m-%d') + 'T00:00:00Z',
        'publishedBefore': datetime.date.today().strftime('%Y-%m-%d') + 'T23:59:59Z',
        'order': 'viewCount'
    },
    'videos': {
        'part': 'id,statistics,topicDetails'
    },
    'commentThreads': {
        'part': 'id,replies,snippet',
        'order': 'time'
    }
}

_default_columns = {
    'default': {
        'search': [
            'snippet.thumbnails.medium.height', 
            'snippet.channelTitle',
            'snippet.thumbnails.default.url',
            'snippet.thumbnails.high.height',
            'id.videoId', 
            'snippet.thumbnails.medium.url',
            'snippet.liveBroadcastContent', 
            'snippet.channelId',
            'snippet.publishedAt', 
            'snippet.thumbnails.default.width',
            'snippet.thumbnails.default.height', 
            'snippet.title',
            'snippet.thumbnails.high.width', 
            'id.kind', 
            'kind',
            'snippet.thumbnails.medium.width', 
            'snippet.publishTime', 
            'etag',
            'snippet.description', 
            'snippet.thumbnails.high.url'
        ],
        'videos': [
            'statistics.likeCount', 
            'statistics.commentCount', 
            'kind', 
            'id',
            'statistics.favoriteCount', 
            'etag', 
            'statistics.viewCount',
            'topicDetails.topicCategories'
            ],
        'commentThreads': [
            'snippet.topLevelComment.snippet.canRate',
            'snippet.topLevelComment.snippet.textDisplay',
            'snippet.topLevelComment.kind',
            'snippet.topLevelComment.snippet.channelId', 
            'snippet.totalReplyCount',
            'snippet.topLevelComment.snippet.authorProfileImageUrl',
            'snippet.topLevelComment.snippet.videoId', 
            'snippet.topLevelComment.id',
            'snippet.topLevelComment.snippet.likeCount',
            'snippet.topLevelComment.snippet.publishedAt', 
            'id',
            'snippet.topLevelComment.snippet.authorDisplayName', 
            'snippet.canReply',
            'snippet.channelId', 
            'snippet.topLevelComment.snippet.authorChannelUrl',
            'snippet.topLevelComment.etag', 
            'snippet.videoId', 
            'kind',
            'snippet.topLevelComment.snippet.authorChannelId.value',
            'snippet.topLevelComment.snippet.textOriginal', 
            'etag',
            'snippet.isPublic', 
            'snippet.topLevelComment.snippet.updatedAt',
            'snippet.topLevelComment.snippet.viewerRating',
        ],
        'commentThreadsreplies': [
            'kind', 
            'id', 
            'snippet.authorDisplayName',
            'snippet.authorProfileImageUrl', 
            'snippet.textDisplay',
            'snippet.updatedAt', 
            'snippet.channelId', 
            'snippet.viewerRating',
            'snippet.authorChannelUrl', 
            'snippet.authorChannelId.value',
            'snippet.publishedAt', 
            'etag', 
            'snippet.videoId',
            'snippet.textOriginal', 
            'snippet.likeCount', 
            'snippet.parentId',
            'snippet.canRate'
        ],
        'transcripts': [
            'videoId',
            'language',
            'is_generated',
            'transcript'
        ]
    },
    'shorten': {
        'search': [
            'liveBroadcastContent', 
            'url', 
            'kind', 
            'channelTitle', 
            'height',
            'title', 
            'description', 
            'etag', 
            'publishTime', 
            'width', 
            'publishedAt',
            'channelId', 
            'videoId'
        ],
        'videos': [
            'viewCount', 
            'kind', 
            'id', 
            'favoriteCount', 
            'topicCategories', 
            'etag',
            'likeCount', 
            'commentCount'
        ],
        'commentThreads': [
            'textDisplay', 
            'totalReplyCount', 
            'canReply', 
            'authorDisplayName',
            'authorProfileImageUrl', 
            'viewerRating', 
            'authorChannelUrl',
            'likeCount', 
            'textOriginal', 
            'updatedAt', 
            'id', 
            'channelId', 
            'canRate',
            'kind', 
            'value', 
            'isPublic', 
            'etag', 
            'publishedAt', 
            'videoId'
        ],
        'commentThreadsreplies': [
            'authorProfileImageUrl', 
            'canRate', 
            'kind', 
            'textDisplay', 
            'id',
            'value', 
            'viewerRating', 
            'authorChannelUrl', 
            'etag', 
            'likeCount',
            'textOriginal', 
            'updatedAt', 
            'authorDisplayName', 
            'parentId',
            'publishedAt', 
            'channelId', 
            'videoId'
        ],
        'transcripts': [
            'videoId',
            'language',
            'is_generated',
            'transcript'
        ]
    }
}