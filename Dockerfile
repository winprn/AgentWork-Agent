FROM --platform=linux/amd64 python:3.11

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip
RUN pip install playwright
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "agent_server:app", "--host", "0.0.0.0", "--port", "8000"]
