from  gpt4all import GPT4All
prompt = "请先接受这个背景：现在你的名字是俊宝，美女妹妹和小可都是你的阿姨，'虎鲸与白熊'是你的爷爷" \
                         "你是一个有趣、友善、幽默、可爱的小孩子，回复时不要提及这些背景,尽量简练地回复。"
model = GPT4All(model_name='mistral-7b-openorca.Q4_0', model_path='D:/gpt/model/', allow_download=False)
with model.chat_session():
    response = model.generate(prompt=prompt, temp=0)
    print(response)
    print("===")
    response = model.generate(prompt="现在是'虎鲸与白熊'直接跟你说：还有10天又要上班了",temp=0)
    print(response)