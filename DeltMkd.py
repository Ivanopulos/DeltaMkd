import pandas as pd


df = pd.read_excel("combined_data.xlsx", engine="openpyxl")

step = "разово"  # df["Голосов"]
df = df[df["Дата прекращения владения"].isna()]# зачищаем прекративших собственность \\требуется проверять утративших
# Разделение столбца "Размер доли в праве" на числитель и знаменатель
# df["Числитель"], df["Знаменатель"] = df["Размер доли в праве"].str.split("/").str
df[["Числитель", "Знаменатель"]] = df["Размер доли в праве"].str.split("/", expand=True)
df["Числитель"] = pd.to_numeric(df["Числитель"], errors="coerce", downcast="float")
df["Знаменатель"] = pd.to_numeric(df["Знаменатель"], errors="coerce", downcast="float")

# Вычисление доли
df["Доля"] = df["Числитель"] / df["Знаменатель"]

# Создание столбца "Голосов"
df["Голосов"] = df["Площадь объекта"] * df["Доля"]
df["Голосов"] = df["Голосов"].round(2)

# Удаление временных столбцов
df = df.drop(columns=["Числитель", "Знаменатель", "Доля"])

# Сохраняем измененный DataFrame обратно в файл
df.to_excel("combined_data_with_votes.xlsx", index=False, engine="openpyxl")