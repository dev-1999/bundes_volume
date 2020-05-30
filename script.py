import tweepy
from datetime import datetime, timedelta
import pandas as pd
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

#Change these keywords according to match
keywords = ['Leverkusen', '#SVWB04', 'Bayer', 'B04', 'Werder', 'Bremen', 'Bundesliga']

#Choose application volume to adjust ('chrome', 'vlc', ...)
source = 'chrome'

#print(datetime.datetime.now() - datetime.timedelta(minutes=1))

#These keys are now outdated
auth = tweepy.OAuthHandler(consumer_key='szWDZmIlsDYZce9I3kmNRqqzO',
                  consumer_secret='6sUOo6vwj0JjGD3of9Y3BlUKcDyNo2AvXCZyfB8sKpiWcyDL0G')
auth.set_access_token('1044080921677377536-27dG33ZYvFxIFpayxduuD0sQKXAzti',
                  '9SQEmn7MlUIGDX0bQwDyGhlaaHy1Gj8Yfy4JvwgFeRs3f')
api = tweepy.API(auth)

time_list = []
text_list = []
score_list = []
end_time = datetime.now() + timedelta(hours=2)

#sets volume of corresponding app
def set_volume(vol,app=source):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == app + ".exe":
            volume.SetMasterVolume(vol, None)


#Creates Stream - api: auth api, interval: seconds for rolling avg
class Stream(tweepy.StreamListener):
    def __init__(self, api, interval):
        self.api = api
        self.me = api.me()
        self.tweetlist = []
        self.interval = interval

#Every Time There's a new tweet this gets run
    def on_status(self, tweet):
        self.tweetlist.append(datetime.now())
        #max volume of tweets
        max_x = 100
        #current volume of tweets
        x = 0
        #determines which tweets are recent
        for d in self.tweetlist:
            if d > (datetime.now() - timedelta(seconds=self.interval)):
                x += 1
        #removes old tweets
        if len(self.tweetlist) > x + 5:
            self.tweetlist = self.tweetlist[(-1*x + 2):]
        #status update
        print(str(x) + " tweets in last " + str(self.interval) + " sec.")
        #sets new max if needed
        if x > max_x:
            max_x = x
        #adds time to record
        time_list.append(datetime.now().strftime("%H:%M:%S.%f"))
        #adds text to record
        text_list.append(tweet.text)
        #adds score to record
        score_list.append(x/max_x)
        #sets the volume of chrome
        set_volume(x/max_x)
        #exit if past time threshold
        if datetime.now() > end_time:
            #creates df
            df = pd.DataFrame(list(zip(time_list, text_list, score_list)), columns=['Time', 'Text', 'Volume'])
            #pushes to destination
            df.to_csv('twitterdest.csv')
            set_volume(100)
            print('done')
            exit()
    def on_error(self, status):
        print("Error Detected")

#Runs the stream
tweets_listener = Stream(api, 25)
stream = tweepy.Stream(api.auth,tweets_listener)

#Tracks keywords in English and German
stream.filter(track=keywords, languages=['en','de'])