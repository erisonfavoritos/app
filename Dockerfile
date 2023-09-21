DE python:3.9

WORKDIR /aplicativo

CÓPIA DE . /aplicativo

EXECUTAR pip install --no-cache-dir -r requisitos.txt

CMD ["python","streamlit", "main.py"]
