import torch
from transformers import AutoModelForCausalLM,AutoTokenizer 


'''
AutoModelForCausalLM and AutoTokenizer are classes from the Hugging Face Transformers library 
used for loading pre-trained language models and their corresponding tokenizers.
'''

#设置设备
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"using device:{device}")

#指定model id
model_id = "Qwen/Qwen1.5-0.5B-Chat"

#加载对应分词器
tokenizer = AutoTokenizer.from_pretrained(model_id)

#加载模型，并将其移动到对应设备
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

print("模型和分词器加载完成。")

#准备对话输入
messages = [
    {'role':'system','content':'you are a helpful assistant.'},
    {'role':'user','content':'你好，请介绍一下中国电信.'},
]

#使用model对应tokenizer进行编码
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

#编码输入文本
model_inputs = tokenizer([text],return_tensors='pt').to(device) #将文本转为张量，并移动到对应设备

print("编码后的文本:")
print(model_inputs)

#使用模型生成回答
#定义max_new_tokens，限制生成的最大新tokens数
generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512,
)

#将生成新的Token ID截取掉输入部分
#这样只解码模型新生成的部分
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids) #输入输出绑定
]

response = tokenizer.batch_decode(generated_ids,skip_special_tokens=True)[0] #解码生成的Token ID为文本
print("模型回答:")
print(response)

