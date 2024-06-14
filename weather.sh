#!/bin/sh

set -eux

CITIES=("Beijing" "Shanghai" "Wuhan" "Hangzhou" "London")
LANGUAGE="zh-CN"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

# 清空result.html文件
> result.html

for CITY in "${CITIES[@]}"
do
  echo "获取 ${CITY} 的天气预报..." >> result.html
  curl -L \
    -H "Accept-Language: $LANGUAGE" \
    -H "User-Agent: $UA" \
    -o - \
    "wttr.in/${CITY}?format=4&m" >> result.html
  echo "" >> result.html
done
