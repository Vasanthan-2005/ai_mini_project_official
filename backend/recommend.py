import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def normalize(text):
    corrections = {
        "veggis": "vegetable",
        "veggies": "vegetable"
    }

    words = text.lower().replace(",", " ").split()

    return set([
        corrections.get(w, w.rstrip('s'))
        for w in words
    ])


def recommend_recipes(user_input, df, vectorizer, X, top_n=5):

    if not user_input or user_input.strip() == "":
        raise ValueError("Please enter at least one ingredient")

    user_list = user_input.lower().replace(",", " ").split()
    user_words = normalize(user_input)

    if len(user_words) == 0:
        raise ValueError("Invalid input")

    primary_ingredient = user_list[0] if user_list else None

    # -------- Filter recipes (fuzzy match for primary ingredient) --------
    if primary_ingredient:
        candidate_df = df[df["ingredients_set"].apply(
            lambda x: any(primary_ingredient in ing for ing in x)
        )]

        if len(candidate_df) == 0:
            candidate_df = df
    else:
        candidate_df = df

    # Reset index to avoid mismatch
    candidate_df = candidate_df.reset_index(drop=True)

    # -------- Compute similarity --------
    user_vec = vectorizer.transform([" ".join(user_words)])
    X_subset = vectorizer.transform(candidate_df["ingredients_text"])

    similarity = cosine_similarity(user_vec, X_subset).flatten()

    top_indices = np.argsort(similarity)[::-1][:50]

    scored_results = []

    # -------- Scoring --------
    for idx in top_indices:
        recipe = candidate_df.iloc[idx]
        recipe_ingredients = recipe["ingredients_set"]

        common = user_words.intersection(recipe_ingredients)
        common_count = len(common)

        if common_count == 0:
            continue

        # Ensure primary ingredient is present
        if primary_ingredient:
            has_primary = any(primary_ingredient in ing for ing in recipe_ingredients)
            if not has_primary:
                continue

            # If multiple inputs → require stronger match
            if len(user_words) > 1 and common_count < 2:
                continue

        missing = list(recipe_ingredients - user_words)
        missing_count = len(missing)

        ingredient_score = common_count / len(user_words)
        recipe_coverage = common_count / len(recipe_ingredients)

        final_score = (
            (ingredient_score * 0.6) +
            (recipe_coverage * 0.3) +
            (similarity[idx] * 0.1)
        )

        penalty = missing_count * 0.03
        final_score -= penalty

        scored_results.append({
            "recipe": recipe,
            "score": final_score,
            "matched": list(common),
            "missing": missing
        })

    scored_results = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    top_results = scored_results[:top_n]

    if len(top_results) == 0:
        raise ValueError("No matching recipes found")

    results = [r["recipe"] for r in top_results]
    scores = [round(r["score"] * 100, 2) for r in top_results]
    matched = [r["matched"] for r in top_results]
    missing = [r["missing"] for r in top_results]

    return pd.DataFrame(results), scores, matched, missing