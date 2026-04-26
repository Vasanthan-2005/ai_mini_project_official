import pickle
import os
from preprocess import load_and_clean_data
from model import create_vectorizer

def build_and_save():
    df = load_and_clean_data("../data/recipes.csv")
    df = df.head(100)
    vectorizer, X = create_vectorizer(df)

    os.makedirs("../embeddings", exist_ok=True)

    with open("../embeddings/recipe_embeddings.pkl", "wb") as f:
        pickle.dump((df, vectorizer, X), f)

    print("Embeddings stored successfully!")

if __name__ == "__main__":
    build_and_save()