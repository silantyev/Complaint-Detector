# Complaint Detector
This repository provides a model that detects the probability of complaint in a short text using modern NLP techniques. The model was trained on the tweets and recommended to be used on short messages from social media.

## Quick Start
### 1. Install the module
```
pip install git+https://www.github.com/silantyev/Complaint-Detector.git
```
### 2. Import the class from the module
```python
from complaint_detector import ComplaintDetector
```
### 3. Create a detector and predict the probability of complaint in your data


#### A. Using a list of strings
```python
cd = ComplaintDetector()
cd.predict([
    'My mobile phone is too slow',
    'My laptop is the best'
])
```

#### B. Using a pandas.Series
```python
import pandas as pd
cd = ComplaintDetector()
df = pd.read_csv('sample.csv')
pred = cd.predict(df['Text'])
```

#### C. You can use any iterable of strings.

## Content

* **complaint_detector/** - The module directory.
* **tutirial.ipynb** - Jupyter notebook with the examples.

## Prerequisites
The module requires the following packages installed:
* numpy >= 1.19.5
* unidecode >= 1.2.0
* tensorflow 2.5.2
* transformers 4.12.3

Older versions may also work, but it's not guaranteed.

## About the model
* The model uses DistilBERT pre-trained model as a feature extractor with one Batch Normalization layer and 2 Dense layers on top of that trained on a smaller dataset.
* Dataset consists of 3,499 rows taken from this repository (https://github.com/danielpreotiuc/complaints-social-media/) and 1,713 rows labeled by ourselves. In both cases, Twitter was used as a source of texts. Total size is 5,212; 1,480 rows have positive labels (1 - Complaint) and 3,732 negative labels (0 - Non-complaint).
* While DistilBERT layers were set non-trainable, another part of the network was trained with the data split into 3 folds. ROC-AUC metric for validation data varied in range from 0.901 to 0.914.
    
