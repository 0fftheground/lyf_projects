FROM python:3.6
WORKDIR /Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

COPY . .

CMD ["gunicorn", "main:app", "-c", "./gunicorn.conf.py"]