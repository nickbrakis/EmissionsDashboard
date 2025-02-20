FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "src/app.py"]