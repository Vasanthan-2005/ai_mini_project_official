import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [recipes, setRecipes] = useState([]);
  const [aiResult, setAiResult] = useState(null); // 🔥 NEW
  const [loading, setLoading] = useState(false);

  const fetchRecipes = async () => {
    if (!input.trim()) {
      alert("Please enter ingredients");
      return;
    }

    try {
      setLoading(true);

      const res = await axios.get("http://127.0.0.1:8000/recommend", {
        params: { ingredients: input },
      });

      if (res.data.success) {
        setRecipes(res.data.recipes);
        setAiResult(res.data.ai); // 🔥 STORE AI OUTPUT
      } else {
        setRecipes([]);
        setAiResult(null);
        alert(res.data.message);
      }
    } catch (error) {
      console.error(error);
      alert("Server error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.app}>
      <h1>👨‍🍳 Cooking Recipe Assistant</h1>

      {/* 🔍 Search */}
      <div style={styles.searchBox}>
        <input
          type="text"
          placeholder="Enter ingredients (e.g. chicken, salt, oil)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
        />

        <button onClick={fetchRecipes} disabled={loading} style={styles.button}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {/* ⏳ Loading */}
      {loading && <p style={{ color: "orange" }}>⏳ Searching recipes...</p>}

      {/* 🤖 AI RESULT */}
      {!loading && aiResult && (
        <div style={styles.aiBox}>
          <h2>🤖 AI Recommendation</h2>

          <h3>⭐ {aiResult.best_recipe}</h3>

          <p>
            <b>Why:</b> {aiResult.why}
          </p>

          <p>
            ❌ <b>Missing:</b>{" "}
            {aiResult.missing_ingredients?.length > 0
              ? aiResult.missing_ingredients.join(", ")
              : "None"}
          </p>

          <h4>📋 Steps</h4>
          <ol>
            {aiResult.steps?.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>

          {aiResult.tips && (
            <p>
              💡 <b>Tips:</b> {aiResult.tips}
            </p>
          )}
        </div>
      )}

      {/* ❌ No results */}
      {!loading && recipes.length === 0 && (
        <p style={{ color: "red" }}>No recipes found</p>
      )}

      {/* 🍗 Results */}
      <div style={styles.container}>
        {recipes.map((recipe, index) => (
          <div key={index} style={styles.card}>
            {index === 0 && (
              <h3 style={{ color: "green" }}>⭐ Best Match</h3>
            )}

            <h2>{recipe.name}</h2>
            <p>
              <b>Match:</b> {recipe.score}%
            </p>

            <p>
              ✅ <b>Available:</b> {recipe.matched.join(", ")}
            </p>
            <p>
              ❌ <b>Missing:</b> {recipe.missing.join(", ")}
            </p>

            <h4>🍴 Ingredients</h4>
            <ul>
              {recipe.ingredients.map((ing, i) => (
                <li key={i}>{ing}</li>
              ))}
            </ul>

            <h4>📋 Steps</h4>
            <ol>
              {recipe.steps.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ol>
          </div>
        ))}
      </div>
    </div>
  );
}

/* 🎨 Styles */
const styles = {
  app: {
    textAlign: "center",
    padding: "30px",
    fontFamily: "Arial",
    backgroundColor: "#f5f5f5",
    minHeight: "100vh",
  },
  searchBox: {
    marginBottom: "20px",
  },
  input: {
    padding: "10px",
    width: "300px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 15px",
    marginLeft: "10px",
    border: "none",
    backgroundColor: "#ff6b6b",
    color: "white",
    borderRadius: "5px",
    cursor: "pointer",
  },
  container: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
  },
  card: {
    width: "300px",
    background: "white",
    margin: "15px",
    padding: "15px",
    borderRadius: "10px",
    textAlign: "left",
    boxShadow: "0px 2px 8px rgba(0,0,0,0.1)",
  },

  // 🔥 NEW AI BOX
  aiBox: {
    background: "#fff3cd",
    margin: "20px auto",
    padding: "20px",
    borderRadius: "10px",
    maxWidth: "700px",
    textAlign: "left",
    boxShadow: "0px 2px 8px rgba(0,0,0,0.1)",
  },
};

export default App;