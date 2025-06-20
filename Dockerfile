FROM python:3.12.4

WORKDIR /app

EXPOSE 8000

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

