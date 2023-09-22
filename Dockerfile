FROM python:3.9
WORKDIR /app
COPY . /app
CMD ["streamlit", "run", "main.py"]
