"""Stable Diffusion XL text-to-image and image-to-image generation."""

import logging
import os
import uuid
from typing import Optional

import torch
from diffusers import AutoPipelineForImage2Image, AutoPipelineForText2Image
from PIL import Image

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self, model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        common = {"torch_dtype": dtype, "use_safetensors": True}
        self.pipeline = AutoPipelineForText2Image.from_pretrained(model_id, **common).to(self.device)
        self.img2img_pipeline = AutoPipelineForImage2Image.from_pretrained(
            model_id, **common
        ).to(self.device)
        if self.device == "cuda":
            self.pipeline.enable_model_cpu_offload()
            self.img2img_pipeline.enable_model_cpu_offload()
        self.output_dir = "outputs/images"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, prompt: str, reference_image: Optional[str] = None, **kwargs) -> str:
        steps = min(int(kwargs.get("num_inference_steps", 25)), 40)
        if reference_image:
            image = Image.open(reference_image).convert("RGB").resize((1024, 1024))
            result = self.img2img_pipeline(
                prompt=prompt, image=image, strength=0.55,
                guidance_scale=float(kwargs.get("guidance_scale", 7.5)),
                num_inference_steps=steps,
            ).images[0]
        else:
            result = self.pipeline(
                prompt=prompt, height=1024, width=1024,
                guidance_scale=float(kwargs.get("guidance_scale", 7.5)),
                num_inference_steps=steps,
            ).images[0]
        path = os.path.join(self.output_dir, f"{uuid.uuid4()}.png")
        result.save(path)
        return path
