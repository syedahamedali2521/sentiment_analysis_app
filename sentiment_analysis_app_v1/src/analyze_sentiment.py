from transformers import pipeline
from functools import lru_cache

@lru_cache(maxsize=1)
def get_pipeline():
    try:
        nlp = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
        return nlp
    except Exception as e:
        raise RuntimeError(f'Failed to load model: {e}')

def predict_text(text):
    nlp = get_pipeline()
    if isinstance(text, str):
        res = nlp(text[:512])[0]
        label = res.get('label', 'NEUTRAL')
        score = float(res.get('score', 0.0))
        if label == 'POSITIVE':
            sentiment = 'Positive'
        elif label == 'NEGATIVE':
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        return {'label': sentiment, 'score': score}
    else:
        raise ValueError('Input must be a string')

def predict_batch(texts):
    nlp = get_pipeline()
    results = []
    for t in texts:
        r = nlp(t[:512])[0]
        label = r.get('label','NEUTRAL')
        score = float(r.get('score',0.0))
        sentiment = 'Positive' if label=='POSITIVE' else 'Negative' if label=='NEGATIVE' else 'Neutral'
        results.append({'text': t, 'label': sentiment, 'score': score})
    return results
