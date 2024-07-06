import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json
from simple_chalk import chalk

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('dslim/bert-base-NER')
model = AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')
nlp = pipeline("ner",model=model,tokenizer=tokenizer)

def NERinferenceAPI(datas):
    NER_tags = []
    for index, data in enumerate(datas):
        print(chalk.red(index), ":", chalk.green('Here'))
        if index != 0:
            continue
        # # Tokenize input text
        # inputs = tokenizer(data['article'], return_tensors='pt', truncation=True, padding=True)
        
        # # Perform NER inference
        # with torch.no_grad():
        #     outputs = model(**inputs)
        #     logits = outputs.logits
        
        # # Convert logits to probabilities
        # predictions = torch.softmax(logits, dim=-1)
        
        # # Get the predicted labels (assuming NER tagging)
        # predicted_ids = torch.argmax(predictions, dim=-1)
        # predicted_tags = [model.config.id2label[tag_id] for tag_id in predicted_ids.tolist()[0]]
        
        try:
            print(chalk.magenta(data['article']))
            predicted_tags = nlp(data['article'])
            print(chalk.green(predicted_tags))
        except:
            continue

        # Prepare JSON data
        jsonData = {
            'url': data['url'],
            'NER_tags': predicted_tags
        }
        
        NER_tags.append(jsonData)
    
    return NER_tags