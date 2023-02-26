"""
Telegram бот для конвертации голосового/аудио сообщения в текст и
создания аудио из текста.
"""
import logging
import os
import openai
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_file import InputFile
from dotenv import load_dotenv

from stt import STT
from tts import TTS


UserContext = [['',' ']] 

load_dotenv()
print("Введите ключ Telegram")
TELEGRAM_TOKEN = str("5835481984:AAG9sHOQaO4mgl0WEu-I2uqZ7Rg8bs0kLOs")
print("Введите ключ OpenAI: ")
openai.api_key = "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"

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота
tts = TTS()
stt = STT()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)
def ChatGPT(Message, maxTokens = 650):
    theanswer = openai.Completion.create(
                 model="text-davinci-003",
                 prompt= Message,
                 temperature=0.5,
                 max_tokens=maxTokens,
                 top_p=1.0,
                 frequency_penalty=0.0,
                 presence_penalty=1.0,
                 )
    return theanswer['choices'][0]['text']


# Хэндлер на команду /start , /help
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Я голосовой ассистент на базе ChatGPT! Буду рада пообщаться. Я могу не только отвечать на текстовые сообщения, но и общаться с помощью голосовых сообщений! Попробуйте!"
    )

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def cmd_text(message: types.Message):
    global UserContext
    FoundUser = False
    ListId = 0
    user_name = message.from_user.first_name
    user_id = message.from_user.id 
    for i in range(len(UserContext)):
                            if str(user_id) == UserContext[i][0]:
                                UserContext[i][1] += str(" [" + user_name + "]" + ': ' + message.text + " [ChatGPT]: ")
                                ListId = i
                                FoundUser = True
                                while len(UserContext[i][1]) > 1850:
                                    temptext = UserContext[i][1]
                                    for i2 in range(len(temptext)):
                                            if temptext[i2] == '[':
                                                UserContext[i][1] = temptext[(i2 + 1):]
                                                break 
                                break
    if FoundUser == False:
                          ListId = len(UserContext)
                          UserContext.insert(len(UserContext),[str(user_id), str(" [" + user_name + "]" + ': ' + message.text + " [ChatGPT]: ")])
    Answer = ChatGPT(UserContext[ListId][1])
    UserContext[ListId][1] += Answer
    await message.reply(Answer)
    print(UserContext[ListId][1])


@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
    ]
)
async def voice_message_handler(message: types.Message):


  try:
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)

    text = stt.audio_to_text(file_on_disk)
    if not text:
        text = "Формат документа не поддерживается"

    global UserContext
    FoundUser = False
    ListId = 0
    user_name = message.from_user.first_name
    user_id = message.from_user.id 
    for i in range(len(UserContext)):
                            if str(user_id) == UserContext[i][0]:
                                UserContext[i][1] += str(" [" + user_name + "]" + ': ' + text + " [ChatGPT]: ")
                                ListId = i
                                FoundUser = True
                                while len(UserContext[i][1]) > 1850:
                                    temptext = UserContext[i][1]
                                    for i2 in range(len(temptext)):
                                            if temptext[i2] == '[':
                                                UserContext[i][1] = temptext[(i2 + 1):]
                                                break 
                                break
    if FoundUser == False:
                          ListId = len(UserContext)
                          UserContext.insert(len(UserContext),[str(user_id), str(" [" + user_name + "]" + ': ' + text + " [ChatGPT]: ")])


    Answer = ChatGPT(UserContext[ListId][1])
    UserContext[ListId][1] += Answer
    out_filename = tts.text_to_ogg(Answer)
    print(UserContext[ListId][1])
    # Отправка голосового сообщения
    path = Path("", out_filename)
    voice = InputFile(path)
    await bot.send_voice(message.from_user.id, voice,
                         caption="")

    # Удаление временного файла
    os.remove(out_filename)

    os.remove(file_on_disk)
  except Exception as ex:
   print("Произошла ошибка! " + str(ex))


if __name__ == "__main__":
    # Запуск бота
    print("Запуск бота")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
