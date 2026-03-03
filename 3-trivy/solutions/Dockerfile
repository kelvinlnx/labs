# Stage 1: Build stage
FROM python:3.14-slim AS builder

# Set a working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install into a specific prefix instead of --user
# This makes it much easier to copy to the final stage
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Final stage
FROM python:3.14-slim

# Disable pyc layer writes and flush logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Update db
# RUN apt-get update && \
#    apt install SOMETHING
#    rm -rf /var/lib/apt/lists/* && \
RUN useradd --create-home appuser

# Set working directory to the user's home
WORKDIR /home/appuser

# Copy the Python dependencies from the builder stage
# The --from flag copies from the previous stage named "builder"
COPY --from=builder --chown=appuser:appuser /install /home/appuser/.local

# Copy the application code
COPY --chown=appuser:appuser src/ .

# Switch to the non‑root user
USER appuser

# Expose the application port
EXPOSE 8080

# Define the command to run the application
CMD ["python", "app.py"]
