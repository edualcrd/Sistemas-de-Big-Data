# Análisis de Perfiles en Bluesky mediante IA y NoSQL

Este proyecto automatiza la extracción de datos no estructurados de perfiles en la red social Bluesky, los almacena de forma estructurada en MongoDB y genera perfiles de intereses automatizados utilizando la inteligencia artificial generativa de Anthropic.

## Características Principales (Features)
- **Extracción de datos:** Conexión con el AT Protocol (Bluesky) para obtener el timeline de cualquier cuenta.
- **Limpieza de datos:** Filtrado de URLs y caracteres extraños de los posts extraídos.
- **Persistencia NoSQL:** Almacenamiento tanto de los datos en bruto como de los procesados en una base de datos MongoDB.
- **Análisis con LLM:** Generación de un perfil psicológico/intereses a partir de los textos utilizando Anthropic API.
- **Exportación:** Generación automática de reportes en `.txt` y exportación de la base de datos en `.json`.

## Tecnologías Utilizadas
- **Lenguaje de Programación:** Python 3
- **Gestor de Entornos y Paquetes:** `uv`
- **Base de Datos:** MongoDB (Local o Atlas)
- **SDKs y APIs:** 
  - `@atproto` (Bluesky SDK)
  - `anthropic` (Claude API)

## Requisitos Previos
- Instalar **Python 3.10** o superior.
- Instalar el gestor de paquetes **`uv`**.
- Tener un servidor de **MongoDB** ejecutándose en local (puerto 27017) o una conexión válida a MongoDB Atlas.
- Disponer de una cuenta en **Bluesky** para generar una contraseña de aplicación.
- Tener una **API Key** válida de Claude (Claude Console).

## Instalación y Configuración
El proyecto hace uso de un entorno virtual gestionado con `uv` que está ubicado en el directorio padre del proyecto.

1. **Clonar el repositorio:**
   ```bash
   git clone <enlace-a-tu-repositorio>
   cd Sistemas_de_Big_Data/Actividad_1_3
   ```

2. **Activar el entorno virtual:**
   - En Windows: `..\..\.venv\Scripts\activate`
   - En Linux/Mac: `source ../../.venv/bin/activate`

3. **Instalar las dependencias:**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   Crea un archivo `.env` en la raíz de la carpeta `Actividad_1_3` con el siguiente contenido:
   ```env
   BSKY_IDENTIFIER=tu_usuario.bsky.social (o correo)
   BSKY_PASSWORD=tu-contraseña-de-app-bluesky
   ANTHROPIC_API_KEY=sk-ant-usr-1He...wAA
   MONGO_URI=mongodb://localhost:27017/
   ```

## Guía de Uso
Para ejecutar el análisis, asegúrate de tener el entorno activado y ejecuta el script principal:

```bash
python 1_3_Alcaide_Rodríguez_Eduardo.py
```

Tras una ejecución exitosa, se generarán automáticamente dos archivos en la carpeta:
- `1_3_Alcaide_Rodríguez_Eduardo.txt`: Con el análisis devuelto por el LLM.
- `1_3_Alcaide_Rodríguez_Eduardo.json`: Con el documento guardado en MongoDB.

## Pruebas (Testing)
Al no disponer de tests unitarios formales, la prueba principal consiste en verificar la conexión de las 3 APIs integradas ejecutando el script y comprobando la correcta generación de los archivos de salida y la inserción del documento en el cliente de MongoDB (Compass o terminal).

## Cómo Contribuir (Contributing)
Si deseas contribuir a este proyecto académico:
1. Haz un Fork del repositorio.
2. Crea una nueva rama para tus funcionalidades (`git checkout -b feature/nueva-funcionalidad`).
3. Haz un commit con tus cambios (`git commit -m 'Añade nueva funcionalidad'`).
4. Haz un push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia
Este proyecto se distribuye bajo la licencia **GNU General Public License v3.0**. Consulta el sitio de GNU o [choosealicense.com](https://choosealicense.com/es/) para más detalles.