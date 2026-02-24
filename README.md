# 🎨 Brand Governance AI - API

Una plataforma inteligente para la gobernanza y gestión de marcas empresariales utilizando IA. Este API permite crear manuales de marca, generar activos creativos y auditar compliance visual contra los estándares de marca.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Variables de Entorno](#variables-de-entorno)
- [Arquitectura](#arquitectura)
- [Servicios](#servicios)
- [Autenticación y Autorización](#autenticación-y-autorización)
- [Contribución](#contribución)

## ✨ Características

- **Generación de Manuales de Marca**: Crea manuales de marca estructurados automáticamente usando IA
- **Auditoría de Imágenes**: Valida imágenes contra manuales de marca usando capacidades de visión por computadora
- **Generación de Activos Creativos**: Genera creatividades para diferentes tipos de activos respetando los lineamientos de marca
- **Gestión de Usuarios**: Sistema de autenticación con roles (Admin, User, Auditor)
- **Paginación**: Listados paginados de manuales y activos
- **Observabilidad**: Integración con Langfuse para trazabilidad de operaciones
- **CORS Habilitado**: Soporte para solicitudes cross-origin

## 📦 Requisitos Previos

- Python 3.12
- pip (gestor de paquetes de Python)
- Cuentas activas en:
  - Groq API
  - Google Generative AI
  - Supabase
  - Langfuse (opcional, para observabilidad)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd service-brand-api
```

### 2. Crear Entorno Virtual

```bash
# En Linux/Mac
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Groq API
GROQ_API_KEY=your_groq_api_key

# Google Generative AI
GOOGLE_API_KEY=your_google_api_key

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Langfuse (Observabilidad)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=your_langfuse_host
```

## 🏃 Uso

### Iniciar el Servidor

**Desarrollo:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Producción:**
```bash
gunicorn app:app \
  --log-level DEBUG \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:9001 \
  --timeout 360
```

El servidor estará disponible en:
- **Desarrollo**: http://localhost:8000
- **Producción**: http://0.0.0.0:9001

### Acceder a la Documentación

Una vez que el servidor está corriendo, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
service-brand-api/
├── app.py                          # Punto de entrada de la aplicación
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── models/
│   ├── schemas.py                  # Esquemas Pydantic para validación
│   └── __pycache__/
├── routes/
│   ├── brand/                      # Endpoints de Gestión de Marcas
│   │   └── __init__.py
│   ├── asset/                      # Endpoints de Gestión de Activos
│   │   └── __init__.py
│   ├── audit/                      # Endpoints de Auditoría Visual
│   │   └── __init__.py
│   ├── login/                      # Endpoints de Autenticación
│   │   └── __init__.py
│   └── __pycache__/
├── services/
│   ├── groq_service.py             # Servicio de IA (Groq)
│   ├── vision_service.py           # Servicio de Visión por Computadora (Google)
│   ├── supabase_service.py         # Servicio de Base de Datos (Supabase)
│   └── __pycache__/
├── tool/
│   ├── __init__.py                 # Utilidades (logger, etc.)
│   └── __pycache__/
└── __pycache__/
```

## 🔌 API Endpoints

### Autenticación

#### **POST** `/api/v1.0/login/`

Autentica un usuario y devuelve tokens de acceso.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "token_string",
  "refresh_token": "refresh_token_string",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "role": "admin"
  }
}
```

**Roles Requeridos**: Ninguno

---

### Gestión de Marcas

#### **POST** `/api/v1.0/brand/brands`

Crea una nueva marca y genera automáticamente su manual.

**Body:**
```json
{
  "name": "Mi Marca",
  "briefing": "Descripción y lineamientos de la marca..."
}
```

**Response:**
```json
{
  "brand_id": "uuid",
  "manual": {
    "mission": "...",
    "vision": "...",
    "values": [...],
    "tone": "...",
    "do_not": [...],
    "positioning": "...",
    "messaging_pillars": [...]
  }
}
```

**Roles Requeridos**: `admin`, `user`

#### **GET** `/api/v1.0/brand/`

Obtiene una lista paginada de manuales de marca.

**Query Parameters:**
- `page` (int, default: 1): Número de página
- `page_size` (int, default: 10, máx: 100): Elementos por página

**Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "brand_id": "uuid",
      "manual": {...},
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 10
}
```

**Roles Requeridos**: Autenticado

---

### Gestión de Activos

#### **POST** `/api/v1.0/asset/creative`

Genera un nuevo activo creativo basado en el manual de marca.

**Body:**
```json
{
  "brand_id": "uuid",
  "asset_type": "social_media_post",
  "instructions": "Genera un post para Instagram con tema navideño"
}
```

**Response:**
```json
{
  "asset_id": "uuid",
  "brand_id": "uuid",
  "asset_type": "social_media_post",
  "content": "...",
  "status": "pending_approval",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Roles Requeridos**: `admin`, `user`

#### **GET** `/api/v1.0/asset/`

Obtiene una lista paginada de activos.

**Query Parameters:**
- `page` (int, default: 1): Número de página
- `page_size` (int, default: 10, máx: 100): Elementos por página
- `brand_id` (string, opcional): Filtrar por ID de marca
- `asset_type` (string, opcional): Filtrar por tipo de activo

**Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "brand_id": "uuid",
      "asset_type": "social_media_post",
      "content": "...",
      "status": "approved",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 10
}
```

**Roles Requeridos**: Autenticado

---

### Auditoría Visual

#### **POST** `/api/v1.0/audit-image/audit-image`

Audita una imagen contra el manual de marca de un producto.

**Form Data:**
- `brand_id` (string): ID de la marca
- `file` (file): Imagen a auditar (JPG, PNG, etc.)

**Response:**
```json
{
  "approved": true,
  "reason": "La imagen cumple con los estándares de color y composición del manual"
}
```

**Roles Requeridos**: `admin`, `auditor`

---

## 🔐 Autenticación y Autorización

El API utiliza autenticación basada en **Bearer Tokens** con Supabase.

### Flujo de Autenticación

1. **Login**: Envía credenciales al endpoint `/api/v1.0/login/`
2. **Recibe Token**: El servidor devuelve `access_token` y `refresh_token`
3. **Usa Token**: Incluye el token en el header `Authorization: Bearer {token}`

### Roles

- **admin**: Acceso completo a todas las operaciones
- **user**: Puede crear marcas y activos
- **auditor**: Puede auditar imágenes

### Protección de Endpoints

Los endpoints están protegidos con middleware de autorización que valida el token y verifica los roles requeridos.

## 🏗️ Arquitectura

### Capas de la Aplicación

```
┌─────────────────────────────────────┐
│         FastAPI Application         │
├─────────────────────────────────────┤
│         Routes (API Endpoints)      │
│  ├── brand_route                    │
│  ├── asset_route                    │
│  ├── audit_image_route              │
│  └── login_route                    │
├─────────────────────────────────────┤
│         Services (Business Logic)   │
│  ├── groq_service (IA)              │
│  ├── vision_service (Visión)        │
│  └── supabase_service (BD)          │
├─────────────────────────────────────┤
│         External APIs               │
│  ├── Groq API                       │
│  ├── Google Generative AI           │
│  ├── Supabase                       │
│  └── Langfuse                       │
└─────────────────────────────────────┘
```

## 🔧 Servicios

### 1. **Groq Service** (`groq_service.py`)

Utiliza el modelo `llama-3.3-70b-versatile` para:
- Generar manuales de marca en formato JSON
- Generar contenido creativo para activos

**Funciones principales:**
- `generate_brand_manual(briefing)`: Crea un manual de marca
- `generate_creative_asset(manual, instructions, asset_type, brand_name)`: Genera un activo creativo

### 2. **Vision Service** (`vision_service.py`)

Utiliza el modelo `gemini-3-flash-preview` de Google para:
- Auditar imágenes contra manuales de marca
- Evaluar compliance visual

**Funciones principales:**
- `audit_image(manual, image_path)`: Audita una imagen

### 3. **Supabase Service** (`supabase_service.py`)

Gestiona:
- Autenticación de usuarios
- Operaciones CRUD de marcas, activos y manuales
- Control de acceso basado en roles
- Obtención de información del usuario autenticado

**Funciones principales:**
- `login_user(email, password)`: Autentica usuario
- `create_brand(name)`: Crea marca
- `save_asset(brand_id, asset_type, content)`: Guarda activo
- `require_roles(roles)`: Middleware de autorización
- `get_current_user(token)`: Obtiene usuario actual

---

## 📊 Modelos de Datos

### BrandCreate
```python
{
  "name": str,
  "briefing": str
}
```

### CreativeRequest
```python
{
  "brand_id": str,
  "asset_type": str,
  "instructions": str
}
```

### LoginRequest
```python
{
  "email": str,
  "password": str
}
```

---

## 🌐 Middleware

### CORS

El API tiene CORS habilitado para aceptar solicitudes desde cualquier origen:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
```

---

## 📝 Variables de Entorno Detalladas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GROQ_API_KEY` | Clave API de Groq | `gsk_...` |
| `GOOGLE_API_KEY` | Clave API de Google Generative AI | `AIzaSy...` |
| `SUPABASE_URL` | URL de la instancia Supabase | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Clave API de Supabase | `eyJhbGc...` |
| `LANGFUSE_PUBLIC_KEY` | Clave pública de Langfuse | `pk_...` |
| `LANGFUSE_SECRET_KEY` | Clave secreta de Langfuse | `sk_...` |
| `LANGFUSE_HOST` | Host de Langfuse | `https://cloud.langfuse.com` |

---

## 🛠️ Dependencias

| Paquete | Versión | Propósito |
|---------|---------|----------|
| `fastapi` | >=0.110.0 | Framework web |
| `uvicorn` | >=0.27.0 | Servidor ASGI |
| `gunicorn` | ==21.2.0 | Servidor WSGI para producción |
| `groq` | >=0.9.0 | Cliente API de Groq |
| `google-genai` | >=0.3.0 | Cliente Google Generative AI |
| `supabase` | >=2.4.0 | Cliente Supabase |
| `python-dotenv` | >=1.0.1 | Gestión de variables de entorno |
| `pydantic` | >=2.6.0 | Validación de datos |
| `pillow` | >=10.2.0 | Procesamiento de imágenes |
| `python-multipart` | >=0.0.9 | Manejo de datos multipart |
| `langfuse` | ==3.14.5 | Observabilidad y trazabilidad |

---

## 🚢 Despliegue

### Despliegue en Producción

```bash
# Usando Gunicorn
gunicorn app:app \
  --log-level DEBUG \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:9001 \
  --timeout 360 \
  --workers 4 \
  --access-logfile - \
  --error-logfile -
```

**Configuración recomendada:**
- Workers: 2-4 (según CPU disponible)
- Timeout: 360 segundos (para operaciones IA)
- Host: 0.0.0.0
- Puerto: 9001

---

## 📈 Monitoreo y Observabilidad

El proyecto integra **Langfuse** para rastrear:
- Llamadas a IA (Groq, Google)
- Latencia de operaciones
- Errores y excepciones
- Uso de tokens

### Visualizar Traces

Accede a tu dashboard de Langfuse en `{LANGFUSE_HOST}` para ver traces de operaciones.
