import pandas as pd
import requests
import folium
from folium.plugins import HeatMap
import os

class SignalMapper:
    def __init__(self):
        # 直接设置API Key，避免.env文件编码问题
        self.amap_key = "308c6e2c574d334b06a71ef7c21f0b25"
        if not self.amap_key:
            raise ValueError("API密钥未设置")

    def read_excel_data(self, file_path):
        """读取Excel文件中的信号盲区数据"""
        try:
            df = pd.read_excel(file_path)
            required_columns = ['位置描述', '详细地址', '网络类型', '信号强度']
            if not all(col in df.columns for col in required_columns):
                print(f"Excel文件列名：{list(df.columns)}")
                raise ValueError(f"Excel文件必须包含以下列：{', '.join(required_columns)}")
            return df
        except Exception as e:
            print(f"读取Excel文件时出错：{str(e)}")
            return None

    def get_location_coordinates(self, location, detailed_address=None):
        """使用高德地图API获取位置坐标"""
        # 优先使用详细地址，如果没有则使用位置描述
        address = detailed_address if detailed_address and str(detailed_address) != 'nan' else location
        
        url = f"https://restapi.amap.com/v3/geocode/geo"
        params = {
            "key": self.amap_key,
            "address": address,
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            print(f"地名: {address}, 返回: {data}")  # 调试信息
            
            if data["status"] == "1" and data["geocodes"]:
                location_coords = data["geocodes"][0]["location"]
                lng, lat = map(float, location_coords.split(","))
                return lat, lng
            else:
                print(f"无法获取坐标：{address}, 错误信息：{data.get('info', '未知错误')}")
                return None
        except Exception as e:
            print(f"获取坐标时出错：{str(e)}")
            return None

    def generate_heatmap(self, df, output_file="signal_heatmap.html"):
        """生成信号盲区热力图"""
        # 创建地图对象，以南通市为中心
        nantong_center = [32.0307, 120.8664]  # 南通市中心坐标
        m = folium.Map(location=nantong_center, zoom_start=11)
        
        # 准备热力图数据
        heat_data = []
        success_count = 0
        
        for index, row in df.iterrows():
            print(f"处理第{index+1}条数据：{row['位置描述']}")
            
            # 获取坐标
            coords = self.get_location_coordinates(
                row['位置描述'], 
                row.get('详细地址', None)
            )
            
            if coords:
                # 根据信号强度设置权重（信号越弱，权重越大，在热力图中越红）
                signal_strength = row.get('信号强度', 5)
                weight = max(1, 11 - signal_strength)  # 信号强度1对应权重10，信号强度10对应权重1
                
                heat_data.append([coords[0], coords[1], weight])
                
                # 在地图上添加标记点，显示详细信息
                popup_text = f"""
                <b>{row['位置描述']}</b><br>
                详细地址：{row.get('详细地址', '未提供')}<br>
                网络类型：{row['网络类型']}<br>
                信号强度：{signal_strength}/10<br>
                上报时间：{row.get('上报时间', '未知')}<br>
                上报人：{row.get('上报人', '匿名')}<br>
                备注：{row.get('备注', '无')}
                """
                
                # 根据信号强度选择标记颜色
                if signal_strength <= 2:
                    color = 'red'  # 信号很差
                elif signal_strength <= 4:
                    color = 'orange'  # 信号较差
                elif signal_strength <= 6:
                    color = 'yellow'  # 信号一般
                else:
                    color = 'green'  # 信号较好
                
                folium.Marker(
                    coords,
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"{row['位置描述']} (信号强度: {signal_strength}/10)",
                    icon=folium.Icon(color=color, icon='signal')
                ).add_to(m)
                
                success_count += 1
            else:
                print(f"跳过无法获取坐标的位置：{row['位置描述']}")
        
        if heat_data:
            # 添加热力图层
            HeatMap(heat_data, radius=20, blur=15, max_zoom=1).add_to(m)
            print(f"成功处理 {success_count} 个位置点")
        else:
            print("警告：没有成功获取到任何位置的坐标，热力图将为空")
        
        # 保存地图
        m.save(output_file)
        print(f"热力图已生成：{output_file}")

def main():
    # 创建SignalMapper实例
    try:
        mapper = SignalMapper()
    except ValueError as e:
        print(f"初始化失败：{str(e)}")
        return
    
    # 读取Excel文件
    excel_file = input("请输入Excel文件路径：")
    df = mapper.read_excel_data(excel_file)
    
    if df is not None:
        print(f"成功读取 {len(df)} 条数据")
        # 生成热力图
        mapper.generate_heatmap(df)
    else:
        print("无法处理Excel文件，请检查文件格式和内容。")

if __name__ == "__main__":
    main() 