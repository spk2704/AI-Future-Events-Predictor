from ollama import chat, web_search, web_fetch


content = input("What future event do you want to know: ")
messages = [{"role": "user", "content": content}]

available_tools = {'web_search': web_search, 'web_fetch': web_fetch}


response = chat(
    model="qwen3.5",
    messages=messages,
    tools=[available_tools],
    think=False
)


messages.append(response.message)

if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        function_to_call = available_tools.get(tool_call.function.name)
        args = tool_call.function.arguments
        result = function_to_call(**args)
        print('Result: ', str(result)[:200] + '...')
        messages.append({'role': 'tool', 'content': str(result)[:2000 * 4], 'tool_name': tool_call.function.name})


final_response = chat(
    model="qwen3.5",
    messages=messages
)

print(final_response.message.content)