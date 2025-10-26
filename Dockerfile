# --- STAGE 1: Build Image ---
    FROM python:3.11-slim-buster as builder

    WORKDIR /app
    
    # Instalar Poetry
    RUN pip install pipx && \
    pipx install poetry && \
    pipx ensurepath
    ENV PATH="/root/.local/bin:$PATH"
    
    # Copiar archivos de configuración
    COPY pyproject.toml poetry.lock ./
    
    # Instalar dependencias
    RUN poetry install --no-dev --no-root
    
    # --- STAGE 2: Runtime Image ---
    FROM python:3.11-slim-buster as runtime
    
    WORKDIR /app
    
    # Copiar el entorno virtual
    COPY --from=builder /root/.local/share/pypoetry/virtualenvs /root/.local/share/pypoetry/virtualenvs
    
    # Configurar el entorno virtual
    ENV POETRY_VIRTUALENVS_IN_PROJECT=false
    ENV POETRY_VIRTUALENVS_PATH=/root/.local/share/pypoetry/virtualenvs
    
    # Copiar el resto del código
    # NOTA: Si tienes una carpeta 'src' con otros módulos, asegúrate de copiarla también
    COPY . .
    
    # Comando de ejecución CORREGIDO
    # El script ahora se ejecuta como un archivo independiente en la raíz:
    CMD ["poetry", "run", "python", "main.py"] 
    # Si el ejecutable estuviera en /src/main.py sería "python", "src/main.py"