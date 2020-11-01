import sys, os, datetime
import GetOldTweets_Python3 as got3
from multiprocessing import Pool

path_to_data = "/Twitter_Sentiment_Clustering_Election_2019/data/"
filename_ = "Twitter_Modi_Gandhi"

def pull_tweets(args_list):
    for args in args_list:
        date_obj, keywords, lang, pull_size = args
        start_date =  date_obj.strftime("%Y-%m-%d")
        end_date = (date_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        filename = filename_ + "_" + start_date + ".csv"

        print("Pulling Twitter Data from: " + start_date)
        tweetCriteria = got3.manager.TweetCriteria().setLang(lang).setQuerySearch(keywords).setSince(start_date).setUntil(end_date).setMaxTweets(pull_size)
        results = got3.manager.TweetManager.getTweets(tweetCriteria)
        os.makedirs(os.path.dirname(path_to_data+"raw/"+filename), exist_ok=True)
        with open(path_to_data+"raw/"+filename, "w") as f:
            for tweet in results:
                tweet_text = tweet.text
                tweet_date = str(tweet.date)
                tweet_usr_id = str(tweet.author_id)
                f.write(tweet_usr_id + "," + tweet_date + "," + tweet_text + "\n")
        print("\nTweets: " , len(results), "\nFirst Tweet Date: ", results[0].date, "\nLast Tweet Date: ", results[-1].date)

if __name__ == '__main__':
    parallel = False;
    cores = 2;
    lang = "en"
    pull_size = 0
    keywords = "@RahulGandhi OR #RahulGandhi OR Rahul Gandhi OR Rahul OR @narendramodi OR #narendramodi OR Narendra Modi OR Modi"
    start_date = "2019-04-11"
    days = 30
    args_list = []
    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(days):
        day_date_obj = start_date_obj + datetime.timedelta(days=i)
        args = [day_date_obj, keywords, lang, pull_size]
        args_list.append(args)
    if parallel:
        args_list_parts = [args_list[i::cores] for i in range(cores)]
        with Pool() as pool:
            pool.map(pull_tweets, args_list_parts)
    else: pull_tweets(args_list)
