"""Reference-guided image generation.

This uses SDXL img2img as a reliable baseline. It preserves composition/style,
but is not face identity locking; add InstantID/IP-Adapter only after testing a
compatible GPU image and model license.
"""

import os
import re
import uuid

import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image


class InfluencerGenerator:
    def __init__(self, base_model="stabilityai/stable-diffusion-xl-base-1.0", extension=None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        self.pipeline = AutoPipelineForImage2Image.from_pretrained(
            base_model, torch_dtype=dtype, use_safetensors=True
        ).to(device)
        if device == "cuda":
            self.pipeline.enable_model_cpu_offload()
        self.output_dir = "outputs/influencers"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, name, description, reference_face, **kwargs):
        if not os.path.exists(reference_face):
            raise FileNotFoundError(reference_face)
        source = Image.open(reference_face).convert("RGB").resize((1024, 1024))
        prompt = (
            f"realistic virtual influencer portrait, {name}, {description}, "
            "professional studio photography, natural skin, detailed face"
        )
        result = self.pipeline(
            prompt=prompt, image=source, strength=0.35,
            guidance_scale=7.0, num_inference_steps=25,
        ).images[0]
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:40]
        path = os.path.join(self.output_dir, f"{safe_name}_{uuid.uuid4()}.png")
        result.save(path)
        return path
