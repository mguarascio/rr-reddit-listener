from datetime import datetime, timedelta
import os
import praw

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

        c = 0
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            print('comment #', c)
            c = c+1
            if substring in comment.body:
                print('_____________________________________________________________')
                print('upvotes: ', comment.ups)
                print('permalink: https://www.reddit.com', comment.permalink)
                print(comment.body)

if __name__ == "__main__":
    print(datetime.utcnow().weekday())
    if datetime.utcnow().weekday() == 4: # Friday only...
        reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], 
                        client_secret=os.environ['REDDIT_CLIENT_SECRET'], 
                        user_agent='runnerreads (by /u/easy10miles)')
        subreddit = os.environ['REDDIT_SUBREDDIT']
        substring = os.environ['REDDIT_SEARCH_SUBSTRING']

        run(reddit, subreddit, substring)