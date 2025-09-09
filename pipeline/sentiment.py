import argparse
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores['compound']

def main(input_file, output_file):
    df = pd.read_csv(input_file)
    df["sentiment"] = df["summary"].astype(str).map(analyze_sentiment)
    df.to_csv(output_file, index=False)
    print(f"Saved sentiment to {output_file}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.input, args.output)