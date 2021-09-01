FROM python:3.7-slim
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=localhost
ENV FLASK_RUN_PORT=5000
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pip setuptools wheel
RUN apt-get update && echo y | apt-get install gcc git
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN git clone https://github.com/alimuldal/diptest.git
RUN cd diptest && python setup.py build_ext -i -f && python setup.py install && cd ..
RUN pip3 install uwsgi

EXPOSE 5000
COPY . .
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:5000", "--module", "app:app", "--processes", "1", "--threads", "8"]
