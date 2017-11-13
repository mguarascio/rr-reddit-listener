from datetime import datetime, timedelta
import os
import praw
import re
import requests
import sys

def run(reddit, subreddit, substring):
    print('running...')

    finish = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start = finish - timedelta(days=7)
    print('start: ', start)
    print('finish: ', finish)
 
    s = 0
    for submission in reddit.subreddit(subreddit).submissions(start.timestamp(), finish.timestamp()):
        print('submission #: ', s)
        s = s+1
        if substring in submission.title or substring in submission.url: 
            print('_________________________________________________________________')
            post_comment(submission.title + ', ' + submission.url, 'https://www.reddit.com' + submission.permalink, submission.ups)

        c = 0
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            c = c+1
            if substring in comment.body:
                print('_____________________________________________________________')
                post_comment(comment.body, 'https://www.reddit.com' + comment.permalink, comment.ups)

def post_comment(comment, link, ups):
    url = re.search("(?P<url>https://www.amazon[^\s]+[0-9a-zA-Z//])", comment).group("url")
    print(url)

    try:
        asin = re.search("\/([A-Z0-9]{10})\/?", url).group(1)
        print(asin)

        headers = {'Authorization': 'Token ' + os.environ['RUNNERREADS_API_TOKEN']}

        if asin:
            data = {
                'title': 'reddit_placeholder',
                'link': url,
                'ASIN': asin,
                'comments': [
                    {
                        'text': comment,
                        'link': link,
                        'ups': ups
                    }
                ]
            }
            print(data)
            response = requests.post(url=os.environ['RUNNERREADS_API'], headers=headers, json=data)
            print(response)
        else: 
            print('no asin found in ', url)
    except:
        e = sys.exc_info()[0]
        print('Exception posting comment: ', e)

if __name__ == "__main__":
    print(datetime.utcnow().weekday())
    if datetime.utcnow().weekday() == 5: # Saturday
        reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], 
                        client_secret=os.environ['REDDIT_CLIENT_SECRET'], 
                        user_agent='runnerreads (by /u/easy10miles)')
        subreddit = os.environ['REDDIT_SUBREDDIT']
        substring = os.environ['REDDIT_SEARCH_SUBSTRING']

        run(reddit, subreddit, substring)