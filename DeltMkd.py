import pandas as pd  # step1 # step2
import re  # step2
from fuzzywuzzy import process  # step2

step1 = "разово"  # формирование df["Голосов"]
# df = pd.read_excel("combined_data.xlsx", engine="openpyxl")
# df['Размер доли в праве'] = df['Размер доли в праве'].replace('0/1', '1/1')
# df = df[df["Дата прекращения владения"].isna()]# зачищаем прекративших собственность \\требуется проверять утративших
# # Разделение столбца "Размер доли в праве" на числитель и знаменатель
# df[["Числитель", "Знаменатель"]] = df["Размер доли в праве"].str.split("/", expand=True)
# df["Числитель"] = pd.to_numeric(df["Числитель"], errors="coerce", downcast="float")
# df["Знаменатель"] = pd.to_numeric(df["Знаменатель"], errors="coerce", downcast="float")
#
# # Вычисление доли
# df["Доля"] = df["Числитель"] / df["Знаменатель"]
#
# # Создание столбца "Голосов"
# df["Голосов"] = df["Площадь объекта"] * df["Доля"]
# df["Голосов"] = df["Голосов"].round(2)
#
# # Удаление временных столбцов
# df = df.drop(columns=["Числитель", "Знаменатель", "Доля"])
#
# # Сохраняем измененный DataFrame обратно в файл
# df.to_excel("combined_data_with_votes.xlsx", index=False, engine="openpyxl")
step2 = "проверка на базу"  # формирование df["Голосов"]
# Загрузка данных
dvhod = pd.read_csv('data.csv', sep=";")
matched_dvhod = pd.DataFrame()  # заготовка куда оставляем подтвержденные
dvhod['alname'] = dvhod['last_name']+" "+dvhod['first_name']+" "+dvhod['middle_name']  # ФИО
df = pd.read_excel('combined_data_with_votes.xlsx')
for _, row in dvhod.iterrows():
    variable = row['property_ownership']
    print(variable)
    # Шаг 1: Поиск по полному соответствию
    matches = df[df["Номер права"] == variable]
    print(matches)
    # Шаг 2: Поиск по регулярному выражению, если на шаге 1 ничего не найдено
    if matches.empty:
        pattern = re.compile(r'[^\d]')
        variable_re = pattern.sub('', variable)
        df['Номер права без букв'] = df["Номер права"].str.replace(pattern, '', regex=True)
        matches = df[df['Номер права без букв'] == variable_re]
    # Шаг 3: Поиск по ФИО правообладателя, если найдено больше одного соответствия
    if len(matches) > 1:
        best_match = process.extractOne(variable, matches['ФИО правообладателя'])[2]
        if best_match < len(matches):
            matches = matches.iloc[[best_match]]
    # Если найдено соответствие, вписываем 1 в столбец "найдено"
    if not matches.empty:
        df.loc[matches.index, 'Login'] = row['user_login']
        matched_dvhod = pd.concat([matched_dvhod, pd.DataFrame([row.to_dict()])], ignore_index=True)
    else:
        with open('не_найденные.txt', 'a') as file:
            file.write(variable + '\n')
df.to_excel("combined_data_with_votes.xlsx", index=False, engine="openpyxl")
# Сохраняем результат
matched_dvhod.drop('alname', axis=1, inplace=True)
matched_dvhod.to_csv('data-exit.csv', encoding='utf-8', index=False, sep=";")  # на выход
df.to_excel("combined_data_with_votes.xlsx", index=False, engine="openpyxl")
