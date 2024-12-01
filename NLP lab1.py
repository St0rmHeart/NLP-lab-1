import nltk
import pymorphy3
from nltk.tokenize import word_tokenize, sent_tokenize

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Функция для получения леммы и морфологических характеристик
def get_word_info(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form, parsed_word.tag

# Функция для проверки совпадений по родам, числам и падежам
def check_gender_number_case(tag1, tag2):
    return tag1.gender == tag2.gender and tag1.number == tag2.number and tag1.case == tag2.case

# Основная функция
def find_noun_adjective_pairs(text):
    # Список для хранения совпавших пар
    matching_pairs = []
    
    # Токенизация текста на предложения
    sentences = sent_tokenize(text)
    
    # Проходим по каждому предложению
    for sentence in sentences:
        # Токенизация предложения на слова
        words = word_tokenize(sentence)
        
        # Пропускаем слишком короткие предложения
        if len(words) < 2:
            continue
        
        # Для каждой пары соседних слов
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            
            # Получаем леммы и грамматические характеристики
            lemma1, tag1 = get_word_info(word1)
            lemma2, tag2 = get_word_info(word2)
            
            # Вывод отладочной информации
            print(f"Сравниваем пару: {word1} ({lemma1}, {tag1}) - {word2} ({lemma2}, {tag2})")
            
            # Проверяем, являются ли оба слова существительными или прилагательными
            if ('NOUN' in tag1 or 'ADJF' in tag1) and ('NOUN' in tag2 or 'ADJF' in tag2):
                # Проверяем совпадение по роду, числу и падежу
                if check_gender_number_case(tag1, tag2):
                    print(f"Пара совпадает: {lemma1} {lemma2}")
                    # Добавляем совпавшую пару в список
                    matching_pairs.append((lemma1, lemma2))
                else:
                    print(f"Пара НЕ совпадает по роду, числу и падежу: {lemma1} {lemma2}")
    
    # Выводим все совпавшие пары
    if matching_pairs:
        print("\nСовпавшие пары (по родам, числам и падежам):")
        for pair in matching_pairs:
            print(f"{pair[0]} {pair[1]}")
    else:
        print("\nСовпавших пар не найдено.")

# Пример текста
text = "В мире существует множество университетов, каждый из которых предлагает уникальные программы обучения. Многие из них имеют богатую историю и традиции. Например, Московский государственный университет, основанный в 1755 году, является одним из самых престижных учебных заведений в России. Он привлекает студентов со всего мира. Университеты часто становятся центрами научных исследований, способствующими развитию новых технологий и идей. Программы для иностранных студентов, обмены и стипендии делают образование доступным для всех. К тому же, в университете студенты могут не только получать знания, но и участвовать в различных культурных и спортивных мероприятиях"

# Вызов функции
find_noun_adjective_pairs(text)