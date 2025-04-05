from flask import Flask, render_template, request
from groq_client import generate_recipe
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-123")

@app.route("/")
def index():
    """Render main input form"""
    return render_template("index.html")

@app.route("/recipes", methods=["POST"])
def process_recipes():
    """Handle recipe generation request"""
    ingredients = request.form.get("ingredients", "").strip()
    
    if not ingredients:
        return render_template("index.html", 
                            error="Please enter at least one ingredient")
    
    try:
        # Get and validate recipes
        result = generate_recipe(ingredients)
        recipes = result.get("recipes", [])
        
        if not recipes:
            raise ValueError("No recipes found in API response")
            
        # Process instructions formatting
        for recipe in recipes:
            if isinstance(recipe.get("instructions"), str):
                recipe["instructions"] = recipe["instructions"].replace("\\n", "\n")
                
        return render_template("recipes.html", recipes=recipes)
        
    except Exception as e:
        return render_template("index.html", 
                            error=f"Recipe generation failed: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)