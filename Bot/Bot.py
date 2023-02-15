from ast import Return
from aiogram import Bot, Dispatcher, executor, types
import openai
from datetime import datetime, timedelta
from urllib.request import urlopen
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
from time import sleep
import os
print("Это бот на ChatGPT с доп. функциями для учебы.\n\nЭтот бот умеет отвечать на ваши вопросы в ЛС и 1 беседе в телеграме, так же поддерживаются комманды:\nДобавить дз (дз)\nКакое дз\nУдали дз (дз)\nУдали все дз!\n\n\nДля того, чтобы бот работал в беседе с другими людьми нужно:\n1) Добавить его и дать права Администратора\n2) Обращатьcя к боту так: (Имя бота, текст), например: Бот, что такое синус?\nВ личных сообщениях бота писать имя бота не обязательно!\n\nПервичные настройки:\n\n")
print("1) Напишите имя бота, на которое бот будет реагировать в других беседах: ")
botname = input()
botname = botname.lower()
print("\n2) Бот может работать только в личных сообщениях и 1 беседе, напишите ID этой беседы \n\nЕсли не знаете ID беседы, то просто оставьте строку пустой! Бот каждый раз пишет в консоль id чата из которого ему пишут! Вы сможете узнать ID позже!\n\nID:")
chatid = input()
print("\n3) Введите ключ Telegram, сделанный с помощью BotFather: ")
API_TOKEN = input()
IWorkNow = False
ListId = 0
HomeWork = ""
LearnOthers = 0
HomeWorkNumber = 0
print("\n4) Введите ключ OpenAI: ")
openai.api_key = input()
print("\n\nОтлично! Настройка завершенна! Теперь " + botname + " работает. Попробуйте написать ему что-то и вы увидете ответ в консоли и в тг!")
now = datetime.now()
UserContext = [['',' ']] 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
tosendtemp = "temp"
zamanal = 0
FirstKnow = False
FirstLesson = ""
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

def Lessons(DoSomething = False):
            global FirstLesson
            page = urlopen("http://asu.sf-misis.ru/rasp/545")
            soup = BeautifulSoup(page, features="html.parser")
            raspTB = soup.findAll(attrs={"class":"raspTB"})
            Lessons = [["","", ""]]
            YaUctal = 0
            IsAlreadyIn = False
            for i in range(len(raspTB)):
                    if((str(raspTB[i]).split('>')[1]).removesuffix('</td')) ==  "№":
                        if DoSomething == True:
                            for letsKmowHowMany in range(len(raspTB)):
                                if IsAlreadyIn == False:
                                    FirstLesson = ((str(raspTB[i + (letsKmowHowMany * 4) + 4]).split('>')[1]).removesuffix('</td'))
                                    IsAlreadyIn = True
                                if(((str(raspTB[i + (letsKmowHowMany * 4) + 4]).split('>')[1]).removesuffix('</td')) == "№"):
                                    YaUctal = letsKmowHowMany
                                    break
                            for Les in range(YaUctal):
                                Lessons.insert(len(Lessons),[(str(raspTB[i + (Les * 4) + 5]).split('>')[1]).removesuffix('</td'),(str(raspTB[i + (Les * 4) + 6]).split('>')[1]).removesuffix('</td'), (str(raspTB[i + (Les * 4) + 7]).split('>')[1]).removesuffix('</td')])
                            break

                    if((str(raspTB[i]).split('>')[1]).removesuffix('</td') ==  "№"):
                        DoSomething = True
                        
            return Lessons
