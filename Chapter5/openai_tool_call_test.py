# 简单的OpenAI范式工具调用测试
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

apiKey = os.getenv("LLM_API_KEY")
baseurl = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL_ID", "gpt-4o-mini")  # 使用环境变量中的模型，默认使用 gpt-4o-mini

# 显示配置信息（用于调试）
print("🔍 当前配置:")
print(f"  API Key: {apiKey[:20]}..." if apiKey else "  API Key: 未设置")
print(f"  Base URL: {baseurl}")
print(f"  模型: {model}")
print()

if not apiKey or not baseurl:
    print("❌ 错误: 缺少必要的环境变量")
    print("   请确保 .env 文件中设置了 LLM_API_KEY 和 LLM_BASE_URL")
    exit(1)

client = OpenAI(api_key=apiKey, base_url=baseurl)

tools = [
  {
    "type": "function", #工具类型
    "function": {
      "name": "get_current_weather", #函数名称
      "description": "Get the current weather in a given location", #函数描述
      "parameters": { #函数参数
        "type": "object", #参数类型
        "properties": { #参数属性
          "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}, #参数名称和描述
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}, #参数枚举值
        },
        "required": ["location"], #参数必填
      },
    }
  }
]

messages = [
    {"role":"user","content":"What's the weather like in Boston today?"}
]

# 先测试不带工具调用的普通对话（确认代理服务可用）
print("📝 步骤1: 测试基础对话功能（不带工具调用）...")
try:
    test_completion = client.chat.completions.create(
        model=model,  # 使用环境变量中的模型
        messages=[{"role": "user", "content": "你好，请简单回复"}],
    )
    print("✅ 基础对话测试成功，代理服务可用")
    print()
except Exception as e:
    print(f"❌ 基础对话测试失败: {e}")
    print("   这说明代理服务本身可能有问题，请先解决基础连接问题")
    print(f"   当前使用的模型: {model}")
    print("   提示: 如果模型名称不正确，请检查 .env 文件中的 LLM_MODEL_ID")
    print()
    exit(1)

# 测试工具调用功能
print("📝 步骤2: 测试工具调用功能...")
try:
    print("🚀 正在调用 API（带工具调用）...")
    print(f"   模型: {model}")
    print(f"   工具数量: {len(tools)}")
    print()
    
    completion = client.chat.completions.create(
        model=model,  # 使用环境变量中的模型
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    print("✅ API 调用成功!")
    
    message = completion.choices[0].message
    
    # 检查是否有工具调用
    if message.tool_calls:
        print("\n" + "="*70)
        print("🔧 检测到工具调用（这是正常的！）")
        print("="*70)
        print("\n💡 为什么 content 为空？")
        print("   当模型决定调用工具时，它不会生成文本内容，而是返回工具调用请求。")
        print("   这是 OpenAI Function Calling 的正常行为。")
        print()
        print("📋 工具调用详情:")
        for tool_call in message.tool_calls:
            print(f"  - 工具名称: {tool_call.function.name}")
            print(f"  - 参数: {tool_call.function.arguments}")
            print(f"  - 调用ID: {tool_call.id}")
        print()
        
        # 将助手的消息（包含工具调用）添加到消息历史
        messages.append(message)
        
        # 模拟执行工具并返回结果
        print("🔨 步骤3: 执行工具并获取结果...")
        tool_results = []
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            import json
            tool_args = json.loads(tool_call.function.arguments)
            
            print(f"   执行工具: {tool_name}")
            print(f"   参数: {tool_args}")
            
            # 模拟工具执行（实际应该调用真实的工具函数）
            if tool_name == "get_current_weather":
                location = tool_args.get("location", "未知")
                unit = tool_args.get("unit", "celsius")
                # 模拟天气数据
                weather_result = f"波士顿今天天气晴朗，温度 22°{unit[0].upper()}"
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_name,
                    "content": weather_result
                })
                print(f"   结果: {weather_result}")
        
        # 将工具结果添加到消息历史
        messages.extend(tool_results)
        
        # 再次调用 API，让模型基于工具结果生成最终答案
        print("\n🔄 步骤4: 基于工具结果生成最终答案...")
        final_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,  # 仍然提供工具，但模型可能不再需要调用
        )
        
        final_message = final_completion.choices[0].message
        print("✅ 获得最终答案!")
        print("\n" + "="*70)
        print("💬 最终回复:")
        print("="*70)
        print(final_message.content)
        print("="*70)
        
    else:
        print("\n💬 模型直接回复（未使用工具）:")
        print(message.content if message.content else "(空内容)")
        

except Exception as e:
    error_msg = str(e)
    print(f"\n❌ API 调用失败: {error_msg}")
    
    if "unsupported_country_region_territory" in error_msg or "403" in error_msg:
        print("\n" + "="*70)
        print("🔍 问题诊断: 即使使用了反向代理，仍然遇到地区限制")
        print("="*70)
        print("\n可能的原因:")
        print("1. ❌ 反向代理服务本身不支持工具调用（Function Calling）")
        print("   - 某些代理服务只支持基础的聊天功能，不支持 tools 参数")
        print("   - 需要确认你的代理服务是否支持 OpenAI Function Calling")
        print()
        print("2. ❌ 反向代理服务配置问题")
        print("   - 代理服务可能没有正确转发 tools 参数")
        print("   - 或者代理服务对工具调用有特殊限制")
        print()
        print("3. ❌ 模型名称问题")
        print(f"   - 当前使用: '{model}'")
        print("   - 某些代理服务可能需要不同的模型名称格式")
        print("   - 建议尝试: 'gpt-4o', 'gpt-4o-mini', 'gpt-4', 'gpt-3.5-turbo' 等")
        print("   - 检查 .env 文件中的 LLM_MODEL_ID 设置")
        print()
        print("💡 解决方案:")
        print("1. 确认代理服务支持 Function Calling")
        print("   - 查看代理服务的文档")
        print("   - 联系代理服务提供商确认")
        print()
        print("2. 尝试不同的模型名称")
        print(f"   - 当前模型: '{model}'")
        print("   - 在 .env 文件中修改 LLM_MODEL_ID")
        print("   - 或使用代理服务推荐的模型名称（如 'gpt-4o'）")
        print()
        print("3. 使用支持工具调用的其他服务")
        print("   - DeepSeek API (支持 Function Calling)")
        print("   - 通义千问 API (支持 Function Calling)")
        print()
        print("4. 测试代理服务是否支持工具调用")
        print("   可以先测试不带 tools 参数的普通对话，确认代理可用")
        print("   然后再测试带 tools 参数的调用")
        print("="*70)
    else:
        print(f"\n其他错误类型: {type(e).__name__}")
        print("\n请检查:")
        print("1. API Key 是否正确")
        print("2. Base URL 是否正确（是否包含 /v1 后缀）")
        print("3. 网络连接是否正常")
        print("4. 代理服务是否正常运行")