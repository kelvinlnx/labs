FROM python:3.9-slim

# 1. Setup the user and working directory first
RUN useradd --create-home appuser
WORKDIR /home/appuser

# 2. Fix the PATH early
ENV PATH=/home/appuser/.local/bin:$PATH

# 3. Switch to the user BEFORE doing anything else
USER appuser

# 4. Copy ONLY requirements and install (Better Caching)
# Note: We don't need --chown here because we are already the 'appuser'
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 5. Copy the rest of the code (Only changes here trigger a rebuild of this layer)
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser static/ static/
COPY --chown=appuser:appuser templates/ templates/

EXPOSE 8080

CMD ["python", "app.py"]