def ForComfortChatting(messagetext = ""):
    global Lessons
    global AllPrompt
    global ChatGPT
    global ListId
    global now
    global HomeWork
    global HomeWorkNumber
    tommorow = now + timedelta(days = 1)
    if messagetext[:17] == "какие пары завтра" or messagetext[:20] == "какие пары на завтра":
             
             Lessons1 = Lessons()
             if(len(Lessons1) < 2):
                 response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Напиши оригинально, что завтра не будет никаких пар! Не больше 1 предложения! Напиши так, чтобы люди обрадовались от твоих слов! Напиши так, чтобы люди тебе поверили!",
                    temperature=0.1,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.2,
                    presence_penalty=0.0,
                    )
                 return (response['choices'][0]['text'])
             else:
                 tosend = ""
                 for i in range(len(Lessons1) - 1):
                     tosend += str(i + int(FirstLesson)) + " " + Lessons1[i + 1][0] + ", " + Lessons1[i + 1][1] + " в " + Lessons1[i + 1][2] + "\n"
                 return "Вот пары на " + str(tommorow.day) + "." + str(tommorow.month) + "." + str(tommorow.year) + ":\n\n" + tosend
    else:
         if  messagetext[:18] == "какие пары сегодня" or messagetext[:21] == "какие пары на сегодня":
             Lessons1 = Lessons(True)
             if(len(Lessons1) < 2):
                 response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Напиши оригинально, что сегодня не будет никаких пар! Не больше 1 предложения! Напиши так, чтобы люди обрадовались от твоих слов! Напиши так, чтобы люди тебе поверили!",
                    temperature=0.1,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.2,
                    presence_penalty=0.0,
                    )
                 return response['choices'][0]['text'] 
             else:
                 tosend = ""
                 for i in range(len(Lessons1) - 1):
                     tosend += str(i + int(FirstLesson)) + " " + Lessons1[i + 1][0] + ", " + Lessons1[i + 1][1] + " в " + Lessons1[i + 1][2] + "\n"
                 return "Вот пары на " + str(now.day) + "." + str(now.month) + "." + str(now.year) + ":\n\n" + tosend
         else:
             if messagetext[:10] == "какие пары":
                 if(now.hour > 14):
                     Lessons1 = Lessons()
                     if(len(Lessons1) < 2):
                         response = openai.Completion.create(
                         model="text-davinci-003",
                         prompt="Напиши оригинально, что завтра не будет никаких пар! Не больше 1 предложения! Напиши так, чтобы люди обрадовались от твоих слов! Напиши так, чтобы люди тебе поверили!",
                         temperature=0.1,
                         max_tokens=1000,
                         top_p=1.0,
                         frequency_penalty=0.2,
                         presence_penalty=0.0,
                         )
                         return response['choices'][0]['text']
                     else:
                      tosend = ""
                      for i in range(len(Lessons1) - 1):
                         tosend += str(i + int(FirstLesson)) + " " + Lessons1[i + 1][0] + ", " + Lessons1[i + 1][1] + " в " + Lessons1[i + 1][2] + "\n"
                      return "Вот пары на " + str(tommorow.day) + "." + str(tommorow.month) + "." + str(tommorow.year) + ":\n\n" + tosend
                 else:
                     Lessons1 = Lessons(True)
                     if(len(Lessons1) < 2):
                         response = openai.Completion.create(
                         model="text-davinci-003",
                         prompt="Напиши оригинально, что завтра не будет никаких пар! Не больше 1 предложения! Напиши так, чтобы люди обрадовались от твоих слов! Напиши так, чтобы люди тебе поверили!",
                         temperature=0.1,
                         max_tokens=1000,
                         top_p=1.0,
                         frequency_penalty=0.2,
                         presence_penalty=0.0,
                         )
                         return response['choices'][0]['text']
                     else:
                      tosend = ""
                      for i in range(len(Lessons1) - 1):
                         tosend += str(i + int(FirstLesson)) + " " + Lessons1[i + 1][0] + ", " + Lessons1[i + 1][1] + " в " + Lessons1[i + 1][2] + "\n"
                      return "Вот пары на " + str(now.day) + "." + str(now.month) + "." + str(now.year) + ":\n\n" + tosend
    if messagetext[:11] == "дз добавить" or messagetext[:9] == "дз добавь" or messagetext[:9] == "добавь дз" or messagetext[:11] == "добавить дз":
             HomeWorkNumber += 1
             HomeWork += messagetext[11:] + " (Добавлено " + str(now.day) + "." + str(now.month) + ")\n"
             return "ДЗ было добавлено! Чтобы узнать дз, напишите: какое дз\nчтобы удалить: удали дз по (предмет)"
    else:
         if messagetext[:8] == "какое дз" or messagetext[:8] == "дз какое":
                 return "ДЗ:\n\n" + HomeWork
         else:
             if messagetext[:8] == "удали дз" or  messagetext[:10] == "дз удалить" or  messagetext[:8] == "дз удали" or  messagetext[:10] == "удалить дз":
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Удали из текста все что касается" + messagetext[12:] + "\n" + HomeWork,
                    temperature=0.1,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    )
                    HomeWork = response['choices'][0]['text']
                    HomeWork.replace("\n"," ")
                    return "Завершила удаление дз! Чтобы узнать дз, напишите: какое дз? "
             else:
                 if messagetext[:12] == "удали все дз":
                     tempwork = HomeWork
                     HomeWork = ""
                     return "Удалила все дз! Вот оно еще раз на всякий случай:\n\n" + tempwork
                     
