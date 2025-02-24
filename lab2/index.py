import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


class PricePrediction:
    
    def __init__(self, url, features, target):
        self.df = pd.read_csv(url)
        self.features = features
        self.target = target
        self.model = LinearRegression()


    def cleanDF(self):
        print("count of rows before cleaning: ", self.df.shape[0])
        self.df = self.df.dropna()  # Видаляємо рядки з пропущеними значеннями
        print("count of rows after cleaning: ", self.df.shape[0])


    def vizualization(self, y_test, y_pred):
        """ Візуалізація фактичних і передбачених значень """
        plt.figure(figsize=(10,5))
        plt.plot(y_test.values[:50], label="Actual", marker='o')
        plt.plot(y_pred[:50], label="Predicted", marker='x')
        plt.legend()
        plt.title("Фактичні та передбачені ціни золота")
        plt.show()


    def train_model(self):
        """ Навчаємо лінійну регресію для прогнозу ціни на наступний день """
        self.cleanDF()

        X = self.df[self.features]
        y = self.df[self.target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        # Оцінка моделі
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Mean Absolute Error (1 день): {mae:.2f}")
        print(f"R² Score (1 день): {r2:.2f}")

        self.vizualization(y_test, y_pred)


    def predict_next_year(self):
        """ Прогноз на 365 днів уперед """
        last_known_data = self.df.iloc[-1][self.features].values  # Останній рядок історичних даних
        future_predictions = []

        for i in range(365):
            next_day_price = self.model.predict([last_known_data])[0]  # Прогнозуємо наступний день
            future_predictions.append(next_day_price)

            # Оновлюємо last_known_data: 
            last_known_data = np.roll(last_known_data, -1)  # Зсуваємо значення
            last_known_data[0] = next_day_price  # Додаємо прогнозовану ціну

        return future_predictions


def main():
    url = './data/Gold Price Prediction.csv'
    features = ['Price 1 Day Prior', 'Price 2 Days Prior', 'Twenty Moving Average', 'EFFR Rate', 'DXY', 'SP Open']
    target = 'Price Tomorrow'
    pp = PricePrediction(url, features, target)
    pp.train_model()


if __name__ == "__main__":
    main()