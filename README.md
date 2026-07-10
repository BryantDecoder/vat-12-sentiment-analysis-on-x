# VAT 12% Sentiment Analysis
# Sentiment Analysis of Public Opinion on Indonesia's 12% VAT Policy Using IndoBERT-BiLSTM

This project is a web-based sentiment analysis application developed as part of an undergraduate thesis. The application classifies public sentiment toward Indonesia's 12% VAT policy into Positive, Neutral, and Negative categories using a hybrid IndoBERT-BiLSTM model. The application supports both single-text prediction and CSV dataset analysis.

## Features

- Single text sentiment prediction
- CSV dataset sentiment analysis
- Automatic text preprocessing
- Confidence score prediction
- Interactive visualization
- Download prediction results as CSV

project/
│
├── app.py
├── assets/
├── data/
├── utils/
├── views/
├── requirements.txt
└── README.md

## Installation

Clone repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run application

```bash
streamlit run app.py
```

## Usage

### Input Text

- Enter a sentence.
- Click **Analyze**.
- View predicted sentiment and confidence score.

### Upload Dataset

- Upload a CSV file containing a **text** column.
- Click **Run AI Model**.
- Download the prediction results.

## Live Demo

https://vat12-sentiment.streamlit.app

## Model

Hybrid IndoBERT-BiLSTM

- Transformer : IndoBERT Base
- Hidden Size : 256
- Max Length : 128
- Output : Positive, Neutral, Negative

## Dataset

The dataset contains public posts collected from X (Twitter) discussing Indonesia's 12% VAT policy.

Labels:
- Positive
- Neutral
- Negative

## Performance

Val F1-Macro : 0,8209
Test Accuracy : 87,50%
Test F1-Macro : 83,63%

## Authors

- Bryant Alfronso Purba
- Roy Jannes Simbolon
- Samuel Natalino Sitorus

Faculty of Informatics

Universitas Mikroskil

## License

This project is developed for academic purposes.