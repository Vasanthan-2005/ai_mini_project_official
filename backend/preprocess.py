import pandas as pd
import ast

def load_and_clean_data(path):
    df = pd.read_csv(path)

    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
    df['steps'] = df['steps'].apply(ast.literal_eval)

    df = df[df['steps'].apply(lambda x: len(x) > 0)]
    df = df[df['name'].str.lower() != 'please ignore']

    df = df.drop_duplicates(subset=['name'])

    df['ingredients_text'] = df['ingredients'].apply(
        lambda x: " ".join(x).lower()
    )

    df['ingredients_set'] = df['ingredients'].apply(
        lambda x: set([i.lower() for i in x])
    )

    df = df.dropna()

    return df