FROM golang:1.16 AS gobuild

WORKDIR /usr/src/app
COPY . .
RUN cd myradio-uploader && go build

FROM python:3

WORKDIR /usr/src/app

RUN mkdir /tmp/showimages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=gobuild /usr/src/app/myradio-uploader/myradio-uploader /myradio-uploader/myradio-uploader

CMD ["python", "daemon.py"]