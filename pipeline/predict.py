import argparse
import pandas as pd

def predict_sentiment(df):
    # Dummy prediction logic: classify as positive if sentiment > 0, else negative
    return df["sentiment"].apply(lambda x: "positive" if x > 0 else "negative")

def main(input_file, output_file):
    df = pd.read_csv(input_file)
    df["prediction"] = predict_sentiment(df)
    df.to_csv(output_file, index=False)
    print(f"Saved predictions to {output_file}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.input, args.output)