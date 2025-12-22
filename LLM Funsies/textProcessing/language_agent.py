import os
import requests
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

# @dataclass
# class ChatMessage:
#     """
#     Represents a single message in a chat sequence.
#     """
#     role: str  # "user", "assistant", "system"
#     content: str
#     timestamp: str  # ISO format string
#     model: Optional[str] = None

# Note: This is code needs to be changed; my proposal is that we start off by either using the geminiApi, or we use a small llm
# For example, there's the ibm granite nano which is small enough that theoretically you wouldn't even need to deal with api issues, as the user can run it 
#but that may limit the usage to PC only, now that i think about that... Equally, we could 
# temporarily just use the gemini free api as we develop, and that should be fine.
# I used qwen in this example, but we prolly should decide sooner than later.

#Here is the core of the program tho where we actually load our agent

class LanguageAgent:
    def __init__(self, api_key: str, base_url: str = "https://api.cerebras.ai", default_model: str = "qwen-3-235b-a22b-thinking-2507"):
        """
        Initialize the LanguageAgent with API credentials and default model.

        Args:
            
            base_url (str): Base API endpoint (default: Cerebras assumed URL)
            default_model (str): Default model to use if not changed
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.current_model: Optional[str] = None  # Will be set after model list check
        self.available_models: List[str] = []
        self.default_model = default_model

        # Validate API key
        if not self.api_key:
            raise ValueError("API key is required.")

        # Fetch available models to validate connectivity and set current model
        if self.list_models():
            if default_model in self.available_models:
                self.current_model = default_model
            else:
                print(f"Warning: Default model '{default_model}' not in available models.")
                print(f"Using first available model: {self.available_models[0]}")
                self.current_model = self.available_models[0]
        else:
            raise ConnectionError("Failed to retrieve model list. Check API key and connectivity.")

    def list_models(self) -> bool:
        """
        Fetches the list of available models from the Cerebras API.

        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/v1/models"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Assume OpenAI-style response: { "data": [ { "id": "model-name" }, ... ] }
                self.available_models = [item["id"] for item in data.get("data", [])]
                print("Available models:")
                for model in self.available_models:
                    print(f"  - {model}")
                return True
            else:
                print(f"Error listing models: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Request failed during model listing: {e}")
            return False

    def change_model(self, model_name: str) -> bool:
        """
        Switch the active model.

        Args:
            model_name (str): Name of the model to switch to

        Returns:
            bool: True if model is available and changed, False otherwise
        """
        if model_name not in self.available_models:
            print(f"Error: Model '{model_name}' is not available.")
            print("Available models:", ", ".join(self.available_models))
            return False
        self.current_model = model_name
        print(f"Model changed to: {self.current_model}")
        return True

    def send_message(self, content: str) -> Optional[str]:
        """
        Send a message to the currently selected model and print the response.

        Args:
            content (str): User message to send

        Returns:
            str or None: Response content if successful, else None
        """
        if not self.current_model:
            print("No model selected. Use change_model() or check model availability.")
            return None

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.current_model,
            "messages": [
                {"role": "user", "content": content}
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                assistant_message = data["choices"][0]["message"]["content"]
                print("Response:")
                print(assistant_message)
                return assistant_message
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None


# ————————————————————————
# Example Usage
# ————————————————————————

if __name__ == "__main__":
    # Replace with your actual key
    API_KEY = "venv/api_key.txt"

    agent = LanguageAgent(api_key=API_KEY)

    # Optional: List models again
    # agent.list_models()

    # Send a test message
    # agent.send_message("Hello, what is your model name?")

    # Change model (only if another is available)
    # agent.change_model("another-model-name")

    # Send another message
    # agent.send_message("Tell me about agentic systems.")