from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, TooManyRequests
from youtube_transcript_api.formatters import TextFormatter, SRTFormatter
from xml.etree.ElementTree import ParseError
import asyncio
import re
import time

def _transcript(video_id, code_language='en', cookies=None, retry_limit=3, retry_delay=1, verbose=False):
    """
    Fetch transcript for a single video ID.
    Args:
        video_id (str): A single video ID to fetch transcript for.
        code_language (str): Language code for the transcript. Default='en'
        cookies (str): Path to cookies file.
        retry_limit (int): The number of retries to attempt.
        retry_delay (int): The delay between retries in seconds.
        verbose (bool): Print verbose output. Default=False
    Returns:
        dict: A dictionary mapping video ID to its transcript.
    """
    attempt = 0

    try:
        # Attempt to fetch the transcript for the given video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=cookies)
    
    except TranscriptsDisabled or ParseError:
        # Handle the case where transcripts are disabled for the video
        if verbose:
            print(f"Transcripts are disabled for video {video_id}")
        return None

    except TooManyRequests:
        # Handle rate limit error
        while attempt < retry_limit:
            attempt += 1
            if verbose:
                print(f"Attempt {attempt} failed for video {video_id}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=cookies)

    except Exception as e:
        # Catch any other exceptions that may occur
        print(f"An error occurred: {e}")
        return None

    # Identify the languages and types of the transcripts
    l_language = [
        (i.language_code, i.is_generated) for i in transcript_list 
            if i.language_code==code_language 
                or code_language in [j['language_code'] for j in i.translation_languages]
        ]
    # If code_language -> get autogenerated or manual. 
    # If NOT code_language -> get autogenerated or manual with code_language translation
    # If NO code_language translation -> return empty
    if (code_language, True) in l_language:
        transcript = transcript_list.find_generated_transcript([code_language])
        return {
            'videoId': transcript.video_id, 
            'language': transcript.language_code,
            'is_generated': transcript.is_generated,
            'transcript': transcript.fetch()
        }
    elif (code_language, False) in l_language:
        transcript = transcript_list.find_manually_created_transcript([code_language])
        return {
            'videoId': transcript.video_id, 
            'language': transcript.language_code,
            'is_generated': transcript.is_generated,
            'transcript': transcript.fetch()
        }
    else:
        generated = next((item for item in l_language if item[1] is True), None)
        manual = next((item for item in l_language if item[1] is False), None)
        if generated:
            transcript = transcript_list.find_generated_transcript([generated[0]])
            translated_transcript = transcript.translate(code_language)
            return {
                    'videoId': transcript.video_id, 
                    'language': transcript.language_code,
                    'is_generated': transcript.is_generated,
                    'transcript': translated_transcript.fetch()
                }
        elif manual:
            transcript = transcript_list.find_manually_created_transcript([manual[0]])
            translated_transcript = transcript.translate(code_language)
            return {
                    'videoId': transcript.video_id, 
                    'language': transcript.language_code,
                    'is_generated': transcript.is_generated,
                    'transcript': translated_transcript.fetch()
                }
        else:
            return None

# Asynchronous function to call the blocking function
async def transcript(video_id, code_language='en', cookies=None, retry_limit=3, retry_delay=1, batch_size=5, batch_delay=1, verbose=False):
    """
    Fetch transcript for multiple video IDs concurrently.
    Args:
        video_id (str/list): A single video ID or list of video IDs to fetch transcript for.
        code_language (str): Language code for the transcript. Default='en'
        cookies (str): Path to cookies file.
        retry_limit (int): The number of retries to attempt.
        retry_delay (int): The delay between retries in seconds.
        batch_size (int): The number of concurrent tasks to run. Default=5
        batch_delay (int): The delay between batches in seconds. Default=1
        verbose (bool): Print verbose output. Default=False
    Returns:
        dict: A dictionary mapping video IDs to their respective transcripts.
    """
    if isinstance(video_id, str):
        result = _transcript(video_id, code_language, cookies)
        result['transcript'] = formatter.format_transcript(result['transcript'])
        return result
    
    else:
        semaphore = asyncio.Semaphore(batch_size)  # Limit to batch_size concurrent tasks

        async def fetch_transcript_with_limit(value):
            async with semaphore:
                return await asyncio.to_thread(_transcript, value, code_language, cookies, retry_limit, retry_delay, verbose)
        
        tasks = []
        results = []

        for index, value in enumerate(video_id):
            tasks.append(fetch_transcript_with_limit(value))
            
            # If we've reached the batch size or the end of the list, wait for the current batch to finish
            if (index + 1) % batch_size == 0 or (index + 1) == len(video_id):
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)
                tasks.clear()  # Clear the task list for the next batch

                # Introduce delay after processing each batch, except after the final batch
                if (index + 1) < len(video_id):
                    await asyncio.sleep(batch_delay)

        # Clean up transcripts
        formatter = TextFormatter()
        for i in results:
            if i:
                i['transcript'] = re.sub(r'[\r\n\s]+', ' ', formatter.format_transcript(i['transcript']))

        return results