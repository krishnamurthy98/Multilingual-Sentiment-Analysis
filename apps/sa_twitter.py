import pickle
import os
import re
import twitter
import pandas as pd
from textblob import TextBlob
import json
#---from google.cloud import translate
import neural_network

pd.options.display.max_colwidth = 700


def perform_analysis(query, lang, geocode):

    # Autheneticate with twitter
    if not os.path.exists('twitter_credentials.pkl'):
        Twittercredentials={}
        Twittercredentials['Consumer Key'] = ''
        Twittercredentials['Consumer Secret'] = ''
        Twittercredentials['Access Token'] = ''
        Twittercredentials['Access Token Secret'] = ''
        with open('twitter_credentials.pkl','wb') as f:
            pickle.dump(Twittercredentials, f)
    else:
        Twittercredentials=pickle.load(open('twitter_credentials.pkl','rb'))


    auth = twitter.oauth.OAuth(Twittercredentials['Access Token'],
                               Twittercredentials['Access Token Secret'],
                               Twittercredentials['Consumer Key'],
                               Twittercredentials['Consumer Secret'])
    twitter_api = twitter.Twitter(auth=auth)

    # Get tweets with required parameters
    number=180
    search_results = twitter_api.search.tweets(q=query,count=number,
                                               geocode=geocode,lang=lang)

    # Get the tweets' JSON objects
    statuses = search_results['statuses']

    df = pd.DataFrame(statuses, columns=['created_at','text',
                                         'retweet_count','favorite_count'])
    print (">>> Before removing duplicates: ", len(df))
    #Extracting texts from tweets and removing duplicates from it
    df = df.drop_duplicates('text', keep='first')
    print(">>> After removing duplicates: ", len(df))
    if len(df.index) == 0:
        return None
    df = df.rename(index=str, columns={"text": "raw_text"})

    # Removing links, special characters & translate if necessary
    regex = pickle.load(open('emoji_uni.pkl', 'rb'))
    #-----translate_client = translate.Client()
    if lang == 'en':
        df['clean_text'] = df['raw_text'].apply(lambda str: " ".join(re.sub("(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str).split()))
    #----else:
    #---    df['native_text'] = df['raw_text'].apply(lambda str: " ".join(re.sub(regex, " ", str).split()))
    #---    df['clean_text'] = df['native_text'].apply(lambda str: translate_client.translate(str, target_language='en')['translatedText'])


    # Get the polarity & set source
    nn = neural_network.NeuralNetwork('nn_model.h5')
    df['polarity'] = df['clean_text'].apply(lambda str: nn.predict([str])[0])
    df['source'] = 'Twitter'
    df_length = len(df)
    df.insert(loc=0, column='Number',value=range(1,df_length+1) )
    print(df)

    # Generate the word ladder
    tweets = df.loc[:, 'clean_text']
    all_text = tweets.str.cat(sep=' ').lower()
    all_words = pd.Series(all_text.split())
    with open('stopwords') as f:
        stopwords = set(f.read().strip().split('\n'))
        value_count = all_words.value_counts()
        value_labels = set(value_count.index) & stopwords  # Getting the stopwords in the Series
        top_word_count = value_count.drop(labels=value_labels)[:10]  # Removing labels with stopwords

    posttweet=df[df['polarity'] > 0.6 ]
    negtweet=df[df['polarity'] < 0.4 ]
    neutweet=df[(df['polarity'] >= 0.4) & (df['polarity'] <= 0.6)]

    positive=round((len(posttweet)*100/df_length), 2)
    negative=round((len(negtweet)*100/df_length),2)
    neutral=round((len(neutweet)*100/df_length),2)

    return (df_length, [len(posttweet), len(negtweet), len(neutweet)],
            [positive, negative, neutral], df, top_word_count)
