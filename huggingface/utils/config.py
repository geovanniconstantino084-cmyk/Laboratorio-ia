"""Configuration loader"""

import yaml
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_config(config_path: str = "space_config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        if not os.path.exists(config_path):
            logger.warning(f"Config file not found: {config_path}")
            return get_default_config()
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration
    
    Returns:
        Default configuration dictionary
    """
    return {
        'models': {
            'chat': {
                'model_id': 'mistralai/Mistral-7B-Instruct-v0.1',
                'max_tokens': 512,
                'temperature': 0.7
            },
            'image_generation': {
                'model_id': 'stabilityai/stable-diffusion-xl-base-1.0',
                'guidance_scale': 7.5,
                'num_inference_steps': 50
            },
            'video_animation': {
                'model_id': 'damo-vilab/text-to-video-ms-1.7b',
                'num_frames': 16,
                'fps': 8
            },
            'influencer_generation': {
                'model_id': 'stabilityai/stable-diffusion-xl-base-1.0',
                'extension': 'ip-adapter-face-id'
            }
        },
        'api': {
            'port': 7860,
            'auth': True,
            'debug': False
        }
    }
