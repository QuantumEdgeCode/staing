import matplotlib.pyplot as plt
import numpy as np
import re
import math
from datetime import datetime

# 从 result.txt 读取数据
with open('result.txt', 'r', encoding='utf-8') as f:
    data_raw = f.read()

# 解析数据
def parse_weather(data_raw):
    cities = []
    temps = []
    winds = []
    has_data = []
    
    for line in data_raw.strip().split('\n'):
        if not line.strip():
            continue
        
        # 提取中文名（第一个空格前的内容）
        cn_name = line.split(' ')[0]
        cities.append(cn_name)
        
        # 提取温度
        temp_match = re.search(r'🌡️\+(\d+)°C', line)
        if temp_match:
            temps.append(int(temp_match.group(1)))
        else:
            temps.append(None)
        
        # 提取风速
        wind_match = re.search(r'🌬️[↗↘↙↖↑↓←→](\d+)km/h', line)
        if wind_match:
            winds.append(int(wind_match.group(1)))
        else:
            winds.append(None)
        
        has_data.append(temp_match is not None and wind_match is not None)
    
    return cities, temps, winds, has_data

cities, temps, winds, has_data = parse_weather(data_raw)

# 过滤有效数据
filtered_cities = []
filtered_temps = []
filtered_winds = []
for city, temp, wind, valid in zip(cities, temps, winds, has_data):
    if valid:
        filtered_cities.append(city)
        filtered_temps.append(temp)
        filtered_winds.append(wind)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 获取当前日期作为文件名时间戳
file_date = datetime.now().strftime('%Y-%m-%d')
today_display = datetime.now().strftime('%Y-%m-%d %H:%M')

# 颜色函数
def get_temp_color(temp):
    if temp >= 30:
        return '#FF4444'
    elif temp >= 20:
        return '#FFAA00'
    elif temp >= 10:
        return '#44AAFF'
    else:
        return '#4444FF'

def get_wind_color(wind):
    if wind >= 20:
        return '#FF4444'
    elif wind >= 10:
        return '#FFAA00'
    else:
        return '#44AAFF'

# ==================== 主图：总览 ====================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(24, 20), gridspec_kw={'height_ratios': [1, 1]})

y_pos = range(len(filtered_cities))

colors_temp = [get_temp_color(t) for t in filtered_temps]
colors_wind = [get_wind_color(w) for w in filtered_winds]

# 温度子图
ax1.barh(y_pos, filtered_temps, color=colors_temp, edgecolor='white', linewidth=0.5, height=0.7)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(filtered_cities, fontsize=11)
ax1.set_xlabel('温度 (°C)', fontsize=14, fontweight='bold')
ax1.set_title('全球主要城市温度 (°C)', fontsize=18, fontweight='bold', pad=15)
ax1.invert_yaxis()
ax1.grid(axis='x', alpha=0.3, linestyle='--')
ax1.set_xlim(0, max(filtered_temps) * 1.12)

for i, temp in enumerate(filtered_temps):
    ax1.text(temp + 0.5, i, f'{temp}°C', va='center', fontsize=9, fontweight='bold')

# 风速子图
ax2.barh(y_pos, filtered_winds, color=colors_wind, edgecolor='white', linewidth=0.5, height=0.7)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(filtered_cities, fontsize=11)
ax2.set_xlabel('风速 (km/h)', fontsize=14, fontweight='bold')
ax2.set_title('全球主要城市风速 (km/h)', fontsize=18, fontweight='bold', pad=15)
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3, linestyle='--')
ax2.set_xlim(0, max(filtered_winds) * 1.12)

for i, wind in enumerate(filtered_winds):
    ax2.text(wind + 0.5, i, f'{wind} km/h', va='center', fontsize=9, fontweight='bold')

fig.suptitle(f'全球主要城市天气数据可视化 - 总览 ({today_display})', fontsize=22, fontweight='bold', y=0.985)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'weather_overview_{file_date}.png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"✅ 总览图已保存: weather_overview_{file_date}.png")

