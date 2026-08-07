import logging
import requests
import asyncio
from typing import Optional, Dict, Any
from backend.app.core.config import settings

logger = logging.getLogger("ai_adapter")

class AIServiceInterface:
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        model: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        raise NotImplementedError

class GeminiHTTPAdapter(AIServiceInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        model: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        model_name = model or settings.AI_MODEL_ROUTINE
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        
        # Build payload
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
            
        generation_config = {}
        if json_mode:
            generation_config["responseMimeType"] = "application/json"
        if generation_config:
            payload["generationConfig"] = generation_config
            
        headers = {"Content-Type": "application/json"}
        
        try:
            # Execute in a threadpool to keep it async
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.session.post(url, json=payload, headers=headers, timeout=30.0)
            )
            
            if response.status_code != 200:
                logger.error(f"Gemini HTTP error {response.status_code}: {response.text}")
                return f"Error: Gemini API returned status {response.status_code}"
                
            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                logger.warning("Gemini returned empty candidates")
                return ""
                
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                logger.warning("Gemini returned empty parts")
                return ""
                
            return parts[0].get("text", "")
            
        except Exception as e:
            logger.exception("Exception in Gemini HTTP Adapter")
            return f"Error: {str(e)}"

class OpenRouterHTTPAdapter(AIServiceInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        model: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        model_name = model or "google/gemini-2.5-flash"
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://routemind.ai",
            "X-Title": "RouteMind Dashboard"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model_name,
            "messages": messages
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
            
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.session.post(url, json=payload, headers=headers, timeout=30.0)
            )
            
            if response.status_code != 200:
                logger.error(f"OpenRouter HTTP error {response.status_code}: {response.text}")
                return f"Error: OpenRouter API returned status {response.status_code}"
                
            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                logger.warning("OpenRouter returned empty choices")
                return ""
                
            message = choices[0].get("message", {})
            return message.get("content", "")
            
        except Exception as e:
            logger.exception("Exception in OpenRouter HTTP Adapter")
            return f"Error: {str(e)}"

class AIService:
    def __init__(self):
        provider = settings.AI_PROVIDER
        if provider == "openrouter":
            logger.info("Initializing OpenRouter AI Adapter")
            self.adapter = OpenRouterHTTPAdapter(settings.OPENROUTER_API_KEY)
        else:
            logger.info("Initializing Google Gemini HTTP Adapter")
            self.adapter = GeminiHTTPAdapter(settings.GOOGLE_API_KEY)
            
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        model: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        return await self.adapter.generate_text(prompt, system_instruction, model, json_mode)

# Singleton Instance
ai_service = AIService()
