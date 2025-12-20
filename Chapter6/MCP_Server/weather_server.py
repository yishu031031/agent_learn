"""
天气查询 MCP 服务器

使用 FastMCP 构建的 MCP 服务器，提供天气查询功能。
支持通过 wttr.in API 查询全球城市的天气信息。
"""

import json
import requests
from fastmcp import FastMCP

# 初始化 FastMCP 服务器
mcp = FastMCP("Weather MCP Server")


@mcp.tool()
def get_weather(city: str) -> str:
    """
    获取指定城市的当前天气信息。
    
    该工具通过调用 wttr.in API 获取实时天气数据，包括天气状况和温度。
    
    Args:
        city: 城市名称，支持中文和英文城市名（例如："北京"、"Beijing"、"New York"）
        
    Returns:
        包含天气状况和温度的字符串描述，格式为："{city}当前天气为:{weather},当前温度为:{temperature}°C"
        
    Examples:
        >>> get_weather("北京")
        "北京当前天气为:Partly cloudy,当前温度为:15°C"
        
        >>> get_weather("New York")
        "New York当前天气为:Sunny,当前温度为:22°C"
    """
    # API端点，请求JSON格式的天气数据
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        # 发起网络请求
        response = requests.get(url, timeout=10)
        # 检查HTTP响应状态
        response.raise_for_status()
        # 解析JSON数据
        data = response.json()
        
        # 提取当前天气状况
        current_condition = data['current_condition'][0]
        weather = current_condition['weatherDesc'][0]['value']
        temperature = current_condition['temp_C']
        
        return f"{city}当前天气为:{weather},当前温度为:{temperature}°C"
        
    except requests.exceptions.Timeout:
        return f"错误：查询{city}的天气时请求超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"错误：查询{city}的天气时遇到网络问题 - {str(e)}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"错误：解析{city}的天气数据失败，可能是城市名称无效或API响应格式变化 - {str(e)}"
    except Exception as e:
        return f"错误：查询{city}的天气时发生未知错误 - {str(e)}"


@mcp.tool()
def get_weather_detailed(city: str) -> str:
    """
    获取指定城市的详细天气信息，包括温度、湿度、风速等。
    
    Args:
        city: 城市名称，支持中文和英文城市名
        
    Returns:
        包含详细天气信息的JSON格式字符串
    """
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data['current_condition'][0]
        weather_info = {
            "城市": city,
            "天气状况": current['weatherDesc'][0]['value'],
            "温度": f"{current['temp_C']}°C",
            "体感温度": f"{current['FeelsLikeC']}°C",
            "湿度": f"{current['humidity']}%",
            "风速": f"{current['windspeedKmph']} km/h",
            "能见度": f"{current['visibility']} km",
            "气压": f"{current['pressure']} mb"
        }
        
        return json.dumps(weather_info, ensure_ascii=False, indent=2)
        
    except requests.exceptions.Timeout:
        return f"错误：查询{city}的详细天气时请求超时"
    except requests.exceptions.RequestException as e:
        return f"错误：查询{city}的详细天气时遇到网络问题 - {str(e)}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"错误：解析{city}的详细天气数据失败 - {str(e)}"
    except Exception as e:
        return f"错误：查询{city}的详细天气时发生未知错误 - {str(e)}"


if __name__ == "__main__":
    # 运行 MCP 服务器（使用 Stdio 传输）
    # 可以通过命令行参数指定传输方式
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        # HTTP 模式：使用 uvicorn 运行
        print("启动 HTTP 模式的 MCP 服务器...")
        print("运行命令: uvicorn weather_server:mcp.http_app --host 0.0.0.0 --port 8000")
    else:
        # Stdio 模式（默认）
        print("启动 Stdio 模式的 MCP 服务器...")
        mcp.run()

