from google import genai
from google.genai import types
from app.core.config import settings
import requests
import json


class GeminiService:
    def __init__(self):
        self.client = genai.Client()

    async def analyze_image(self, file_content: bytes, mime_type: str):
        prompt = """
        Analyze the provided image and return the answer in.
        Identify if it is a "medical prescription" (receta medica) or a "legal document" (documento legal).
        Provide a brief explanation of the document content.
        Return the result in JSON format with the following keys:
        - type: "medical_prescription" or "legal_document" or "other"
        - explanation: A brief explanation of the document in spanish.
        - extracted_text: (Optional) Any key text extracted from the document to help with the query.
        """

        image = types.Part.from_bytes(
            data=file_content,
            mime_type=mime_type,
        )

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, image],
        )

        try:
            # Clean up the response text to ensure it's valid JSON
            text_response = response.text.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                text_response = text_response[3:-3]

            result = json.loads(text_response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "type": "unknown",
                "explanation": "Could not parse Gemini response.",
                "raw_response": response.text,
            }

        if result.get("type") == "legal_document":
            # Call external API
            external_response = self._call_legal_copilot(
                result.get("extracted_text", "") or result.get("explanation", "")
            )
            result["legal_copilot_response"] = external_response

        return result

    def _call_legal_copilot(self, query_text: str):
        url = settings.LEGAL_COPILOT_API_URL
        payload = {
            "query": f"Analyze this legal document context: {query_text}",
            "top_k": 5,
            "score_threshold": 0.3,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to call legal copilot: {str(e)}"}


gemini_service = GeminiService()
