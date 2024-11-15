# Step 1: Base image
FROM python:3.9-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy project files
COPY . .

# Step 5: Expose the port for FastAPI
EXPOSE 8000

# Step 6: Command to run FastAPI server
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]