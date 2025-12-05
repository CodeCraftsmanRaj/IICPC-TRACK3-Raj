FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements (create a server-specific requirements.txt first if needed)
# For now, we manually install what we used
RUN pip install fastapi uvicorn sqlalchemy pydantic python-multipart requests

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]