# ==================== 分页：温度排名 ====================
temp_sorted = sorted(zip(filtered_cities, filtered_temps), key=lambda x: x[1], reverse=True)
temp_cities_sorted, temp_vals_sorted = zip(*temp_sorted)

cities_per_page = 20
total_pages = math.ceil(len(temp_cities_sorted) / cities_per_page)

for page in range(total_pages):
    start = page * cities_per_page
    end = min(start + cities_per_page, len(temp_cities_sorted))
    
    page_cities = temp_cities_sorted[start:end]
    page_temps = temp_vals_sorted[start:end]
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    y_pos = range(len(page_cities))
    colors = [get_temp_color(t) for t in page_temps]
    
    ax.barh(y_pos, page_temps, color=colors, edgecolor='white', linewidth=0.8, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(page_cities, fontsize=12)
    ax.set_xlabel('温度 (°C)', fontsize=14, fontweight='bold')
    ax.set_title(f'城市温度排名 - 第{page+1}/{total_pages}页', fontsize=18, fontweight='bold', pad=15)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_xlim(0, max(page_temps) * 1.12)
    
    for i, temp in enumerate(page_temps):
        ax.text(temp + 0.5, i, f'{temp}°C', va='center', fontsize=10, fontweight='bold')
    
    fig.suptitle(f'全球主要城市温度排名 ({today_display})', fontsize=20, fontweight='bold', y=0.985)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'weather_temp_page{page+1}_{file_date}.png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"✅ 温度排名第{page+1}页已保存: weather_temp_page{page+1}_{file_date}.png")

# ==================== 分页：风速排名 ====================
wind_sorted = sorted(zip(filtered_cities, filtered_winds), key=lambda x: x[1], reverse=True)
wind_cities_sorted, wind_vals_sorted = zip(*wind_sorted)

total_pages = math.ceil(len(wind_cities_sorted) / cities_per_page)

for page in range(total_pages):
    start = page * cities_per_page
    end = min(start + cities_per_page, len(wind_cities_sorted))
    
    page_cities = wind_cities_sorted[start:end]
    page_winds = wind_vals_sorted[start:end]
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    y_pos = range(len(page_cities))
    colors = [get_wind_color(w) for w in page_winds]
    
    ax.barh(y_pos, page_winds, color=colors, edgecolor='white', linewidth=0.8, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(page_cities, fontsize=12)
    ax.set_xlabel('风速 (km/h)', fontsize=14, fontweight='bold')
    ax.set_title(f'城市风速排名 - 第{page+1}/{total_pages}页', fontsize=18, fontweight='bold', pad=15)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_xlim(0, max(page_winds) * 1.12)
    
    for i, wind in enumerate(page_winds):
        ax.text(wind + 0.5, i, f'{wind} km/h', va='center', fontsize=10, fontweight='bold')
    
    fig.suptitle(f'全球主要城市风速排名 ({today_display})', fontsize=20, fontweight='bold', y=0.985)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'weather_wind_page{page+1}_{file_date}.png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"✅ 风速排名第{page+1}页已保存: weather_wind_page{page+1}_{file_date}.png")

# ==================== 统计汇总 ====================
missing_cities = [c for c, v in zip(cities, has_data) if not v]
print(f"\n📊 统计汇总:")
print(f"   数据来源: result.txt")
print(f"   总城市数: {len(cities)}")
print(f"   有效数据: {len(filtered_cities)}")
print(f"   数据缺失: {len(missing_cities)} ({', '.join(missing_cities)})")
print(f"   当前时间: {today_display}")
print(f"   生成图片:")
print(f"     - weather_overview_{file_date}.png (总览)")
print(f"     - weather_temp_page*_{file_date}.png (温度排名分页)")
print(f"     - weather_wind_page*_{file_date}.png (风速排名分页)")
