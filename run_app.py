from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
import pandas as pd
import os
import numpy as np
from figures import *

import streamlit as st
# set configs
st.set_option('server.headless', 'true')
st.set_option('browser.serverAddress', '0.0.0.0')
st.set_option('browser.gatherUsageStats', 'false')

# ---------------------
# Read the model
# ---------------------
@st.cache(ignore_hash=True)
def load_model(path):
    glove_file = datapath(path)
    tmp_file = get_tmpfile("glove_word2vec.txt")

    _ = glove2word2vec(glove_file, tmp_file)

    model = KeyedVectors.load_word2vec_format(
        tmp_file,
        binary=False
    )

    return model

# ---------------------
# Common part
# ---------------------
st.sidebar.title('GloVe Twitter')
st.sidebar.markdown("""
GloVe is an unsupervised learning algorithm for obtaining vector representations for words. Pretrained on 
2 billion tweets with vocabulary size of 1.2 million. Download from [Stanford NLP](http://nlp.stanford.edu/data/glove.twitter.27B.zip). 

Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. *GloVe: Global Vectors for Word Representation*.
""")

model_type = st.sidebar.selectbox(
    'Choose the model',
    ('25d', '50d', '100d', '200d'),
    index=3
)
# load the model
dir_path = os.path.dirname(os.path.realpath(__file__))
model = load_model(dir_path + '/glove.twitter.27B.%s.txt' % model_type)

# -------------------------
# Choose option
# -------------------------
option = st.sidebar.selectbox(
    'Task type',
    ('Compare weights','Most similar'),
    index=1
)

if option == 'Most similar':

    st.title('Most similar')

    word = st.text_input(
        'Type your word',
        value='dog'
    )
    title = 'Most similar to %s' % word.upper()
    # run gensim
    try:
        ret = model.wv.most_similar(
            positive=word,
            topn=10
        )
    except Exception as e:
        ret = None
        st.markdown('Ups! The word **%s** is not in dictionary.' % word)

    if ret is not None:
        # convert to pandas
        data = pd.DataFrame(ret, columns=['word','distance'])

        chart = render_most_similar(data, title)
        st.altair_chart(chart)

elif option == 'Compare weights':

    st.title('Compare weights')

    word1 = st.text_input(
        'First word',
        'dog'
    )
    word2 = st.text_input(
        'Second word',
        'cat'
    )
    try:
        vec1 = model.wv.word_vec(word1, use_norm=True)
        vec2 = model.wv.word_vec(word2, use_norm=True)

        data = pd.DataFrame(
            {
                'word': [word1] * len(vec1) + [word2] * len(vec2),
                'x': list(range(0, len(vec1))) + list(range(0, len(vec2))),
                'weight': np.concatenate((vec1, vec2), axis=0)
            }
        )

        chart = render_compare(data)
        st.altair_chart(chart)

        data = pd.DataFrame({
            'index': list( range(0,len(vec1)) ),
            'weight': np.abs(vec1-vec2)
        })

        chart = render_absolute_compare(data)
        st.altair_chart(chart)
    except:
        st.markdown('Ups! One of the words is not present in dictionary.')