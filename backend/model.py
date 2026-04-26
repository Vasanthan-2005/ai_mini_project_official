from sklearn.feature_extraction.text import TfidfVectorizer

def create_vectorizer(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['ingredients_text'])
    return vectorizer, X