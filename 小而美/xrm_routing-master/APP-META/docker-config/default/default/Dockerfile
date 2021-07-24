# python 业务镜像模版
FROM harbor-k8s.xsyxsc.cn/appruntime/python_base:3.6.8

# 应用名
ARG APP_NAME
# 执行的Binary名字
ARG APP_BIN
# 环境名字
ARG ENV_TYPE
# 需要COPY打到镜像的内容
ARG ARCHIVE

ENV APP_NAME=${APP_NAME} APP_BIN=${APP_BIN} ENV_TYPE=${ENV_TYPE} IS_COMPOSE=true
ENV START_TIME_OUT=10  HEALTH_CHECK_PORT=8000



ADD flask_app/requirements.txt /appruntime/python/


RUN yum install git -y && \
    mkdir -p /appruntime/python/${APP_NAME} && \
    cd /appruntime/python/${APP_NAME} && \
    mv /appruntime/python/requirements.txt /appruntime/python/${APP_NAME}/ && \
    pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY flask_app/  /appruntime/python/${APP_NAME}/

RUN echo 'gunicorn -c /appruntime/python/${APP_NAME}/gunicorn.conf.py app:app' >>/appruntime/python/start.sh
