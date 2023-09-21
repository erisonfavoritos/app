FROM python:3.9

WORKDIR /aplicativo

COPY . /aplicativo

RUN pip install --no-cache-dir -r requisitos.txt

CMD ["streamlit", "run", "main.py"]
