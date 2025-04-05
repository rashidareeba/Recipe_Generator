from groq import Groq
import os
import json
from typing import Dict, List

def generate_recipe(ingredients: str) -> Dict[str, List[Dict]]:
    """
    Generates recipes using Groq API with structured JSON response
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    Generate 3 creative recipes using some of these ingredients: {ingredients}.
    Respond ONLY with valid JSON containing:
    - recipe name
    - ingredients (mark user-provided ones)
    - clear step-by-step instructions
    - cooking time
    - difficulty level
    
    Use this exact JSON structure:
    {{
        "recipes": [
            {{
                "name": "Recipe Name",
                "ingredients": [
                    {{"name": "ingredient1", "user_provided": true}},
                    {{"name": "ingredient2", "user_provided": false}}
                ],
                "instructions": "1. Step one\\n2. Step two",
                "time": "XX mins",
                "difficulty": "Easy/Medium/Hard"
            }}
        ]
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional chef. Respond only with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        # Validate and parse response
        response = json.loads(completion.choices[0].message.content)
        if not isinstance(response.get("recipes"), list):
            raise ValueError("Invalid recipe format received")
            
        return response
        
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"API request failed: {str(e)}")