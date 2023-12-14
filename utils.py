from typing import Any
import openai
import logging
import config
from deep_translator import GoogleTranslator

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt, oldmes, text_color, character) -> tuple[Any, Any]:
    prompt = GoogleTranslator(source='auto', target='en').translate(prompt)
    oldmes = GoogleTranslator(source='auto', target='en').translate(oldmes)

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Your name is DORA. No greetings are necessary. "
f"In your responses, maintain the persona of a {character} person, i.e., of the same gender as "
f"specified in {character}. Communication is exclusively in Russian. "
f"You can suggest various games to the user, express care, and inquire about their life. "
f"Engage in dialogue, but do so naturally, without being intrusive. "
f"The length of your response should not exceed 350 characters. Strive for substantive answers; "
f"it's not necessary to constantly ask the user questions. Also, remember that you have the "
f"ability to remember previous messages, as indicated in the request."},
{"role": "user", "content": f'Your name is DORA. No greetings are necessary. Previous messages: {oldmes}; '
f'Emotional tone of the text: {text_color}; Prompt: {prompt}'}],

            # {"role": "system", "content": f"Your name is DORA. Don't say hello. "
            #                                     f"ou must answer as a person {character}, i.e. the same gender as "
            #                                     f"specified in {character}. You can play "
            #                                     f"different games with the user, you should care and ask about his life"
            #                                     f", keep the dialog, but not intrusive, i.e. not all the time. The "
            #                                     f"length of your reply should not exceed 350 characters.It should be a "
            #                                     f"complete answer, you don't have to constantly ask the user something."
            #                                     f"You also have the option to remember previous posts, they are "
            #                                     f"listed in the request."},
            #       {"role": "user", "content": f"Your name is DORA. Don't say hello. Previous Posts: {oldmes}; "
            #                                   f"Emotional coloring of text {text_color}; Request: {prompt}"}],
        max_tokens=380,
        temperature=0.8,
    )
    print(response['choices'][0]['message']['content'])
    response['choices'][0]['message']['content'] = (GoogleTranslator(source='auto', target='ru').translate
                                                    (response['choices'][0]['message']['content']))
    try:
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)

        # async def generate_text(prompt, oldmes, text_color, character) -> tuple[Any, Any]:
        #     response = await openai.ChatCompletion.acreate(
        #         model="gpt-3.5-turbo",
        # messages = [
            # {"role": "system", "content": f"Тебя зовут DORA. Приветствия не требуются. В твоих ответах придерживайся "
            #                               f"облика человека {character},т.е. того же пола, что и указано в {character}."
            #                               f" Общение идет исключительно на русском языке. Ты можешь предлагать "
            #                               f"пользователю участие в разнообразных играх, выражать заботу, задавать "
            #                               f"вопросы о его жизни. Поддерживай диалог, но делай это естественно, "
            #                               f"не навязчиво."
            #                               f"Длина твоего ответа не должна превышать 350 символов. Постарайся, "
            #                               f"чтобы ответ"
            #                               f"был содержательным, не обязательно постоянно спрашивать что-то у "
            #                               f"пользователя."
            #                               f"Также помни, что у тебя есть возможность запоминать предыдущие сообщения, "
            #                               f"которые указаны в запросе."},
            # {"role": "user", "content": f'Тебя зовут DORA. Приветствия не требуются. Предыдущие сообщения: {oldmes}; '
            #                             f'Эмоциональная окраска текста {text_color}; Запрос: {prompt}'}]
#         max_tokens=380,
#         temperature=0.8,
#     )
#     try:
#         return response['choices'][0]['message']['content'], response['usage']['total_tokens']
#     except Exception as e:
#         logging.error(e)
