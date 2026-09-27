"""Image generation model using Stable Diffusion"""

import logging
from typing import Optional
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, ControlNetPipeline
import torch
from PIL import Image
import os
import uuid

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Wrapper for image generation models"""
    
    def __init__(self, model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        """
        Initialize image generator
        
        Args:
            model_id: HuggingFace model identifier
        """
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "outputs/images"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"Loading model {model_id} on device {self.device}")
        
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        
        self.img2img_pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        
        logger.info(f"Model {model_id} loaded successfully")
    
    def generate(
        self,
        prompt: str,
        reference_image: Optional[str] = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        height: int = 512,
        width: int = 512
    ) -> str:
        """
        Generate image from text
        
        Args:
            prompt: Text description
            reference_image: Optional reference image path
            guidance_scale: Classifier-free guidance scale
            num_inference_steps: Number of diffusion steps
            height: Image height
            width: Image width
            
        Returns:
            Path to generated image
        """
        try:
            logger.info(f"Generating image with prompt: {prompt}")
            
            if reference_image and os.path.exists(reference_image):
                # Image-to-image generation
                ref_img = Image.open(reference_image).convert("RGB")
                
                image = self.img2img_pipeline(
                    prompt=prompt,
                    image=ref_img,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    height=height,
                    width=width
                ).images[0]
            else:
                # Text-to-image generation
                image = self.pipeline(
                    prompt=prompt,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    height=height,
                    width=width
                ).images[0]
            
            # Save image
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(self.output_dir, filename)
            image.save(filepath)
            
            logger.info(f"Image saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise
