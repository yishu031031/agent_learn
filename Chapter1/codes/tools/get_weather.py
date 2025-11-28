import json
import requests

def get_weather(city:str)->str:
    '''
    通过调用 wrttr.in 的 API 获取指定城市的天气信息
    '''
    #API端点，请求JSON格式的天气数据
    url = f"https://wttr.in/{city}?format=j1"

    try:
        #发起网络请求
        response = requests.get(url)
        #检查url响应
        response.raise_for_status()
        #解析JSON数据
        data = response.json()

        #提取当前天气状况
        current_condition = data['current_condition'][0]
        weather = current_condition['weatherDesc'][0]['value']
        temperature = current_condition['temp_C']

        return f"{city}当前天气为:{weather},当前温度为:{temperature}°C"
    except requests.exceptions.RequestException as e:
        return f"错误：查询天气时遇到网络问题 -{e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"错误：解析天气数据失败，可能是城市名称无效 -{e}"
    

