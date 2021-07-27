FROM python:3

WORKDIR /usr/src/app

RUN mkdir /tmp/showimages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "daemon.py"]