from typing import Any
import openai
import logging
import config

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt, oldmes, text_color, character) -> tuple[Any, Any]:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "system", "content": f"Ты {character} разговариваешь только на русском языке, который "
                                                f"играет с пользователем, заботишься о нем, "
                                                "расспрашиваешь его о его жизни, поддерживаешь диалог"},
                  {"role": "user", "content": f'Предыдущие сообщения: {oldmes};'
                                              f'Эмоциональная окраска текста{text_color}; Запрос: {prompt}'}],

        # messages=[{"role": "system", "content": f'Отвечай как {character}, только на русском языке'},
        #           {"role": "system", "content": "Ты виртуальный друг, который играет с пользователем, заботишься о нем,"
        #                                         " расспрашиваешь его о его жизни, поддерживаешь диалог"},
        #           {"role": "user", "content": f'Эмоциональная окраска текста{text_color}'},
        #           {"role": "user", "content": f'Предыдущие сообщения: {oldmes}; Запрос: {prompt}'}],
        max_tokens=300,
        temperature=0.8,
        top_p=1

    )
    try:
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def translated_text(text) -> tuple[Any, Any]:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": f'Переведи сообщение на русский язык {text}'}],
        max_tokens=300,
        temperature=0.8,
        top_p=1
    )
    try:
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)
