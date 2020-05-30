from matplotlib import pyplot as plt
import pandas as pd
from pandasql import sqldf

#read in csv
df = pd.read_csv('twitterdest.csv', index_col=0)

#function determining minutes elapsed
def to_minutes_since_start(t1):
    t = df.loc[t1, 'Time']
    (h, m, s) = t.split(':')
    r = int(h) * 60 + int(m) + float(s) / 60
    t_1 = df.loc[0, 'Time']
    (h, m, s) = t_1.split(':')
    r_1 = int(h) * 60 + int(m) + float(s) / 60
    return r - r_1

#adding minutes elapsed to df
elapsed_list = []
vol_list = []
for i in range(len(df)):
    elapsed_list.append(to_minutes_since_start(i))
df['elapsed'] = elapsed_list

#backing out tweet volume
for i in range(len(df)):
    count = 0
    start = 0
    if i > 175:
        start = i - 175
    for j in range(start,i):
        if df.loc[i,'elapsed'] - df.loc[j,'elapsed'] < .25 and df.loc[i,'elapsed'] - df.loc[j,'elapsed'] > 0:
            count += 1
    vol_list.append(count)


#finalizing df
df['tweet_volume'] = vol_list
df['audio_volume'] = df['tweet_volume']/df.tweet_volume.max()
df = sqldf("SELECT * FROM df WHERE elapsed <= 90.1")


#Plotting
plt.style.use('ggplot')
fig, ax = plt.subplots()
#Creating a histogram of tweet volume
ax.hist(df.elapsed, bins = 240,alpha=0.4,label='Tweets Sent',color='b')
#A line plot of audio volume
ax.plot(df.elapsed,df.audio_volume*100, color='g',label='Audio Volume (%)',alpha=.95)
#Manual title
ax.set(title='Tweet Activity/Audio Volume: Bremen v. Leverkusen')
ax.set_xlabel('Minutes since start')
ax.set_ylim(0, 230)
ax.set_xlim(0, 91)
ax.legend()

#Manual annotations for goals
ax.text(0,140,"Gebre Selassie (30')",color='black')
ax.text(3,180,"Haivertz (33')",color='black')
ax.text(48,175,"Weiser (61')",color='black')
ax.text(65,155,"Demirbay (78')",color='black')
ax.text(80,120,"Full Time",color='black')
ax.text(16,66,"Half Time",color='black')

plt.show()