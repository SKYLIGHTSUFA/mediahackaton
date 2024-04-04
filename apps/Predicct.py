import customtkinter as ctk
import os
import cv2
from PIL import Image
import speech_recognition as sr
import pyttsx3
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import threading
import time
class Predict(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name_or_path).cuda()
        self.count = 0
        self.flag = False
        # Инициализация объектов распознавания речи и синтеза речи
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.label = ctk.CTkLabel(self, text="МХ Яндекс x ЭМИТ | 2024", fg_color="blue", text_color="white")
        self.label.grid(row=0, column=0, sticky="ew", columnspan=2)
        self.button_get_dir = ctk.CTkButton(self, text="Начать общение", command=self.__start_talking)
        self.button_get_dir.grid(row=1, column=0, pady=10, sticky="ew", columnspan=2)


    def __open_file_dialog(self):
        root = ctk.CTk()
        root.withdraw()
        file_path = ctk.filedialog.askdirectory(title='Choose image dataset')
        if file_path != '':
            root.destroy()
            self.storage_name = file_path
            self.iterator = iter(os.listdir(self.storage_name))
            return file_path

    def __start_predict(self):
        if self.counter > 0:
            self.label.destroy()
        self.counter+=1
        filename = next(self.iterator)
        dicter3 = {}
        if filename.endswith("png") or filename.endswith("jpg"):
            print(filename)
            img = cv2.cvtColor(cv2.imread(os.path.join(self.storage_name, filename)), cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (1080, 720))
            if len([1,1]) < 1:
                print(f'len detection = {len([1,1])}')
            for detection in [1, 1]:
                pass
                    #image[0:128, 0:128] = cv2.resize(cv2.cvtColor(image_usa, cv2.COLOR_BGR2RGB), (128,128))
                    #image[0:128, 138:266] = cv2.resize(cv2.cvtColor(image_ussr, cv2.COLOR_BGR2RGB), (128,128))
                    #self.image = Image.fromarray(image)
                    #self.image_tk = ctk.CTkImage(self.image, size=(self.image.width, self.image.height))
                    #self.label = ctk.CTkLabel(self, image=self.image_tk, text=self.name_usa[result[0][0]], text_color="red")
                    #self.label.grid(row=3, column=0, pady=10, sticky="ew")

    def show_img(self):
        print("thread is starting")

        while True:
            cap = cv2.VideoCapture("../data/animation.gif.mp4")
            if self.flag:
                break
            while True:
                ret, frame = cap.read()
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                try:
                    frame = cv2.resize(frame, (1080, 720))
                    if not ret:
                        break
                    cv2.imshow("Mascot is talking ", frame)
                    cv2.waitKey(5)
                    if self.flag:
                        break
                except:
                    break


                #self.image = Image.fromarray(frame)
                #self.image_tk = ctk.CTkImage(self.image, size=(self.image.width, self.image.height))
                #self.label = ctk.CTkLabel(self, image=self.image_tk, text="", text_color="red")
                #self.label.grid(row=3 + self.count, column=1, pady=10, sticky="ew", rowspan=2)
    def __start_talking(self):

        self.button_get_dir.destroy()
        self.button_get_dir = ctk.CTkButton(self, text="Продолжить общение", command=self.__start_talking)
        self.button_get_dir.grid(row=1, column=0, pady=10, sticky="ew", columnspan=2)


        def speech_thread():
            def recognize_speech():
                with sr.Microphone() as source:
                    print("Говорите что-нибудь...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio_data = self.recognizer.listen(source)

                    try:
                        # Распознавание речи с помощью Google Web Speech API
                        text = self.recognizer.recognize_google(audio_data, language="ru-RU")
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
                self.engine.say(text)
                self.engine.runAndWait()

            # Распознавание речи
            user_input = recognize_speech()
            if "нужно" not in user_input:
                user_input = "Для того, чтобы приготовить " + user_input + " нужно"

            input_ids = self.tokenizer.encode(user_input, return_tensors="pt").cuda()
            out = self.model.generate(input_ids.cuda(), max_length=100)
            generated_text = list(map(self.tokenizer.decode, out))[0]
            print("gen_text = ", generated_text)
            answer = list(map(self.tokenizer.decode, out))[0].split("\n")
            self.thread.start()
            try:
                speak(generated_text)
                self.label_answer = ctk.CTkLabel(self, text=user_input, fg_color="green", text_color="white")
                self.label_answer.grid(row=3 + self.count, column=0, sticky="ew", columnspan=2)
                self.count += 1
                self.label_answer = ctk.CTkLabel(self, text=generated_text, fg_color="blue", text_color="white")
                self.label_answer.grid(row=3 + self.count, column=0, sticky="ew", columnspan=2)
                self.count += 2
            except:
                speak("Простите, я не поняла ваш запрос, повторите пожалуйста")
            finally:
                self.flag = True

        self.thread = threading.Thread(target=self.show_img)
        self.thread1 = threading.Thread(target=speech_thread)

        self.thread1.start()








