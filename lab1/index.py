import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def clean_data(df):
    """
    Видаляє всі рядки, що містять NaN у колонках 'math score', 'reading score' і 'writing score'.
    Значення 0 залишаються.
    """
    df_cleaned = df.dropna(subset=['math score', 'reading score', 'writing score'])
    return df_cleaned


def encode_categorical(df):
    """
    Кодує категоріальні змінні у числовий формат для кореляційного аналізу.
    """
    df_encoded = df.copy()

    # Кодування 'Освіта батьків'
    education_levels = {
        "some high school": 0,
        "high school": 1,
        "some college": 2,
        "associate's degree": 3,
        "bachelor's degree": 4,
        "master's degree": 5
    }
    df_encoded["Освіта батьків (код)"] = df_encoded["Освіта батьків"].map(education_levels)

    # Кодування 'Обід'
    lunch_mapping = {"free/reduced": 0, "standard": 1}
    df_encoded["Обід (код)"] = df_encoded["Обід"].map(lunch_mapping)

    # Кодування 'Курс підготовки'
    prep_mapping = {"none": 0, "completed": 1}
    df_encoded["Курс підготовки (код)"] = df_encoded["Курс підготовки"].map(prep_mapping)

    return df_encoded


def main():
    dfStudents = pd.read_csv('./data/StudentsPerformance.csv')
    
    # Очищення даних
    dfStudents = clean_data(dfStudents)

    # Перейменування стовпців
    dfStudents = dfStudents.rename(columns={
        "gender": "Стать",
        "race/ethnicity": "Раса/етнічність",
        "parental level of education": "Освіта батьків",
        "lunch": "Обід",
        "test preparation course": "Курс підготовки",
        "math score": "Оцінка з математики",
        "reading score": "Оцінка з читання",
        "writing score": "Оцінка з письма"
    })

    print(dfStudents.head())

    # Додавання нових колонок: загальна оцінка та середня оцінка
    dfStudents["Загальна оцінка"] = dfStudents["Оцінка з математики"] + dfStudents["Оцінка з читання"] + dfStudents["Оцінка з письма"]
    dfStudents["Середня оцінка"] = dfStudents["Загальна оцінка"] / 3

    # Розрахунок статистики
    stats = {
        "Оцінка з математики": {
            "Середнє": dfStudents["Оцінка з математики"].mean(),
            "Максимум": dfStudents["Оцінка з математики"].max(),
            "Мінімум": dfStudents["Оцінка з математики"].min()
        },
        "Оцінка з читання": {
            "Середнє": dfStudents["Оцінка з читання"].mean(),
            "Максимум": dfStudents["Оцінка з читання"].max(),
            "Мінімум": dfStudents["Оцінка з читання"].min()
        },
        "Оцінка з письма": {
            "Середнє": dfStudents["Оцінка з письма"].mean(),
            "Максимум": dfStudents["Оцінка з письма"].max(),
            "Мінімум": dfStudents["Оцінка з письма"].min()
        },
        "Середня оцінка": {
            "Середнє": dfStudents["Середня оцінка"].mean(),
            "Максимум": dfStudents["Середня оцінка"].max(),
            "Мінімум": dfStudents["Середня оцінка"].min()
        }
    }

    # Виведення результатів
    print("Статистика оцінок:")
    for subject, values in stats.items():
        print(f"\n{subject}:")
        for stat, value in values.items():
            print(f"  {stat}: {value:.2f}")


    # Кодування категоріальних змінних
    dfStudents = encode_categorical(dfStudents)

    #  Обчислення кореляції
    correlation_matrix = dfStudents[["Середня оцінка", "Освіта батьків (код)", "Обід (код)", "Курс підготовки (код)"]].corr()

    # Виведення кореляції
    print("\nКореляція середньої оцінки з іншими змінними:")
    print(correlation_matrix["Середня оцінка"])



main()