# Laboratorio IA

Creación de imagen a video mediante inteligencia artificial.

Este proyecto integra diferentes servicios para ofrecer una experiencia completa de generación y gestión de contenido con IA, desde la autenticación de usuarios hasta el procesamiento del modelo de chat y la gestión de suscripciones.

## Estructura del proyecto

```text
Laboratorio-ia/
├── GitHub
│   └── Código fuente
├── Vercel
│   └── Web Next.js + API routes
├── Supabase
│   ├── Login con Google
│   ├── Usuarios
│   ├── Configuración del personaje
│   ├── Conversaciones
│   └── Límites de uso
├── Hugging Face
│   └── Modelo de chat
├── Stripe
│   └── Suscripciones y pagos
└── README.md
```

## Servicios y responsabilidades

### GitHub
- Repositorio central del proyecto.
- Almacena el código fuente, control de versiones y colaboración del equipo.

### Vercel
- Aloja la aplicación web desarrollada con Next.js.
- Se encarga de la interfaz de usuario y de las API routes del backend ligero.

### Supabase
- Maneja la autenticación de usuarios con Google.
- Guarda la información de usuarios.
- Administra la configuración del personaje.
- Sirve como base para almacenar conversaciones.
- Controla los límites de uso por usuario o plan.

### Hugging Face
- Proporciona el modelo de chat utilizado para generar respuestas con inteligencia artificial.
- Se integra con la aplicación para procesar prompts y devolver resultados inteligentes.

### Stripe
- Gestiona las suscripciones y pagos de los usuarios.
- Permite activar funcionalidades premium o planes de acceso.

## Arquitectura general

La aplicación se compone de una web frontend desplegada en Vercel, conectada a Supabase para la gestión de usuarios y datos de la aplicación, mientras que Hugging Face se utiliza para la parte de IA generativa y Stripe para monetización y suscripciones.

En resumen:
- Frontend: Vercel + Next.js
- Base de datos/autenticación: Supabase
- IA generativa: Hugging Face
- Pagos: Stripe
- Código fuente: GitHub

## Flujo de uso

1. El usuario inicia sesión con Google mediante Supabase.
2. El sistema guarda y administra sus datos y preferencias.
3. El usuario configura su personaje o perfil.
4. La aplicación genera conversaciones o respuestas con el modelo de Hugging Face.
5. Los límites de uso y los planes de suscripción se gestionan con Supabase y Stripe.

## Requisitos

- Cuenta en GitHub
- Proyecto desplegado en Vercel
- Proyecto en Supabase
- Modelo o acceso en Hugging Face
- Cuenta de Stripe para pagos y suscripciones

## Objetivo del proyecto

Crear una plataforma de IA orientada a experiencias interactivas con personajes, chats inteligentes y gestión avanzada de usuarios, suscripciones y contenido generado.

## Notas

Este README sirve como base de arquitectura y documentación del proyecto. A medida que avance el desarrollo, se pueden agregar:
- instrucciones de instalación
- variables de entorno
- guía de despliegue
- documentación API
- ejemplos de uso

