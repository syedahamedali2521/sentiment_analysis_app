from src.analyze_sentiment import predict_text

if __name__ == '__main__':
    sample = "I absolutely love this! It's fantastic and works as expected."
    r = predict_text(sample)
    print(r)
