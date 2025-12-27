# language_agent/structured_query.py
#Try guess which comments i wrote, and which bossman wrote
# Ibr don't know what it does, but we can prolly come back to this!
import json
import time
import requests
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ValidationError
from .main_agent import LanguageAgent

#Guess which code might also have to be refactored entirely!!!!!

def create_strict_educational_schema() -> Dict[str, Any]:
    """
    Manually creates a JSON schema compliant with Cerebras strict mode requirements
    for the Educational content structure. 
    Again, if we choose to use gemini or another model, we will likely have to change this code
    """
    return {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "The main topic of the lecture segment"},
            "summary": {"type": "string", "description": "A concise summary of the content"},
            "key_concepts": {
                "type": "string", 
                "description": "Comma-separated list of key concepts defined in the text"
            },
            "quiz_question": {"type": "string", "description": "A practice question based on this content"}
        },
        "required": ["topic", "summary", "key_concepts", "quiz_question"],
        "additionalProperties": False
    }


class BaseStructuredModel(BaseModel):
    """Base class - kept for potential future use or inheritance."""
    class Config:
        json_schema_extra = {}


class LectureAnalysisModel(BaseModel):
    """
    Pydantic model for Lecture Analysis responses. Used for validation *after* receiving
    the strictly formatted JSON from the API.
    """
    topic: str = Field(..., description="The main topic of the lecture segment")
    summary: str = Field(..., description="A concise summary of the content")
    key_concepts: str = Field(..., description="Comma-separated list of key concepts")
    quiz_question: str = Field(..., description="A practice question based on this content")


class StructuredQueryEngine:
    """
    Engine for making structured queries using Cerebras' native JSON schema support.
    """

    def __init__(self, agent: LanguageAgent):
        self.agent = agent

    def query_with_structure(self,
                           prompt: str,
                           model_class: type, # Used for post-processing validation/fallback
                           system_prompt: Optional[str] = None,
                           max_retries: int = 2) -> BaseModel:
        """
        Query LLM with strict JSON schema enforcement.

        Args:
            prompt: The query prompt
            model_class: Pydantic model class for post-validation/fallback
            system_prompt: Optional system prompt
            max_retries: Max number of retries

        Returns:
            BaseModel: Validated structured response instance
        """
        # --- Use the manually created, Cerebras-compliant schema ---
        # We primarily rely on the API's strict mode, but keep model_class for fallback validation
        schema = create_strict_educational_schema()
        # --- End Schema ---

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # --- Prepare API payload with EXPLICIT strict=True ---
        payload = {
            "model": self.agent.current_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "lecture_analysis_schema", # Generic name, as schema is defined inline
                    "strict": True,                # <<< CRITICAL: Explicitly set to True >>>
                    "schema": schema               # Use the clean, manual schema
                }
            }
        }
        # --- End Payload ---

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    print(f"  Waiting 1.5s before retry {attempt}...")
                    time.sleep(1.5) # Slightly longer delay

                response_content = self._send_request(payload)

                if not response_content or not response_content.strip():
                    error_msg = f"Attempt {attempt + 1}: Received empty/whitespace response."
                    print(f"  Warning: {error_msg}")
                    last_exception = Exception(error_msg)
                    if attempt < max_retries:
                        print("  Retrying...")
                        continue
                    else:
                        print(f"  Returning default {model_class.__name__} due to persistent emptiness.")
                        return self._create_default_instance(model_class)

                # --- Attempt to parse JSON ---
                try:
                    response_data = json.loads(response_content)
                    print(f"  Raw API JSON response (Attempt {attempt + 1}): {response_content[:200]}...") # Debug log
                except json.JSONDecodeError as e:
                    error_msg = f"Attempt {attempt + 1}: JSON parsing failed: {e}. Raw: '{response_content[:200]}...'"
                    print(f"  Warning: {error_msg}")
                    last_exception = e
                    if attempt < max_retries:
                        print("  Retrying...")
                        continue
                    else:
                        print(f"  Returning default {model_class.__name__} due to persistent JSON errors.")
                        return self._create_default_instance(model_class)
                # --- End Parse ---

                # --- Validate using Pydantic model ---
                # Even though the API should enforce the schema, validate as a safety net.
                try:
                    # Use model_validate on the class itself
                    structured_response = model_class.model_validate(response_data)
                    print(f"  Successfully validated response for {model_class.__name__}")
                    return structured_response
                except ValidationError as ve:
                    error_msg = (f"Attempt {attempt + 1}: Pydantic validation failed *after* API response: {ve}. "
                                 f"Raw API response: '{response_content[:200]}...'")
                    print(f"  Warning: {error_msg}")
                    # This indicates the API didn't enforce the schema correctly or returned malformed JSON that looked valid
                    last_exception = ve
                    if attempt < max_retries:
                        print("  Retrying...")
                        continue
                    else:
                        print(f"  API returned invalid data despite strict=True. Returning default {model_class.__name__}.")
                        # Try to salvage the question if present
                        extracted_question = response_data.get('question', f"[Question not found. Raw API response: {response_content[:100]}...]")
                        return self._create_default_instance(model_class, question_override=extracted_question)

            except Exception as e:
                print(f"  Unexpected error during query attempt {attempt + 1}: {e}")
                last_exception = e
                if attempt < max_retries:
                    print("  Retrying...")
                else:
                    if last_exception:
                        raise last_exception
                    else:
                        raise

        if last_exception:
            raise last_exception
        raise Exception("Max retries exceeded.")

    def _create_default_instance(self, model_class: type, question_override: str = "Error: Topic unavailable.") -> BaseModel:
        """Helper to create a default model instance."""
        return model_class(
            topic=question_override,
            summary="Could not process content.",
            key_concepts="None",
            quiz_question="What is the main topic?"
        )

    def _send_request(self, payload: dict) -> Optional[str]:
        """Send request to LLM agent."""
        url = f"{self.agent.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.agent.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                error_info = response.text
                if response.status_code == 429:
                    print(f"API Rate Limit Error (429): {error_info}")
                elif response.status_code == 400:
                    print(f"API Bad Request Error (400): {error_info}")
                else:
                    print(f"API Error {response.status_code}: {error_info}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Network Request failed: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during request/response parsing: {e}")
            return None
