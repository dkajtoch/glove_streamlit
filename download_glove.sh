#!/bin/sh

wget -c http://nlp.stanford.edu/data/glove.twitter.27B.zip \
    && unzip glove.twitter.27B.zip \
    && rm glove.twitter.27B.zip