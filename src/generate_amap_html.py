#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图信号盲区可视化生成器
读取Excel数据，生成高德地图HTML文件
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime

# 高德地图API配置 - 从配置文件读取
import os
try:
    from config import AMAP_API_KEY, AMAP_JS_KEY
except ImportError:
    # 如果没有配置文件，从环境变量读取
    AMAP_API_KEY = os.getenv('AMAP_API_KEY', '')
    AMAP_JS_KEY = os.getenv('AMAP_JS_KEY', '')
    
    if not AMAP_API_KEY or not AMAP_JS_KEY:
        print("⚠️  警告: 未找到API密钥配置")
        print("请按照以下步骤配置:")
        print("1. 复制 config_template.py 为 config.py")
        print("2. 在 config.py 中填入您的高德地图API密钥")
        print("3. 或设置环境变量 AMAP_API_KEY 和 AMAP_JS_KEY")

def geocode_address(address):
    """使用高德地图API进行地理编码"""
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        'key': AMAP_API_KEY,
        'address': address,
        'output': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == '1' and data['geocodes']:
            location = data['geocodes'][0]['location']
            lng, lat = location.split(',')
            return float(lng), float(lat)
        else:
            print(f"地理编码失败: {address} - {data.get('info', '未知错误')}")
            return None, None
    except Exception as e:
        print(f"地理编码异常: {address} - {str(e)}")
        return None, None

