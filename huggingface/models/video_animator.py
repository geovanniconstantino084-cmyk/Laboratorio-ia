"""Image-to-video generation using Stable Video Diffusion, loaded on demand."""

import os
import uuid

import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
from torchvision.io import write_video


class VideoAnimator:
    def __init__(self, model_id="stabilityai/stable-video-diffusion-img2vid-xt"):
        self.model_id = model_id
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "outputs/videos"
        os.makedirs(self.output_dir, exist_ok=True)

    def _load(self):
        if self.pipeline is None:
            if self.device != "cuda":
                raise RuntimeError("La animación de video requiere una GPU en este Space.")
            self.pipeline = StableVideoDiffusionPipeline.from_pretrained(
                self.model_id, torch_dtype=torch.float16, variant="fp16"
            )
            self.pipeline.enable_model_cpu_offload()

    def animate(self, image_path, prompt="", duration=4, fps=8, **kwargs):
        if not os.path.exists(image_path):
            raise FileNotFoundError(image_path)
        self._load()
        image = Image.open(image_path).convert("RGB").resize((1024, 576))
        frames = self.pipeline(image, num_frames=min(25, max(14, int(duration * fps))),
                               decode_chunk_size=4, motion_bucket_id=127,
                               noise_aug_strength=0.02).frames[0]
        path = os.path.join(self.output_dir, f"{uuid.uuid4()}.mp4")
        tensor = torch.stack([torch.from_numpy(__import__("numpy").array(frame)) for frame in frames])
        write_video(path, tensor, fps=fps, video_codec="h264")
        return path
