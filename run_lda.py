'''
This code is part of the publication "Who Let The Trolls Out? Towards Understanding State-Sponsored Trolls" (https://arxiv.org/abs/1811.03130).
If you use this code please cite the publication.
'''


# LDA stuff
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import pandas as pd
tokenizer = RegexpTokenizer(r'\w+')
from html.parser import HTMLParser
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    tweet2 = strip_urls_spchr(tweet)
    return ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet2).split())
# method that strips urls and special characters from a given text
def strip_urls_spchr(text):
    text = HTMLParser().unescape(text)
    return re.sub(r'https?:\/\/.*', '', text).strip()
# load the new data
russians_df_all = pd.read_csv('./data/ira_tweets_csv_hashed.csv')
iranians_df_all = pd.read_csv('./data/iranian_tweets_csv_hashed.csv')


# load the dataset from Reddit
submissions_trolls = pd.read_json('./data/reddit_troll_submissions.txt', lines=True)
comments_trolls = pd.read_json('./data/reddit_troll_comments.txt', lines=True)
submissions_trolls['is_submission'] = True
comments_trolls['is_comment'] = True
russians_reddit = pd.concat([submissions_trolls, comments_trolls])
russians_reddit['datetime'] = pd.to_datetime(russians_reddit['created_utc'], unit='s')

russians = russians_df_all[russians_df_all.tweet_language=='en']
iranians = iranians_df_all[iranians_df_all.tweet_language=='en']


russians['clean_text'] = russians['tweet_text'].map(clean_tweet)
doc_set_all_russians = russians['clean_text'].tolist()
doc_set_all_russians2 = [x for x in doc_set_all_russians if len(x)>3]
iranians['clean_text'] = iranians['tweet_text'].map(clean_tweet)

doc_set_all_iranians = iranians['clean_text'].tolist()
doc_set_all_iranians2 = [x for x in doc_set_all_iranians if len(x)>3]


texts_reddit = []
for index, row in submissions_trolls.iterrows():
    texts_reddit.append(clean_tweet(row['title'] + ' ' + row['selftext']))
for index, row in comments_trolls.iterrows():
    texts_reddit.append(clean_tweet(row['body']))


def find_topics_and_save_words(doc_set, model_path,  path, num_passes):
    # list for tokenized documents in loop
    texts = []
    
    # loop through document list
    for i in doc_set:
        
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop and len(i)>2]
        
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        texts.append(stopped_tokens)
    
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
        
    # convert tokenized documents into a document-term matrix
    corpus_org = [dictionary.doc2bow(text) for text in texts]
    
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus_org, num_topics=10, id2word = dictionary, chunksize=10000, update_every=1, passes=num_passes)
    ldamodel.save(model_path)
    print(ldamodel.print_topics(num_topics=10, num_words=10))
    topics_org = []
    lda_topics = ldamodel.print_topics(num_topics=10, num_words=10)
    for topic in lda_topics:
        words = []
        elements = topic[1].split('+')
        for i in range(len(elements)):
            topic_word = elements[i].split('*')[-1].replace('\'', '').replace('"', '').replace(' ', '').replace('_', '')
            words.append(topic_word)
        topics_org.append(','.join(words))
        
    print(topics_org)
    
            
    with open(path, 'w') as f:
        for top in topics_org:
            f.write(top + '\n')
    return ldamodel
            
print("Russians LDA......")
lda_model_russians = find_topics_and_save_words(doc_set_all_russians2, 'model_lda_russians_all','./topics_russians.txt', 5)
print("Iranians LDA......")
lda_model_iranians = find_topics_and_save_words(doc_set_all_iranians2, 'model_lda_iranians_all', './topics_iranians.txt', 5)
print("Russians Reddit LDA......")
lda_model_russians_reddit = find_topics_and_save_words(texts_reddit, 'model_lda_russians_reddit', './topics_russians_reddit.txt', 10)


