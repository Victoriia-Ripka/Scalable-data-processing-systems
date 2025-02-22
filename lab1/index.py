import pandas as pd
import seaborn as sns
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

    # Візуалізація розподілу оцінок
    dfStudents[['Оцінка з математики', 'Оцінка з читання', 'Оцінка з письма']].hist(bins=20, edgecolor='black', alpha=0.7)
    plt.suptitle("Розподіл оцінок")
    plt.show()

    # Додавання нових колонок: загальна оцінка та середня оцінка
    dfStudents["Загальна оцінка"] = dfStudents["Оцінка з математики"] + dfStudents["Оцінка з читання"] + dfStudents["Оцінка з письма"]
    dfStudents["Середня оцінка"] = dfStudents["Загальна оцінка"] / 3

    # Візуалізація середньої оцінки
    plt.figure(figsize=(8, 5))
    sns.histplot(dfStudents["Середня оцінка"], bins=20, kde=True, color='blue')
    plt.title("Розподіл середньої оцінки")
    plt.xlabel("Середня оцінка")
    plt.ylabel("Частота")
    plt.show()

    # Розрахунок статистики
    stats = dfStudents[['Оцінка з математики', 'Оцінка з читання', 'Оцінка з письма', 'Середня оцінка']].agg(['mean', 'max', 'min'])
    print("\nСтатистика оцінок:\n", stats)

    # Візуалізація boxplot для оцінок
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dfStudents[['Оцінка з математики', 'Оцінка з читання', 'Оцінка з письма']], palette="Set2")
    plt.title("Boxplot оцінок")
    plt.show()

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

    # Візуалізація кореляційної матриці
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Кореляційна матриця")
    plt.show()

    # Візуалізація залежності середньої оцінки від освіти батьків
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Освіта батьків", y="Середня оцінка", data=dfStudents, palette="Set3")
    plt.xticks(rotation=45)
    plt.title("Розподіл середніх оцінок за рівнем освіти батьків")
    plt.show()


main()