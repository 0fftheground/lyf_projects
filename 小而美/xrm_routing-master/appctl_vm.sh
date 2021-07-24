#!/bin/bash

ACTION=$1
APP_NAME=$2
ENV_TYPE=$3
HEALTH_CHECK_PORT=8000
HEALTH_CHECK_URL=""


cd /appruntime/python/${APP_NAME}

START_TIME_OUT=10
echo IMAGE_FULL_NAME IS : ${IMAGE_FULL_NAME}
echo ENV_TYPE IS : ${ENV_TYPE}


_pre_install(){
    if which git >/dev/null 2>&1; then
        yum install git -y || exit 1
    fi
    if [[ ! -d /appruntime/python/${APP_NAME}/venv ]]; then
        if ! which pip3 >/dev/null 2>&1; then
            echo "[INFO] python3 not exist,try to install"
            yum install python3 -y || exit 1
        fi
        echo "[INFO] install virtualenv"
        pip3 install virtualenv -i https://mirrors.aliyun.com/pypi/simple/ 2>&1 || exit 1
        echo "[INFO] create virtualenv"
        echo "[INFO] PATH=${PATH}"
        export PATH=/usr/local/bin:${PATH}
        ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv
        virtualenv -p python3 /appruntime/python/${APP_NAME}/venv || exit 1
    fi
    echo "[INFO] add virtualenv to path"
    export PATH=/appruntime/python/${APP_NAME}/venv/bin:${PATH}
    echo "[INFO] new PATH=${PATH}"
    echo "[INFO] try to install requirements"
    pip install -r /appruntime/python/${APP_NAME}/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ || exit 1
}

_online(){
    echo "[INFO]online donoting"

}

_offline(){
    echo "[INFO]offline donoting"
}


start(){
    echo "[INFO] begin start application"
    _pre_install
    echo "[INFO] start gunicorn process"
    cd /appruntime/python/${APP_NAME}
    nohup gunicorn -c gunicorn.conf.py app:app > start.log 2>&1 &
    check
    echo "[INFO] start application done"
    echo "[INFO] begin online"
    _online
    echo "[INFO] online done"
}


stop(){
    _offline
    pids=`ps -ef |grep -v 'grep' | grep "python/${APP_NAME}/venv" | awk '{print $2}'`
    echo "[INFO] stop application ${pids}"
    if [[ "${pids}" != "" ]]; then
        kill -15 ${pids}
    fi
    pids=`ps -ef |grep -v 'grep' | grep "python/${APP_NAME}/venv" | awk '{print $2}'`
    if [[ "${pids}" != "" ]]; then
        echo "[INFO] still has some process, try force kill"
        kill -9 ${pids}
    fi
    echo "[INFO] stop application done"
}


restart(){
    stop
    start
}

check(){
    for((i=1;i<=${START_TIME_OUT};i++));
    do
        success=`curl -I -s  127.0.0.1:${HEALTH_CHECK_PORT}/${HEALTH_CHECK_URL} | grep '200 OK'`
        if [[ "${success}" = "" ]]; then
            if [[ "$i" = "${START_TIME_OUT}" ]]; then
                echo "[ERROR] application start in 10s failed"
                exit 1
            fi
            echo "[INFO] waiting for ready ..."
            sleep 1
        else
            echo "[INFO] application start success"
            break
        fi
    done
}


case ${ACTION} in
    start )
        start
    ;;
    stop )
        stop
    ;;

    check )
        check
    ;;
    * | restart )
        restart
    ;;
esac





