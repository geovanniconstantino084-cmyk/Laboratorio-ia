# Laboratorio IA - Hugging Face Space

Este es el espacio de Hugging Face que ejecuta los modelos open source para la plataforma Laboratorio IA.

## Características

- 💬 **Chat con Influencer Virtual** - Conversaciones en tiempo real
- 🎨 **Generación de Imágenes** - Creación de imágenes con descripciones
- ⭐ **Creación de Influencers** - Personajes virtuales personalizados
- 🎬 **Animación de Imágenes a Video** - Convierte imágenes en videos

## Modelos Open Source Utilizados

### Chat
- **Mistral-7B-Instruct** - Modelo de lenguaje de código abierto
- Alternativas: Llama 2, Qwen

### Generación de Imágenes
- **Stable Diffusion XL** - Generación de imágenes de alta calidad
- Alternativas: Flux, DALL-E mini

### Influencer Virtual
- **SDXL + IP-Adapter** - Consistencia facial usando embeddings
- Alternativa: InstantID

### Animación de Videos
- **AnimateDiff / Stable Video Diffusion** - Convierte imágenes en videos
- Alternativa: Wan

## Requisitos

- GPU: A10 o superior (recomendado)
- RAM: 16GB mínimo
- Almacenamiento: 50GB
- CUDA 11.8+

## Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/geovanniconstantino084-cmyk/Laboratorio-ia.git
cd Laboratorio-ia/huggingface

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar ejemplo de configuración
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:7860`

## Despliegue en Hugging Face Spaces

1. Crear un nuevo Space en Hugging Face: https://huggingface.co/spaces
2. Seleccionar **Gradio** como SDK
3. Conectar este repositorio
4. Configurar variables de entorno
5. El Space se desplegará automáticamente

## Variables de Entorno

```env
# Configuración de modelos
MODEL_CHAT=mistralai/Mistral-7B-Instruct-v0.1
MODEL_IMAGE=stabilityai/stable-diffusion-xl-base-1.0
MODEL_VIDEO=damo-vilab/text-to-video-ms-1.7b

# Configuración de API
HUGGINGFACE_API_KEY=your_key_here
```

## Estructura de Carpetas

```
huggingface/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── space_config.yaml      # Configuración
├── models/               # Módulos de modelos
│   ├── chat_model.py
│   ├── image_generator.py
│   ├── video_animator.py
│   └── influencer_generator.py
├── utils/               # Utilidades
│   ├── validators.py
│   └── config.py
└── outputs/            # Directorio de salida (generado)
    ├── images/
    ├── videos/
    └── influencers/
```

## Notas de Seguridad

- ✅ Valida todas las entradas
- ✅ Limita tamaño de archivos
- ✅ Sanitiza prompts
- ✅ Maneja excepciones correctamente
- ✅ Limpia archivos temporales

## Licencias

Todos los modelos son open source bajo licencias:

- **Mistral**: Apache 2.0
- **Stable Diffusion**: OpenRAIL
- **AnimateDiff**: Apache 2.0

Verifica las licencias antes de uso comercial.

## Soporte

Para reportar problemas:
- GitHub Issues: https://github.com/geovanniconstantino084-cmyk/Laboratorio-ia/issues
- Hugging Face Discussions: [Tu Space URL]

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
