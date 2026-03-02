FROM python:3.9-slim

# Create a non‑root user and set the working directory
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
COPY app.py .
COPY static static/
COPY templates templates/

# Install dependencies to a local user directory
# We use --no-cache-dir to keep the image size slightly smaller
RUN pip install --no-cache-dir --user -r requirements.txt && \
    rm -rf /root/.cache/pip

# Ensure the local bin directory is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to the non‑root user
USER appuser

# Expose the application port
EXPOSE 8080

# Define the command to run the application
CMD ["python", "app.py"]

