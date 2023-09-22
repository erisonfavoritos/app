FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install streamlit

CMD ["streamlit", "run", "main.py"]
