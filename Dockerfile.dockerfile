# Use a lightweight Python base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Train the model during build so it's ready to go
RUN python train.py

# Expose the FastAPI port
EXPOSE 8000

# By default, start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]