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
            print(submission.title)
            print(submission.url)
            print('upvotes: ', submission.ups)
            print('permalink: https://www.reddit.com', submission.permalink)
            post_comment(submission.title + ', ' + submission.url, 'https://www.reddit.com' + submission.permalink)

        c = 0
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            c = c+1
            if substring in comment.body:
                print('_____________________________________________________________')
                print('upvotes: ', comment.ups)
                print('permalink: https://www.reddit.com', comment.permalink)
                print(comment.body)
                post_comment(comment.body, 'https://www.reddit.com' + comment.permalink)

def post_comment(comment, link):
    url = re.search("(?P<url>https://www.amazon[^\s]+[0-9a-zA-Z//])", comment).group("url")
    print(url)

    try:
        asin = re.search("\/([A-Z0-9]{10})\/?", url).group(1)
        print(asin)

        headers = {'Authorization': 'Token ' + os.environ['RUNNERREADS_API_TOKEN']}

        data = {
            'title': 'reddit_placeholder',
            'link': url,
            'ASIN': asin,
            'comments': [
                {
                    'text': comment,
                    'link': link
                }
            ]
        }
        print(data)
        response = requests.post(url=os.environ['RUNNERREADS_API'], headers=headers, json=data)
        print(response)
    except:
        e = sys.exc_info()[0]
        print('Exception posting comment: ', e)

if __name__ == "__main__":
    print(datetime.utcnow().weekday())
    if datetime.utcnow().weekday() == 4: # Fridays
        reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], 
                        client_secret=os.environ['REDDIT_CLIENT_SECRET'], 
                        user_agent='runnerreads (by /u/easy10miles)')
        subreddit = os.environ['REDDIT_SUBREDDIT']
        substring = os.environ['REDDIT_SEARCH_SUBSTRING']

        run(reddit, subreddit, substring)