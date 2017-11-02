import os
import praw

def run(reddit, subreddit, substring):
    print('running...')
    for comment in reddit.subreddit(subreddit).stream.comments():
        print(comment.id)
        if substring in comment.body:
            print('_____________________________________________________________')
            print('upvotes: ', comment.ups) # num upvotes
            print('permalink: https://www.reddit.com', comment.permalink) # use this, but prefix with https://www.reddit.com
            print(comment.body)

if __name__ == "__main__":
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], 
                    client_secret=os.environ['REDDIT_CLIENT_SECRET'], 
                    user_agent='runnerreads (by /u/easy10miles)')
    subreddit = os.environ['REDDIT_SUBREDDIT']
    substring = os.environ['REDDIT_SEARCH_SUBSTRING']

    run(reddit, subreddit, substring)