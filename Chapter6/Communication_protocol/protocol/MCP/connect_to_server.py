import asyncio
from hello_agents.protocols import MCPClient
import sys

async def connect_to_server():
    # 方式1：连接到社区提供的文件系统服务器
    # npx会自动下载并运行@modelcontextprotocol/server-filesystem包

    command = "npx.cmd" if sys.platform == "win32" else "npx"

    client = MCPClient([
        command, "-y",
        "@modelcontextprotocol/server-filesystem",
        "."  # 指定根目录
    ])

    # 使用async with确保连接正确关闭
    async with client:
        # 在这里使用client
        tools = await client.list_tools()
        print(f"可用工具: {[t['name'] for t in tools]}")
    '''
    📝 使用 Stdio 传输 (命令): npx.cmd -y @modelcontextprotocol/server-filesystem .
    🔗 连接到 MCP 服务器...
    ✅ 连接成功！
    可用工具: ['read_file', 'read_text_file', 'read_media_file', 'read_multiple_files', 'write_file', 
        'edit_file', 'create_directory', 'list_directory', 'list_directory_with_sizes', 'directory_tree', 'move_file', 
        'search_files', 'get_file_info', 'list_allowed_directories']
    '''

    # 方式2：连接到自定义的Python MCP服务器
    '''
    client = MCPClient(["python", "my_mcp_server.py"])
    async with client:
        # 使用client...
        pass
    '''

async def discover_tools():
    """
    发现服务器提供所有工具,并打印工具的总体信息、名称、描述、输入模式
    """
    client = MCPClient(["npx.cmd", "-y", "@modelcontextprotocol/server-filesystem", "."])

    async with client:
        #获取所有可用工具
        tools = await client.list_tools()
        '''
        函数调用返回：
        return [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
            }
            for tool in tools
        ]
        '''
        print(f"\n服务器提供{len(tools)}个工具:")
        for tool in tools:
            print(f"\n工具总体信息:{tool}\n")
            name = tool.get("name",None)
            description = tool.get("description",None)
            if name and description:
                print(f"\n 工具名称为:{name}")
                print(f"\n 工具描述为:{description}")
            if 'input_schema' in tool:
                schema = tool['input_schema']
                print(f"\n 工具输入模式为:")
                for key,value in schema.items():
                    print(f"  {key}: {value}")
            
            print('-'*40)

        print()

'''
服务器提供14个工具:

工具总体信息:{'name': 'read_file', 
'description': 'Read the complete contents of a file as text. DEPRECATED: Use read_text_file instead.', 
'input_schema': {'$schema': 'http://json-schema.org/draft-07/schema#', 
                 'type': 'object', 
                 'properties': {'path': {'type': 'string'}, 
                                'tail': {'description': 'If provided, returns only the last N lines of the file', 'type': 'number'}, 
                                'head': {'description': 'If provided, returns only the first N lines of the file', 'type': 'number'}
                               }, 
                 'required': ['path']}
                }


工具名称为:read_file

 工具描述为:Read the complete contents of a file as text. DEPRECATED: Use read_text_file instead.

 工具输入模式为:
  $schema: http://json-schema.org/draft-07/schema#
  type: object
  properties: {'path': {'type': 'string'}, 'tail': {'description': 'If provided, returns only the last N lines of the file', 'type': 'number'}, 'head': {'description': 'If provided, returns only the first N lines of the file', 'type': 'number'}}
  required: ['path']
'''


async def use_tool():
    """
    使用工具
    """
    # 将工作目录设置为 Communication_protocol 目录（向上两级）
    # 这样 MCP 服务器就可以访问该目录下的所有文件了
    client = MCPClient(["npx.cmd", "-y", "@modelcontextprotocol/server-filesystem", "../.."])
    '''
    📝 使用 Stdio 传输 (命令): npx.cmd -y @modelcontextprotocol/server-filesystem ../..
    🔗 连接到 MCP 服务器...
    ✅ 连接成功！
    可用工具: ['read_file', 'read_text_file', 'read_media_file', 'read_multiple_files', 'write_file', 
        'edit_file', 'create_directory', 'list_directory', 'list_directory_with_sizes', 'directory_tree', 'move_file', 
        'search_files', 'get_file_info', 'list_allowed_directories']
    '''
    async with client:
        # 先列出目录，确认实际的工作目录
        result = await client.call_tool("list_directory", {"path": "."})
        print(f"\n当前工作目录内容:\n{result}")
        
        # 调用读取文件函数 - 现在可以直接访问 intro.md
        result = await client.call_tool("read_file", {"path": "intro.md"})
        print(f"\n读取文件结果（前100个字符）:\n{str(result)[:100]}...")

        # 写入文件 - 直接写入到当前工作目录，避免路径问题
        result = await client.call_tool("write_file", {
            "path": "test_output.txt",
            "content": "Hello from MCP!",
        })
        print(f"\n写入文件结果:\n{result}")


'''

当然，也可以列出所有资源:
# 列出可用资源
resources = client.list_resources()
print(f"可用资源：{[r['uri'] for r in resources]}")

# 读取资源
resource_content = client.read_resource("file:///path/to/resource")
print(f"资源内容：{resource_content}")

同时也可以提供预定义的模板：
# 列出可用提示
prompts = client.list_prompts()
print(f"可用提示：{[p['name'] for p in prompts]}")

# 获取提示内容
prompt = client.get_prompt("code_review", {"language": "python"})
print(f"提示内容：{prompt}")


'''


# 运行异步函数
#asyncio.run()

