from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


import joblib
model = joblib.load("./prediction/pickle/model.pkl")
vectorizer = joblib.load("./prediction/pickle/vectorizer.pkl")


import re
def clean_text(text):
    text = re.sub(r'[^\w\s]', ' ', text) 
    text = text.replace('\n', ' ')      
    text = re.sub(r'\d+', '', text)  
    text = text.lower()        
    return text


def remove_stop_words(text):
    words = text.split() 
    filtered_words = []  

    for word in words:   
        if word.lower() not in stop_words: 
            filtered_words.append(word)   

    return ' '.join(filtered_words)


@app.route("/predict", methods=['POST'])
def predict():
    try:
        input_text = request.json.get('message')
        if not input_text:
            return jsonify({"error": "No input text provided."}), 400

        cleaned_text = clean_text(input_text)
        processed_text = remove_stop_words(cleaned_text)

        vectorized_text = vectorizer.transform([processed_text])

        probas = model.predict_proba(vectorized_text) 

        predicted_class = model.predict(vectorized_text)[0]
        predicted_probability = probas[0][predicted_class]  
        confidence_percentage = predicted_probability * 100

        return jsonify({
            "prediction": int(predicted_class),
            "confidence": round(confidence_percentage, 2) 
        })

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({
            "prediction": 0,
            "confidence": 50 
        })

if __name__ == '__main__':
    app.run(debug=True)
