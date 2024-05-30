import openai
from elevenlabs import play
from elevenlabs.client import ElevenLabs

openai.api_key = 'PUT_YOUR_API_KEY_HERE'
elevenlabs = ElevenLabs(
  api_key="PUT_YOUR_API_KEY_HERE" # Defaults to ELEVEN_API_KEY
)


def interact_with_assistant():
    message_history = [{
        "role": "system",
        "content": "You are an AI assistant tasked with having a friendly conversation with a user. Your goal is to engage the user, ask relevant questions, and keep the conversation flowing in a natural way while being helpful and answering the user's questions to the best of your knowledge."
    }]

    while True:
        user_input = input("Ваше сообщение: ")

        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "clear":
            # Очищаем историю, оставляем только системное сообщение
            message_history = [{
                "role": "system",
                "content": "You are an AI assistant tasked with having a friendly conversation with a user. Your goal is to engage the user, ask relevant questions, and keep the conversation flowing in a natural way while being helpful and answering the user's questions to the best of your knowledge."
            }]
            print("\033[92m" + "История сообщений очищена." + "\033[0m")
            continue

        # Добавляем сообщение пользователя в историю
        message_history.append({
            "role": "user",
            "content": user_input
        })

        # Создаём запрос к модели GPT-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=message_history
        )

        # Получаем ответ ассистента и добавляем его в историю
        assistant_reply = response['choices'][0]['message']['content']
        print("\033[93m" + "Ассистент: " + assistant_reply + "\033[0m")

        message_history.append({
            "role": "assistant",
            "content": assistant_reply
        })

        # Если сообщений стало больше 20, удаляем самые старые
        if len(message_history) > 20:
            message_history = message_history[-20:]

        # Генерация аудио из текста и воспроизведение
        audio_stream = elevenlabs.generate(text=assistant_reply,
                                           voice="Rachel",
                                           model="eleven_multilingual_v2",
                                           stream=True)
        play(audio_stream)

# Запускаем диалог с ассистентом
interact_with_assistant()