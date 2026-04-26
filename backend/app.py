from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pickle

from recommend import recommend_recipes
from llm import format_with_llm

app = FastAPI(title="Cooking Recipe Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("../embeddings/recipe_embeddings.pkl", "rb") as f:
    df, vectorizer, X = pickle.load(f)

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/recommend")
def get_recipes(ingredients: str = Query(...)):

    try:
        results, scores, matched, missing = recommend_recipes(
            ingredients, df, vectorizer, X
        )

        output = []
        for i, (_, row) in enumerate(results.iterrows()):
            output.append({
                "name": row["name"].title(),
                "ingredients": row["ingredients"],
                "steps": row["steps"][:5],
                "score": scores[i],
                "matched": matched[i],
                "missing": missing[i][:3],
            })

        llm_result = format_with_llm(ingredients, output)

        return {
            "success": True,
            "recipes": output,
            "ai": llm_result
        }

    except Exception as e:
        return {"success": False, "message": str(e)}