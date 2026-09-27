#!/usr/bin/env python3
"""
Hugging Face Space - Laboratorio IA
Main application for AI models inference
"""

import os
import sys
import logging
from typing import Optional, Tuple
import gradio as gr
from dotenv import load_dotenv

from models.chat_model import ChatModel
from models.image_generator import ImageGenerator
from models.video_animator import VideoAnimator
from models.influencer_generator import InfluencerGenerator
from utils.validators import validate_image, validate_prompt
from utils.config import load_config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Initialize models
logger.info("Initializing AI models...")
chat_model = ChatModel(model_id=config['models']['chat']['model_id'])
image_gen = ImageGenerator(model_id=config['models']['image_generation']['model_id'])
video_animator = VideoAnimator(model_id=config['models']['video_animation']['model_id'])
influencer_gen = InfluencerGenerator(
    base_model=config['models']['influencer_generation']['model_id'],
    extension=config['models']['influencer_generation']['extension']
)
logger.info("Models initialized successfully")


def chat_with_influencer(message: str, history: list) -> str:
    """
    Chat interface with AI influencer
    
    Args:
        message: User message
        history: Conversation history
        
    Returns:
        AI response
    """
    try:
        if not message or len(message.strip()) == 0:
            return "Por favor, escribe un mensaje válido."
            
        # Validate prompt
        if not validate_prompt(message):
            return "El mensaje contiene caracteres no permitidos."
        
        # Generate response
        response = chat_model.generate(message, history)
        return response
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return f"Error al procesar tu mensaje: {str(e)}"


def generate_image(prompt: str, reference_image: Optional[gr.File] = None) -> Tuple[str, str]:
    """
    Generate image with optional reference
    
    Args:
        prompt: Text description
        reference_image: Optional reference image
        
    Returns:
        Generated image path and metadata
    """
    try:
        if not prompt or len(prompt.strip()) == 0:
            return None, "Error: Prompt vacío"
        
        # Validate prompt
        if not validate_prompt(prompt):
            return None, "Error: Prompt contiene caracteres no permitidos"
        
        # Validate reference image if provided
        if reference_image:
            is_valid, error_msg = validate_image(reference_image.name)
            if not is_valid:
                return None, f"Error: {error_msg}"
        
        # Generate image
        image_path = image_gen.generate(
            prompt=prompt,
            reference_image=reference_image.name if reference_image else None
        )
        
        return image_path, "✓ Imagen generada exitosamente"
        
    except Exception as e:
        logger.error(f"Error in image generation: {str(e)}")
        return None, f"Error: {str(e)}"


def create_virtual_influencer(name: str, description: str, reference_image: gr.File) -> Tuple[str, str]:
    """
    Create a virtual influencer character
    
    Args:
        name: Character name
        description: Character description
        reference_image: Face reference image
        
    Returns:
        Generated character image and metadata
    """
    try:
        # Validate inputs
        if not name or not description or not reference_image:
            return None, "Error: Todos los campos son requeridos"
        
        if not validate_prompt(description):
            return None, "Error: Descripción contiene caracteres no permitidos"
        
        is_valid, error_msg = validate_image(reference_image.name)
        if not is_valid:
            return None, f"Error: {error_msg}"
        
        # Generate influencer
        influencer_image = influencer_gen.generate(
            name=name,
            description=description,
            reference_face=reference_image.name
        )
        
        return influencer_image, f"✓ Influencer '{name}' creado exitosamente"
        
    except Exception as e:
        logger.error(f"Error creating influencer: {str(e)}")
        return None, f"Error: {str(e)}"


def animate_image_to_video(image: gr.File, prompt: str, duration: int = 8) -> Tuple[str, str]:
    """
    Animate image to video
    
    Args:
        image: Input image
        prompt: Animation description
        duration: Video duration in seconds
        
    Returns:
        Generated video path and metadata
    """
    try:
        # Validate inputs
        if not image or not prompt:
            return None, "Error: Imagen y descripción son requeridas"
        
        if not validate_prompt(prompt):
            return None, "Error: Descripción contiene caracteres no permitidos"
        
        is_valid, error_msg = validate_image(image.name)
        if not is_valid:
            return None, f"Error: {error_msg}"
        
        # Generate video
        video_path = video_animator.animate(
            image_path=image.name,
            prompt=prompt,
            duration=duration
        )
        
        return video_path, "✓ Video generado exitosamente"
        
    except Exception as e:
        logger.error(f"Error in video animation: {str(e)}")
        return None, f"Error: {str(e)}"


