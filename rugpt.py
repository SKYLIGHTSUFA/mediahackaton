

tok = GPT2Tokenizer.from_pretrained("models/weights") #загрузка дообученного токенизатора

model = GPT2LMHeadModel.from_pretrained("models/essays") #загрузка дообученной модели

model.cuda() #перевод модели на GPU, можно обойтись и без этого, тогда генерация будет происходить медленнее