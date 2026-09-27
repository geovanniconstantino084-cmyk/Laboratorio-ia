"""Chat model using Mistral or similar open source LLM"""

import logging
from typing import List, Dict, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

logger = logging.getLogger(__name__)


class ChatModel:
    """Wrapper for open source chat models"""
    
    def __init__(self, model_id: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        """
        Initialize chat model
        
        Args:
            model_id: HuggingFace model identifier
        """
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading model {model_id} on device {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        
        self.model.eval()
        logger.info(f"Model {model_id} loaded successfully")
    
    def generate(
        self,
        prompt: str,
        history: Optional[List[Dict]] = None,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.95
    ) -> str:
        """
        Generate chat response
        
        Args:
            prompt: User message
            history: Conversation history
            max_length: Maximum response length
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated response
        """
        try:
            # Format conversation history
            if history is None:
                history = []
            
            formatted_prompt = self._format_prompt(prompt, history)
            
            # Tokenize
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new generated part
            response = response[len(formatted_prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error al generar respuesta: {str(e)}"
    
    def _format_prompt(self, prompt: str, history: List[Dict]) -> str:
        """
        Format conversation history and current prompt
        
        Args:
            prompt: Current user message
            history: Conversation history
            
        Returns:
            Formatted prompt
        """
        formatted = ""
        
        # Add history
        for msg in history:
            if msg.get("role") == "user":
                formatted += f"Usuario: {msg.get('content')}\n"
            elif msg.get("role") == "assistant":
                formatted += f"Asistente: {msg.get('content')}\n"
        
        # Add current message
        formatted += f"Usuario: {prompt}\nAsistente:"
        
        return formatted
