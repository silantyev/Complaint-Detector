import numpy as np
import os
import tensorflow as tf
from transformers import DistilBertConfig, TFDistilBertModel
from transformers import DistilBertTokenizer
from transformers import logging
from tensorflow.keras.layers import BatchNormalization, Dense, Average, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC

from .helpers import module_path

logging.set_verbosity_error()

def create_tokenizer():
    distil_bert = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(
        distil_bert, do_lower_case=True, add_special_tokens=True,
        max_length=128, pad_to_max_length=True
    )
    return tokenizer

def create_model(input_shape):
    
    distil_bert = 'distilbert-base-uncased'
    config = DistilBertConfig(dropout=0.2, attention_dropout=0.2)
    config.output_hidden_states = False
    transformer_model = TFDistilBertModel.from_pretrained(distil_bert, config = config)

    input_ids_in = Input(shape=input_shape, name='input_token', dtype='int32')
    input_masks_in = Input(shape=input_shape, name='masked_token', dtype='int32') 

    embedding_layer = transformer_model(input_ids_in, attention_mask=input_masks_in)[0]
    cls_token = embedding_layer[:,0,:]
    
    outs = list()
    for fold in range(3):
        b0 = BatchNormalization(name='b0_{}'.format(fold))(cls_token)
        d0 = Dense(128, activation='relu', name='d0_{}'.format(fold))(b0)
        out = Dense(1, activation='sigmoid', name='out_{}'.format(fold))(d0)
        outs.append(out)
        
    global_out = Average()(outs)
    
    model = Model(inputs=[input_ids_in, input_masks_in], outputs=global_out)
        
    weights_path = module_path() + '/weights'
    for fold in range(3):
        for lname in ['b0','d0','out']:
            fnames = [fname for fname in os.listdir(weights_path) if (fname.startswith('{}_{}'.format(lname,fold))) and (fname.endswith('npy'))]
            fnames.sort()
            weights = list()
            for i, fname in enumerate(fnames):
                weights.append(np.load('{}/{}'.format(weights_path, fname)))
            model.get_layer('{}_{}'.format(lname, fold)).set_weights(weights)

    for layer in model.layers:
        layer.trainable = False
        
    model.compile(
        optimizer = Adam(lr=0.001),
        loss = 'binary_crossentropy',
        metrics=[AUC(name='auc')]
    )
    
    return model