# 🚨 LoraLink API

API para registro y gestión de emergencias utilizando FastAPI.

## 📖 Documentación

- **Producción**: [https://api.loralink.live/scalar](https://api.loralink.live/scalar)
- **Local**: [http://localhost:8000/scalar](http://localhost:8000/scalar)

## 🛠️ Desarrollo Local

### Prerrequisitos

- Python 3.8+
- Redis (opcional, para rate limiting)

### Configuración

1. **Clona el repositorio**:
   ```bash
   git clone <repository-url>
   cd loralinka-api
   ```

2. **Crea y activa el entorno virtual**:
   ```bash
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   ```bash
   cp src/.env.example src/.env
   ```

   Edita el archivo `src/.env` con tus valores locales. El archivo incluye todas las variables necesarias:
   - `API_KEY` - Clave de autenticación
   - `DATABASE_URL` - Conexión a base de datos (SQLite por defecto)
   - `REDIS_URL` - Conexión a Redis para rate limiting
   - Variables individuales de DB (opcional)
   - `SQL_ECHO` - Debug de queries SQL

5. **Instala Redis (opcional)**:
   ```bash
   # macOS:
   brew install redis
   brew services start redis

   # Ubuntu/Debian:
   sudo apt install redis-server
   sudo systemctl start redis

   # Windows:
   # Descarga desde: https://redis.io/download
   ```

### Ejecutar la aplicación

```bash
fastapi dev src/main.py
```

La API estará disponible en:
- **Aplicación**: http://localhost:8000
- **Documentación Scalar**: http://localhost:8000/scalar
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔑 Uso de la API

Todos los endpoints requieren autenticación con API key:

```bash
curl -H "X-API-Key: tu-api-key" http://localhost:8000/emergencies
```

## 📚 Endpoints Principales

### Emergencias
- `POST /emergencies` - Crear emergencia
- `GET /emergencies` - Listar emergencias
- `GET /emergencies/{id}` - Obtener emergencia específica

### Unidades de Emergencia
- `POST /emergency-units` - Registrar unidad
- `GET /emergency-units` - Listar unidades
- `GET /emergency-units/search/nearby` - Buscar unidades cercanas

### Usuarios
- `POST /users` - Registrar usuario
- `GET /users` - Listar usuarios

### Catálogos
- `GET /catalogs/accident-types` - Tipos de accidentes
- `GET /catalogs/medical-conditions` - Condiciones médicas

## 🚀 Despliegue

El proyecto incluye automatización completa de despliegue con SSL. Ver:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de despliegue
- [SSL-AUTOMATION.md](SSL-AUTOMATION.md) - Configuración SSL automática

## 🗄️ Base de Datos

- **Local**: SQLite (automático)
- **Producción**: PostgreSQL

Las migraciones se ejecutan automáticamente al iniciar la aplicación.

## 🔧 Scripts Útiles

```bash
# Ejecutar en modo desarrollo
fastapi dev src/main.py

# Ejecutar en modo producción
fastapi run src/main.py

# Verificar sintaxis
python -m py_compile src/main.py
```