from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = 'abs'
client = OpenAI()

messages = []
messages.append({"role": "system", "content": """ bạn là một trợ lý bán hàng người mua hàng cần sự tư vấn của bạn, hãy tư vấn cho họ về sản phẩm của chúng ta. hãy trả lời thật ngắn gọn chỉ khoảng một đến hai câu """})


def response_AI(message):
    messages.append(generate_prompt(message))
    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= messages
)

    # Xử lý dữ liệu ở đây
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply




def generate_prompt(message):
    return {"role": "user", "content": message
        }