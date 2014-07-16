import praw
import time
from textblob import TextBlob

SUBMISSION_LIMIT = 100
NUM_COMMENTS_THRESHOLD = 100
COMMENT_REPLACE_LIMIT = 2

if __name__ == "__main__":
    r = praw.Reddit('Sentiment Analysis Bot by /u/Xece v 1.0.')
    r.login('username', 'password')
    alreadyDone = []
    
    while True:
        subreddit = r.get_subreddit('all')
        for submission in subreddit.get_hot(limit = SUBMISSION_LIMIT):
            print "Processing thread %s \n" % submission.id 
            submission.replace_more_comments(limit = COMMENT_REPLACE_LIMIT)
            flatComments = praw.helpers.flatten_tree(submission.comments)
            if (len(flatComments) > NUM_COMMENTS_THRESHOLD and submission.id not in alreadyDone):
                posCount = 0
                negCount = 0
                polaritySum = 0
                subjectivitySum = 0
                for comment in flatComments:
                    try:
                        if (TextBlob(comment.body).sentiment.polarity > 0):
                            posCount += 1
                        else: 
                            negCount += 1
                        polaritySum += TextBlob(comment.body).sentiment.polarity
                        subjectivitySum += TextBlob(comment.body).sentiment.subjectivity
                    except: 
                        pass
                print """There are a total of %d analysed comments,
of which %d are positive 
and %d are negative \n""" % (
                        posCount + negCount, posCount, negCount)
                print """The average polarity of the comments is %f                
and the average subjectivity is %f\n""" % (
                        polaritySum / (posCount + negCount), 
                        subjectivitySum / (posCount + negCount))
                alreadyDone.append(submission.id)
        time.sleep(1800) #rest for half an hour
