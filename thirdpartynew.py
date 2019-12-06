from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
import urllib
import tweepy
import pandas as pd
from tweepy import OAuthHandler

app = Flask(__name__)

# Supporting Cross Origin requests for all APIs
cors = CORS(app)

#Google Books API
@app.route('/v1/googlebooks/<string>', methods=['GET'])
def getGoogleBooks(string):
    return jsonify(get_googlebooks(string))

def get_googlebooks(string):
    googleResourceUrl = "https://www.googleapis.com/books/v1/volumes?"
    params = {'q': string}
    finalUrl = googleResourceUrl + urllib.urlencode(params)
    response = requests.get(finalUrl)
    return json.loads(response.text)

#Tweets API
@app.route('/v1/tweets/<string>', methods=['POST'])
def TweetPred(string):
    consumer_key = "LxjMiK3zxdkGUADCxst6hO0lZ"
    consumer_secret = "isY1RawP3HvYS3HsMwCQ3ZSiRqPoau67hnceIwS0klV3bK8PvE"
    access_key = "2422714549-4jdggTNWfG0HYDHbSxPWH73JBT6zuEhWocGDlil"
    access_secret = "dKUO6419UGmgzUg3wPunTq3U2vYr4Lcj4mAkzgQ14FyRS"

    def authorize_twitter_api():
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        return tweepy.API(auth)

    def fetch_tweets(keyword, no_of_tweets=10):
        return twitter_api.search(keyword, count=no_of_tweets)

    twitter_api = authorize_twitter_api()
    keyword = string.split(" ")
    no_of_tweets = 100
    tweets = []
    terminator = 0
    for i in keyword:
        if terminator == 10:
            break
        tweets += [tweet._json for tweet in fetch_tweets(i, 5)]
    data = pd.DataFrame(tweets)
    # data.to_csv('tweet_custom.csv')
    df = data
    df['Tweet'] = df.text
    return df['Tweet'].to_json(orient='records')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
