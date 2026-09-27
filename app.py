"""Root entry point for Hugging Face Spaces."""

import os
import sys

SPACE_DIR = os.path.join(os.path.dirname(__file__), "huggingface")
sys.path.insert(0, SPACE_DIR)
os.chdir(SPACE_DIR)

from app import build_interface  # noqa: E402


demo = build_interface()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
