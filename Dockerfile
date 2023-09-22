FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install streamlit

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