# Build Gradio Interface
def build_interface():
    """
    Build the Gradio web interface
    """
    
    with gr.Blocks(title="Laboratorio IA - Influencers Virtuales", theme=gr.themes.Soft()) as demo:
        
        gr.Markdown("""
        # 🤖 Laboratorio IA
        ## Generación de Influencers Virtuales, Imágenes y Videos con IA
        
        Utiliza modelos open source para crear contenido multimedia generado con inteligencia artificial.
        """)
        
        with gr.Tabs():
            
            # Tab 1: Chat with Influencer
            with gr.TabItem("💬 Chat con Influencer"):
                gr.Markdown("Conversa con un influencer virtual generado por IA")
                
                with gr.Row():
                    chat_input = gr.Textbox(
                        label="Tu mensaje",
                        placeholder="Escribe aquí tu mensaje...",
                        lines=2
                    )
                
                chat_output = gr.Textbox(
                    label="Respuesta del Influencer",
                    interactive=False,
                    lines=3
                )
                
                chat_history = gr.State(value=[])
                
                chat_button = gr.Button("Enviar Mensaje", variant="primary")
                chat_button.click(
                    fn=chat_with_influencer,
                    inputs=[chat_input, chat_history],
                    outputs=[chat_output]
                )
            
            # Tab 2: Generate Image
            with gr.TabItem("🎨 Generar Imagen"):
                gr.Markdown("Genera imágenes realistas basadas en descripciones")
                
                with gr.Row():
                    with gr.Column():
                        prompt_input = gr.Textbox(
                            label="Descripción",
                            placeholder="Describe la imagen que deseas...",
                            lines=3
                        )
                        reference_image = gr.Image(
                            label="Imagen de Referencia (opcional)",
                            type="filepath"
                        )
                    
                    with gr.Column():
                        image_output = gr.Image(label="Imagen Generada")
                        image_status = gr.Textbox(label="Estado", interactive=False)
                
                generate_button = gr.Button("Generar Imagen", variant="primary")
                generate_button.click(
                    fn=generate_image,
                    inputs=[prompt_input, reference_image],
                    outputs=[image_output, image_status]
                )
            
            # Tab 3: Create Virtual Influencer
            with gr.TabItem("⭐ Crear Influencer"):
                gr.Markdown("Crea tu propio influencer virtual personalizado")
                
                with gr.Row():
                    with gr.Column():
                        name_input = gr.Textbox(
                            label="Nombre",
                            placeholder="Nombre del influencer"
                        )
                        desc_input = gr.Textbox(
                            label="Descripción",
                            placeholder="Describe su personalidad y estilo...",
                            lines=3
                        )
                        face_image = gr.Image(
                            label="Foto de Referencia del Rostro",
                            type="filepath"
                        )
                    
                    with gr.Column():
                        influencer_output = gr.Image(label="Influencer Generado")
                        influencer_status = gr.Textbox(label="Estado", interactive=False)
                
                create_button = gr.Button("Crear Influencer", variant="primary")
                create_button.click(
                    fn=create_virtual_influencer,
                    inputs=[name_input, desc_input, face_image],
                    outputs=[influencer_output, influencer_status]
                )
            
            # Tab 4: Animate Image to Video
            with gr.TabItem("🎬 Animar Imagen a Video"):
                gr.Markdown("Convierte imágenes estáticas en videos animados")
                
                with gr.Row():
                    with gr.Column():
                        video_image = gr.Image(
                            label="Imagen de Entrada",
                            type="filepath"
                        )
                        animation_prompt = gr.Textbox(
                            label="Descripción de Animación",
                            placeholder="Describe cómo debe animarse la imagen...",
                            lines=3
                        )
                        duration_slider = gr.Slider(
                            label="Duración (segundos)",
                            minimum=4,
                            maximum=16,
                            value=8,
                            step=1
                        )
                    
                    with gr.Column():
                        video_output = gr.Video(label="Video Generado")
                        video_status = gr.Textbox(label="Estado", interactive=False)
                
                animate_button = gr.Button("Generar Video", variant="primary")
                animate_button.click(
                    fn=animate_image_to_video,
                    inputs=[video_image, animation_prompt, duration_slider],
                    outputs=[video_output, video_status]
                )
    
        gr.Markdown("""
        ---
        **Notas:**
        - Todos los modelos son open source y se ejecutan localmente en el servidor
        - Los tiempos de generación varían según la complejidad
        - Las imágenes y videos se eliminan después de la sesión
        - Respeta los términos de uso y políticas de privacidad
        """)
    
    return demo


if __name__ == "__main__":
    logger.info("Starting Laboratorio IA Gradio App...")
    demo = build_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=os.getenv("DEBUG", "False") == "True"
    )
