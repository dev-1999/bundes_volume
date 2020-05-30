# bundes_volume
Using twitter activitiy to simply create crowd noise at Bundesliga matches.

This script (script.py) utilizes tweepy to monitor the volume of tweets surrounding an event and adjusts the volume of an application according to this twitter activity. This was designed towards simulating crowd noise for Bundesliga matches played in empty stadiums during the COVID pandemic but is robust enough to take any list of keywords and adjust any app volume accordingly.

This relies on having a crowd noise playing during the match - [this](https://www.youtube.com/watch?v=-FLgShtdxQ8&t=480s) is one easy example that just relies on changing the chrome.exe volume. The script sets the app volume proportional to the number of tweets sent in the last 25 seconds over the maximum tweet volume (defaulted to 100).

After two hours, the script ends and creates a csv of the relevant tweets (twitterdest.csv). Running histogram.py will plot the twitter activity and audio volume of the match from the data recorded.

The example here is from the last 60 minutes of Leverkusen v. Werder Bremen on 18.5.2020. Keywords used were:

- Leverkusen
- #SVWB04
- Bayer
- Werder
- Bremen
- Bundesliga

And the plot of the result:

![Plot](images/SVWB04%20Plot.png)

Clearly the crowd noise swelled exclusively around goals and full time, and is worse than someone manually creating dynamic crowd noise - but the script does pull down the text of the tweets so I plan create a script that parses the content and plays soundbites according to sentiment in the future.

Code is obviously not plug and play due to keywords/auth tokens etc...

email: devlin.s@wustl.edu
