import pytest
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def test_sentiment_positive():
    analyzer = SentimentIntensityAnalyzer()
    text = "This is a great day for the stock market!"
    score = analyzer.polarity_scores(text)["compound"]
    assert score > 0

def test_sentiment_negative():
    analyzer = SentimentIntensityAnalyzer()
    text = "This is the worst crash in years."
    score = analyzer.polarity_scores(text)["compound"]
    assert score < 0