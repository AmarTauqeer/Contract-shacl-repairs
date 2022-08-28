FROM python:3.9.5
WORKDIR /contract-shacl-repairs/backend

COPY . /contract-shacl-repairs/backend
RUN pip install -r requirements.txt
COPY . /contract-shacl-repairs/backend
CMD ["python", "app.py" ]

