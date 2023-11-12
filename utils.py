from typing import Any
import openai
import logging
import config

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt, oldmes, text_color, character) -> tuple[Any, Any]:
    # response = await openai.ChatCompletion.acreate(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "system", "content": f"Ты {character} разговариваешь только на русском языке, который "
    #                                             f"играет с пользователем, заботишься о нем, "
    #                                             "расспрашиваешь его о его жизни, поддерживаешь диалог. Длина "
    #                                             "твоего ответа не должна превышать 300 символов. Это должен быть "
    #                                             "полноценный ответ. Также у тебя есть возможность помнить предыдущие "
    #                                             "сообщение, они указаны в запросе."},
    #               {"role": "user", "content": f'Предыдущие сообщения: {oldmes};'
    #                                           f'Эмоциональная окраска текста{text_color}; Запрос: {prompt}'}],
    #     max_tokens=300,
    #     temperature=0.8,
    # )
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Ты должен отвечать как человек {character}, т.е. такого же пола что "
                                                f"указано в {character} разговариваешь только на русском языке. Ты "
                                                f"можешь играть с пользователем в различные игры, должен заботиться и "
                                                f"расспрашивать о его жизни, поддерживаешь диалог, но не навязчиво, "
                                                f"т.е. не постоянно.  Длина твоего ответа не должна превышать 350 "
                                                f"символов. Это должен быть полноценный ответ, не обязательно "
                                                f"постоянно спрашивать что-то у пользователя. Также у тебя есть "
                                                f"возможность помнить предыдущие сообщения, они указаны в запросе. "},
                  {"role": "user", "content": f'Предыдущие сообщения: {oldmes};'
                                              f'Эмоциональная окраска текста {text_color}; Запрос: {prompt}'}],
        max_tokens=380,
        temperature=0.8,
    )
    try:
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def translated_text(text) -> tuple[Any, Any]:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": f'Переведи сообщение на русский язык {text}'}],
        temperature=0.8,
    )
    try:
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)
