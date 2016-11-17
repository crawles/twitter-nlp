import numpy as np
import random
import time

def sse_pack(d):
    """Pack data in SSE format.
       Source: https://taoofmac.com/space/blog/2014/11/16/1940"""
    buffer = ''
    for k in ['retry','id','event','data']:
        if k in d.keys():
            buffer += '{}: {}\n'.format(k, d[k])
    return buffer + '\n'

def polarity_prob2class(p, pol_thresh = [.2,.8]):
    """Convert 0-1 to pos,nue,neg"""
    pol_thresh[0]
    if p <= pol_thresh[0]:
        color = '#CD0F15'
        pclass = 'neg'
    elif p >= pol_thresh[1]:
        color = '#3ECD0F'
        pclass = 'pos'
    else:
        color = '#838682'
        pclass = 'neu'
    #pclass += '{:2.2f}'.format(p)
    return '<font color="{}">{}</font>'.format(color,pclass)


def polarity_meets_criteria(polarity, threshs = [0.2,0.8]):
    polar_tweet = (polarity > threshs[1]) or (polarity < threshs[0])
    neutral_tweet = (0.4 < polarity < 0.6) 
    randomness = random.random() <= 0.01
    if polar_tweet or (neutral_tweet and randomness):
        return True
    return False

def last_m_seconds(m,times,n):
    del_times = time.time() - times
    ix = np.where(del_times <= m)
    return times[ix],n[ix]

def get_tweets_per_m_seconds(times,n):
    del_time = times[0] - times[-1]
    del_n    = n[0] - n[-1]
    return del_n/del_time

