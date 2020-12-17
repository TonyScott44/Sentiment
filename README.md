# TwitterSentimentAnalysis
It's amazing how much data is generated from a single tweet!
- Utilized Twitter's API to stream tweets in real time and generate data from the search and user_timeline API methods
- Analyzed data from tweet data elements like likes, retweets, source, length, and date
- Arguments I used were lang, tweet_mode, result_type, and count
- I focused specifically on the hashtag #twittersupport to analyze what types of tweets were surfacing...feedback on sharing fleets, suspended accounts, political related, noticed a lot of these messages were targeting Jack as well
- When I used the recent result_type argument, the tweets didn't have many likes (because they were new) but some had a lot of retweets, mostly android users
- Of course more likes were shown when I changed result_type to popular, also most of the tweets using this argument were from the twitter web app source
- Analyzed sentiment data with TextBlob(interface to perform a variety of NLP tasks, used with sentiment analysis) -1=negative 0= neutral 1=positive  (based on subjectivity, range -1 to 1 from very objective to very subjective)
- Extracted/appended tweets to JSON file
- Visualized/plotted data on graphs using Matplotlib
- Utilized python libraries like:
numpy: Scientific computing library that helped organize and format data
pandas: To create and customize data frames

