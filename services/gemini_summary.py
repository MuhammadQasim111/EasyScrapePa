import google.generativeai as genai
import os
import json

class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp') # Using 2.0 Flash as requested/available
        else:
            self.model = None

    def is_available(self):
        return self.model is not None

    def summarize(self, text):
        if not self.model:
            return "Gemini API Key not provided."
        
        try:
            prompt = f"Summarize the following text in 3-5 bullet points:\n\n{text[:10000]}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def extract_entities(self, text):
        if not self.model:
            return {}
        
        try:
            prompt = f"""
            Extract the following entities from the text if present: 
            - Names
            - Emails
            - Phone Numbers
            - Products/Prices
            
            Return as JSON.
            
            Text: {text[:10000]}
            """
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}
