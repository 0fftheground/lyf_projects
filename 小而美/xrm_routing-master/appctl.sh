#!/bin/bash

ACTION=$1
APP_NAME=$2
IMAGE_FULL_NAME=$3
ENV_TYPE=$4
HEALTH_CHECK_PORT=8000
HEALTH_CHECK_URL=""


cd /appruntime/python/${APP_NAME}

START_TIME_OUT=10
echo IMAGE_FULL_NAME IS : ${IMAGE_FULL_NAME}
echo ENV_TYPE IS : ${ENV_TYPE}


_online(){
    echo "[INFO]online donoting"

}

_offline(){
    echo "[INFO]offline donoting"
}


start(){
    echo "[INFO] begin start docker-compose"
    echo "[INFO] edit docker-compose-ciflow.yaml"
	  cp -rf APP-META/docker-compose/docker-compose.yml docker-compose.yaml
	  sed -i "s#{{image_url}}#$IMAGE_FULL_NAME#g" docker-compose.yaml
	  sed -i "s/{{env_type}}/$ENV_TYPE/g" docker-compose.yaml
	  echo "[INFO] exec docker-compose up -d"
    docker-compose up -d
    echo "[INFO] start application done"
    echo "[INFO] begin online"
	  check
    _online
    echo "[INFO] online done"
}


stop(){
    _offline
    container=`docker ps -a | grep ${APP_NAME} | awk '{print $1}'`
    echo "[INFO] stop docker-compose"
    if [[ "${container}" != "" ]]; then
        docker rm -f ${container}
    fi
    echo "[INFO] stop application done"
}


restart(){
	echo "[INFO] restart docker-compose ${APP_NAME}"
    docker-compose restart ${APP_NAME}
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
    restart )
        stop
        start
    ;;
    check )
        check
    ;;
    * )
      stop
      start
      check
    ;;
esac





