import numpy as np

from .helpers import clean_tweet
from .model import create_model, create_tokenizer

class ComplaintDetector():
    
    def __init__(self):

        self.tokenizer = create_tokenizer()
        input_shape = (128,)
        self.model = create_model(input_shape)
        return
    
    def clean(self, x):
        x = np.asarray(x)
        f = np.vectorize(clean_tweet)
        return f(x)
    
    def tokenize(self, x):
        input_ids, input_masks, input_segments = [],[],[]
        for sentence in x:
            inputs = self.tokenizer.encode_plus(
                sentence, add_special_tokens=True, max_length=128, pad_to_max_length=True, 
                return_attention_mask=True, return_token_type_ids=True
            )
            input_ids.append(inputs['input_ids'])
            input_masks.append(inputs['attention_mask'])
            input_segments.append(inputs['token_type_ids'])        
        
        return np.asarray(input_ids, dtype='int32'), np.asarray(input_masks, dtype='int32'), np.asarray(input_segments, dtype='int32')
    
    def predict(self, x):
        
        x = self.clean(x)
        x = self.tokenize(x)[:2]
        return self.model.predict(x)[:,0]
    
    def evaluate(self, x, y):
        x = self.clean(x)
        x = self.tokenize(x)
        return self.model.evaluate(x)
        