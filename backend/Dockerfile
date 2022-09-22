FROM python:3.9.5
WORKDIR /Contract-shacl-repairs/backend

COPY . /Contract-shacl-repairs/backend
RUN pip install -r requirements.txt
COPY . /Contract-shacl-repairs/backend
CMD ["python", "app.py" ]