def generate_amap_html(excel_file, output_file):
    """生成高德地图HTML文件"""
    
    # 读取Excel数据
    print("正在读取Excel数据...")
    try:
        df = pd.read_excel(excel_file)
        print(f"成功读取 {len(df)} 条记录")
    except Exception as e:
        print(f"读取Excel文件失败: {str(e)}")
        return False
    
    # 验证必要的列
    required_columns = ['位置描述', '详细地址', '网络类型', '信号强度', '上报时间', '上报人', '备注']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Excel文件缺少必要的列: {missing_columns}")
        return False
    
    # 处理数据并进行地理编码
    signal_data = []
    print("正在进行地理编码...")
    
    for index, row in df.iterrows():
        print(f"处理第 {index + 1}/{len(df)} 条记录: {row['位置描述']}")
        
        # 地理编码
        lng, lat = geocode_address(row['详细地址'])
        if lng is None or lat is None:
            print(f"跳过无法定位的地址: {row['详细地址']}")
            continue
        
        # 构建数据记录
        record = {
            'name': str(row['位置描述']),
            'address': str(row['详细地址']),
            'lng': lng,
            'lat': lat,
            'signal': int(row['信号强度']),
            'network': str(row['网络类型']),
            'reporter': str(row['上报人']),
            'time': str(row['上报时间']),
            'note': str(row['备注'])
        }
        signal_data.append(record)
        
        # 避免API调用过快
        time.sleep(0.1)
    
    if not signal_data:
        print("没有成功处理的数据记录")
        return False
    
    print(f"成功处理 {len(signal_data)} 条记录")
    
    # 计算统计信息
    total_points = len(signal_data)
    severe_blindspots = len([d for d in signal_data if d['signal'] <= 2])
    avg_signal = sum(d['signal'] for d in signal_data) / total_points
    g5_coverage = len([d for d in signal_data if d['network'] == '5G']) / total_points * 100
    
    # 生成JavaScript数据
    js_data = json.dumps(signal_data, ensure_ascii=False, indent=12)
    
    # HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>信号盲区分布图 - 高德地图版</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .map-container {{
            position: relative;
            height: 600px;
            margin: 20px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        #map {{
            width: 100%;
            height: 100%;
        }}
        .legend {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            min-width: 200px;
        }}
        .legend h4 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 1.1em;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 8px 0;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 8px;
            border: 2px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        .red {{ background-color: #dc3545; }}
        .orange {{ background-color: #fd7e14; }}
        .yellow {{ background-color: #ffc107; }}
        .green {{ background-color: #28a745; }}
        .legend-text {{
            font-size: 0.9em;
            color: #666;
        }}
        .info-panel {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
        }}
        .info-panel h4 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 0.9em;
        }}
        .stat-item {{
            text-align: center;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        .stat-number {{
            font-weight: bold;
            color: #333;
            display: block;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.8em;
        }}
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            z-index: 2000;
        }}
        .timestamp {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(255,255,255,0.9);
            padding: 10px;
            border-radius: 5px;
            font-size: 0.8em;
            color: #666;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗺️ 信号盲区分布图</h1>
        <p>基于高德地图的信号质量可视化分析</p>
    </div>

    <div class="map-container">
        <div id="map"></div>
        <div class="loading" id="loading">
            <div>正在加载地图...</div>
        </div>
        
        <div class="legend">
            <h4>📶 信号强度图例</h4>
            <div class="legend-item">
                <div class="legend-color red"></div>
                <span class="legend-text">严重盲区 (1-2分)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color orange"></div>
                <span class="legend-text">信号较差 (3-4分)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color yellow"></div>
                <span class="legend-text">信号一般 (5-6分)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color green"></div>
                <span class="legend-text">信号良好 (7-10分)</span>
            </div>
        </div>

        <div class="info-panel">
            <h4>📊 统计信息</h4>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_points}</span>
                    <span class="stat-label">监测点位</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{severe_blindspots}</span>
                    <span class="stat-label">严重盲区</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{g5_coverage:.0f}%</span>
                    <span class="stat-label">5G覆盖</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{avg_signal:.1f}</span>
                    <span class="stat-label">平均强度</span>
                </div>
            </div>
        </div>
        
        <div class="timestamp">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>

    <script src="https://webapi.amap.com/maps?v=2.0&key={AMAP_JS_KEY}"></script>
    <script>
        // 信号盲区数据
        const signalData = {js_data};

        // 获取信号强度对应的颜色
        function getSignalColor(signal) {{
            if (signal <= 2) return '#dc3545'; // 红色
            if (signal <= 4) return '#fd7e14'; // 橙色
            if (signal <= 6) return '#ffc107'; // 黄色
            return '#28a745'; // 绿色
        }}

        // 获取信号强度描述
        function getSignalDesc(signal) {{
            if (signal <= 2) return '严重盲区';
            if (signal <= 4) return '信号较差';
            if (signal <= 6) return '信号一般';
            return '信号良好';
        }}

        // 初始化地图
        function initMap() {{
            // 创建地图实例
            const map = new AMap.Map('map', {{
                zoom: 10,
                center: [signalData[0].lng, signalData[0].lat],
                mapStyle: 'amap://styles/normal',
                viewMode: '2D'
            }});

            // 隐藏加载提示
            document.getElementById('loading').style.display = 'none';

            // 添加标记点
            signalData.forEach(point => {{
                // 创建标记
                const marker = new AMap.Marker({{
                    position: [point.lng, point.lat],
                    title: point.name,
                    icon: new AMap.Icon({{
                        size: new AMap.Size(30, 30),
                        image: createMarkerIcon(point.signal),
                        imageSize: new AMap.Size(30, 30)
                    }})
                }});

                // 创建信息窗体内容
                const infoContent = `
                    <div style="padding: 10px; max-width: 280px;">
                        <h4 style="margin: 0 0 10px 0; color: #333; font-size: 1.1em;">${{point.name}}</h4>
                        <div style="margin: 5px 0;"><strong>地址：</strong>${{point.address}}</div>
                        <div style="margin: 5px 0;"><strong>信号强度：</strong>
                            <span style="color: ${{getSignalColor(point.signal)}}; font-weight: bold;">
                                ${{point.signal}}/10 (${{getSignalDesc(point.signal)}})
                            </span>
                        </div>
                        <div style="margin: 5px 0;"><strong>网络类型：</strong>
                            <span style="background: #e3f2fd; color: #1976d2; padding: 2px 6px; border-radius: 3px; font-size: 0.9em;">
                                ${{point.network}}
                            </span>
                        </div>
                        <div style="margin: 5px 0;"><strong>上报时间：</strong>${{point.time}}</div>
                        <div style="margin: 5px 0;"><strong>上报人：</strong>${{point.reporter}}</div>
                        <div style="margin: 5px 0;"><strong>问题描述：</strong>${{point.note}}</div>
                    </div>
                `;

                // 创建信息窗体
                const infoWindow = new AMap.InfoWindow({{
                    content: infoContent,
                    offset: new AMap.Pixel(0, -30)
                }});

                // 点击标记显示信息窗体
                marker.on('click', function() {{
                    infoWindow.open(map, marker.getPosition());
                }});

                // 添加标记到地图
                map.add(marker);
            }});

            // 自适应显示所有标记点
            if (signalData.length > 0) {{
                const bounds = new AMap.Bounds();
                signalData.forEach(point => {{
                    bounds.extend([point.lng, point.lat]);
                }});
                map.setBounds(bounds, false, [50, 50, 50, 50]);
            }}
        }}

        // 创建标记图标
        function createMarkerIcon(signal) {{
            const canvas = document.createElement('canvas');
            canvas.width = 30;
            canvas.height = 30;
            const ctx = canvas.getContext('2d');

            // 绘制外圆
            ctx.beginPath();
            ctx.arc(15, 15, 14, 0, 2 * Math.PI);
            ctx.fillStyle = getSignalColor(signal);
            ctx.fill();
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 2;
            ctx.stroke();

            // 绘制信号强度数字
            ctx.fillStyle = 'white';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(signal.toString(), 15, 15);

            return canvas.toDataURL();
        }}

        // 页面加载完成后初始化地图
        window.onload = function() {{
            // 等待高德地图API加载完成
            if (typeof AMap !== 'undefined') {{
                initMap();
            }} else {{
                // 如果API未加载，等待一段时间后重试
                setTimeout(() => {{
                    if (typeof AMap !== 'undefined') {{
                        initMap();
                    }} else {{
                        document.getElementById('loading').innerHTML = '<div style="color: red;">地图加载失败，请检查网络连接</div>';
                    }}
                }}, 2000);
            }}
        }};
    </script>
</body>
</html>"""
    
    # 写入HTML文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"成功生成高德地图HTML文件: {output_file}")
        return True
    except Exception as e:
        print(f"写入HTML文件失败: {str(e)}")
        return False

def main():
    """主函数"""
    excel_file = "../data/example_data.xlsx"
    output_file = "amap_signal_heatmap.html"
    
    print("🗺️ 高德地图信号盲区可视化生成器")
    print("=" * 50)
    
    if generate_amap_html(excel_file, output_file):
        print("✅ 生成完成！")
        print(f"📄 HTML文件: {output_file}")
        print("💡 请在浏览器中打开HTML文件查看地图")
    else:
        print("❌ 生成失败！")

if __name__ == "__main__":
    main() 