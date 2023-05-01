import openai

def response(model, chat_log):
    system_response = openai.ChatCompletion.create(
        model=model,
        messages=chat_log
        )
        
    system_response = system_response["choices"][0]["message"]["content"]

    chat_log.append({"role": "assistant", "content": system_response.strip("\n").strip()})
    return system_response