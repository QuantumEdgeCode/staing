#2026/05/07 02:16:00 GMT+08:00
#!/bin/sh

set -eux

CITIES=(
  "北京:Beijing"
  "上海:Shanghai"
  "武汉:Wuhan"
  "杭州:Hangzhou"
  "伦敦:London"
  "纽约:New York"
  "东京:Tokyo"
  "巴黎:Paris"
  "莫斯科:Moscow"
  "悉尼:Sydney"
  "柏林:Berlin"
  "罗马:Rome"
  "马德里:Madrid"
  "首尔:Seoul"
  "曼谷:Bangkok"
  "新加坡:Singapore"
  "迪拜:Dubai"
  "孟买:Mumbai"
  "伊斯坦布尔:Istanbul"
  "多伦多:Toronto"
  "巴塞罗那:Barcelona"
  "安卡拉:Ankara"
  "德黑兰:Tehran"
  "马什哈德:Mashhad"
  "伊斯法罕:Isfahan"
  "设拉子:Shiraz"
  "大不里士:Tabriz"
  "库姆:Qom"
  "平壤:Pyongyang"
  "喀布尔:Kabul"
  "摩加迪沙:Mogadishu"
  "萨那:Sanaa"
  "阿姆斯特丹:Amsterdam"
  "雅典:Athens"
  "金沙萨:Kinshasa"
  "加拉加斯:Caracas"
  "阿布扎比:Abu Dhabi"
  "三亚:Sanya"
  "香港:Hong Kong"
  "新德里:New Delhi"
  "巴格达:Baghdad"
  "科威特城:Kuwait City"
  "多哈:Doha"
  "麦纳麦:Manama"
  "马斯喀特:Muscat"
  "安曼:Amman"
  "贝鲁特:Beirut"
  "大马士革:Damascus"
  "特拉维夫:Tel Aviv"
  "拉姆安拉:Ramallah"
  "尼科西亚:Nicosia"
  "开罗:Cairo"
  "维也纳:Vienna"
  "布拉格:Prague"
  "哥本哈根:Copenhagen"
  "华沙:Warsaw"
)

LANGUAGE="zh-CN"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

> result.txt

for ITEM in "${CITIES[@]}"
do
  CN_NAME="${ITEM%%:*}"
  EN_NAME="${ITEM##*:}"
  
  WEATHER=$(curl -L \
    -H "Accept-Language: $LANGUAGE" \
    -H "User-Agent: $UA" \
    -s \
    "wttr.in/${EN_NAME}?format=4&m" | \
    grep -oP '<div class="term-container">\K[^<]+' | \
    sed 's/&#47;/\//g')
  
  # 去掉原始返回中的 "英文名: " 前缀
  WEATHER_CLEAN=$(echo "$WEATHER" | sed "s/^.*: //")
  
  echo "${CN_NAME} ${EN_NAME} ${WEATHER_CLEAN}" >> result.txt
done

cat result.txt
