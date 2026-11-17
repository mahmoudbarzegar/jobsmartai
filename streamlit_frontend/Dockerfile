
FROM python:3.12-slim

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency definitions from project root
COPY pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1
ENV UV_HTTP_TIMEOUT=300
ENV UV_HTTP_RETRIES=10
ENV UV_CONCURRENT_DOWNLOADS=4

RUN uv sync --frozen --no-dev --only-group frontend --no-install-project

# Copy Streamlit application
COPY streamlit_frontend/ .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