@dp.message_handler()
async def echo(message: types.Message):
   try:
         m = message.text
         m = m.lower()
         global FirstLesson
         global botname
         global chatid
         print("\n Ко мне обратились из чата: ID " + str(message.chat.id) + "\n")
         global Lessons
         global AllPrompt
         global ChatGPT
         global ListId
         if m[:len(botname)] == botname:
             mt = m[len(botname) + 1:]
             mt = mt.lower()
             if mt == "какое дз" or mt[:11] == "добавить дз" or mt[:9] == "добавь дз" or mt[:8] == "удали дз" or mt == "удали все дз" or mt[:11] == "дз добавить" or mt[:10] == "дз удалить" or mt[:10] == "какие пары" or mt[:2] == "дз":
                await message.answer(ForComfortChatting(mt))
                return

         mt = m
         mt = mt.lower()
         if mt == "какое дз" or mt[:11] == "добавить дз" or mt[:9] == "добавь дз" or mt[:8] == "удали дз" or mt == "удали все дз" or mt[:11] == "дз добавить" or mt[:10] == "дз удалить" or mt[:2] == "дз":
              await message.answer(ForComfortChatting(mt))
              return
         else:
             if m[:len(botname)] == botname or message.chat.type == 'private':
                 if str(message.chat.id) == chatid or message.chat.type == 'private':
                    try:
                         IsUserIsPrivate = False
                         if m[:len(botname)] != botname:
                                IsUserIsPrivate = True
                         global UserContext
                         global IWorkNow
                         user_name = message.from_user.first_name
                         user_id = message.from_user.id 
                         FoundUser = False
                         for i in range(len(UserContext)):
                            if str(user_id) == UserContext[i][0]:
                                if IsUserIsPrivate == False:
                                    UserContext[i][1] += str(" [" + user_name + "]" + ': ' + m[len(botname) + 1:] + " [ChatGPT]: ")
                                else:
                                    UserContext[i][1] += str(" [" + user_name + "]" + ': ' + m + " [ChatGPT]: ")
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
                             if IsUserIsPrivate == False:
                                UserContext.insert(len(UserContext),[str(user_id), str(" [" + user_name + "]" + ': ' + m[len(botname) + 1:] + " [ChatGPT]: ")])
                             else:
                                UserContext.insert(len(UserContext),[str(user_id), str(" [" + user_name + "]" + ': ' + m + " [ChatGPT]: ")])  
                         if m[len(botname) + 1:] == "забудь контекст" or m[len(botname) + 1:] == "забудь все, что я написал!":
                             UserContext[ListId][1] = str(" [" + user_name + "]" + ': ' + "Привет!" + " [ChatGPT]: ")
                             await message.answer("Контекст был удален!")

                         if IWorkNow == False:
                             await message.answer(str(user_name + ", Я снова работаю, пишу ответ..."))
                             IWorkNow = True
                         question = UserContext[ListId][1]
                         question = ChatGPT(question, 750)
                         UserContext[ListId][1] += question
                         print(UserContext[ListId][1])
                         await message.answer(question)
                    except Exception as e:
                         await message.answer("Что-то пошло не так :/ \n\n Ошибка: \n" + "{0}".format(str(e.args[0])).encode("utf-8") + "\n Попробуйте написать мне еще раз")
             else:
                 if m == "info":
                     await message.answer("Я нейросеть на базе ChatGPT, меня можно использовать как дневник и шпаргалку:\n\nЧтобы задать мне вопрос, напишите: Аннушка (Ваш вопрос)\n\n Чтобы записать в меня домашку, напишите: дз добавить (дз)\n Например: дз добавить Русский язык - задание номер 18\n\n Чтобы посмотреть дз, напишите: какое дз\nЧтобы удалить дз, напишите: удали дз (какое дз).\n Чтобы удалить все дз, напишите: удали все дз.\n\nПары:\n\n Чтобы узнать какие пары, напишите: Какие пары.\n(Вы можете только узнать пары за сегодня и завтра (Какие пары сегодня), (Какие пары завтра)\n\n так же вы можете просто написать: Какие пары, ответ будет зависить от времени когда вы это пишите!)")
   except:
       await message.answer("Кажется сервер перегружен :/ \nПопробуйте написать мне еще раз")
                 

if __name__ == '__main__':
  executor.start_polling(dp)
  