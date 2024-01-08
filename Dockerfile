
FROM python:3.9-slim

# ensure local python is preferred over distribution python
# ENV PATH /usr/local/bin:$PATH

WORKDIR /src

COPY main.py .

CMD ["python3", "main.py"]

