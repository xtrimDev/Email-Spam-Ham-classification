import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import nltk

# Load Data
df = pd.read_csv("./dataset/spam.csv")
assert 'Message' in df.columns and 'Label' in df.columns, "Required columns are missing."

# Preprocessing
def clean_text(text):
    text = re.sub(r'[^\w\s]', ' ', text) 
    text = re.sub(r'\n', ' ', text)      
    text = re.sub(r'\d+', '', text)     
    return text.lower()

df['Message'] = df['Message'].apply(clean_text)

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def remove_stop_words(text):
    filtered_words = [word for word in text.split() if word.lower() not in stop_words]
    return ' '.join(filtered_words)

df['Message'] = df['Message'].apply(remove_stop_words)

# Feature Extraction
vectorizer = CountVectorizer() 
X_Message = vectorizer.fit_transform(df['Message'])
Message_df = pd.DataFrame.sparse.from_spmatrix(X_Message, columns=vectorizer.get_feature_names_out())

# Encode Labels
label_encoder = LabelEncoder()
df['Label'] = label_encoder.fit_transform(df['Label'])

# Save Vectorizer
joblib.dump(vectorizer, "./pickle/vectorizer.pkl")

# Split Data
X = Message_df
Y = df['Label']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

# Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "./pickle/model.pkl")

# Evaluate Model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
