import csv
import joblib
import json
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

    return reviews


# Read json
file_name = 'imdb_reviews_tt8421350.json'

json_data = json.load(open(file_name, 'r'))

all_reviews = []
all_date = []

for key in json_data:
    review = json_data[key]
    all_date.append(review['Date'])
    all_reviews.append(review['Text'])

text_data_clean = preprocess_reviews(all_reviews)

model = joblib.load('model.pkl')

out_filename = 'output_tt8421350_sentiment.csv'

out_prob = model.predict_proba(text_data_clean)

with open(out_filename, 'w') as out_file:
    fieldnames = ['Review No', 'Review Date', 'Positive Sentiment Score', 'Negative Sentiment Score']
    writer = csv.DictWriter(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
    writer.writeheader()
    for i, output in enumerate(out_prob):
        print(output)
        print(all_date[i])
        writer.writerow({'Review No': str(i), 'Review Date': str(all_date[i]),
                         'Positive Sentiment Score': str(output[1]),
                         'Negative Sentiment Score': str(output[0])})
