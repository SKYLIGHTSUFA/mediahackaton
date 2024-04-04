import speech_recognition as sr
import pyttsx3
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path).cuda()

# Инициализация объектов распознавания речи и синтеза речи
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Функция для распознавания речи
def recognize_speech():
    with sr.Microphone() as source:
        print("Говорите что-нибудь...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

        try:
            # Распознавание речи с помощью Google Web Speech API
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            print("Вы сказали:", text)
            return text
        except sr.UnknownValueError:
            print("Извините, не удалось распознать речь")
            return ""
        except sr.RequestError as e:
            print("Ошибка при запросе к Google Web Speech API: {0}".format(e))
            return ""


# Функция для синтеза речи
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Основной цикл программы
while True:
    # Распознавание речи
    user_input = recognize_speech()
    input_ids = tokenizer.encode(user_input, return_tensors="pt").cuda()
    out = model.generate(input_ids.cuda(), max_length=100)
    generated_text = list(map(tokenizer.decode, out))[0]
    print("gen_text = ", generated_text)
    answer = list(map(tokenizer.decode, out))[0].split("\n")
    try:
        speak(generated_text)
    except:
        speak("Простите, я не поняла ваш запрос, повторите пожалуйста")