# ChatGPTBotTelegram
Это бот на ChatGPT для телеграма.

Бот может отвечать как текстовыми, так и голосовыми. Чтобы бот ответил голосом, нужно записать ему гс с вопросом.

**Как запустить бота?**

Бот работает прекрасно на Python 3.10, так что советую использовать именно эту версию!

Клонируйте мой репозиторий 
```
git clone https://github.com/Wodjess/ChatGPTBotTelegram
```
Так же вам понадобятся эти библиотеки, установить их можно этими командами:
```
cd ChatGPTBotTelegram
cd Bot
pip install -r requirements.txt
```
Теперь скачайте архив и распакуйте его по адресу models/vosk
```
https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
```
Переменуйте папку vosk-model-small-ru-0.22 в model

Затем, установите FFMPEG и поместите его по адресу ChatGPTBotTelegram/Bot

Найти FFMPEG для Windows можно тут:
```
https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
```
Для Ubuntu:
```
sudo apt install ffmpeg
```

Отлично! Вы все установили! Теперь просто запустите бота
```
python Bot.py
```

Так же TTS и STT были взяты [отсюда](https://github.com/tochilkinva/tg_bot_stt_tts)