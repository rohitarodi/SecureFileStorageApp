# Use Python slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy entire app folder contents into the container
COPY ./app /app

# Copy root-level .env and requirements.txt
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (Flask: 5000, Streamlit: 8501)
EXPOSE 5000
EXPOSE 8501

# Start both Flask and Streamlit using a shell script
CMD ["sh", "-c", "python main.py & streamlit run front.py --server.port 8501"]
