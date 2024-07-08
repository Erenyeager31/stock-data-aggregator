import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification
import json
from simple_chalk import chalk

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
model = RobertaForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

# Define sentiment labels
sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}

def sentiment_analysis(datas):
    sentiments = []
    for index, data in enumerate(datas):
        print(chalk.red(str(index)), ":", chalk.green('Processing'))
        try:
            article = data['article']
            
            inputs = tokenizer(article, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            sentiment = torch.argmax(predictions).item()
            
            sentiment_label = sentiment_labels.get(sentiment, 'Unknown')
            sentiments.append({
                'article': article,
                'sentiment': sentiment_label
            })
            
            print(chalk.blue(f"Sentiment: {sentiment_label}"))
        except Exception as e:
            print(chalk.red(f"Error processing article {index}: {e}"))
            continue
    
    return {
        'status':True,
        'message': 'Sentiment analysis completed',
        'results': sentiments
    }