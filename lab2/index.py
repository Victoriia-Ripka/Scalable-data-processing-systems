import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.metrics import mean_absolute_error, r2_score # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from datetime import timedelta


class PricePrediction:
    def __init__(self, url, features, target):
        self.df = pd.read_csv(url)
        self.features = features
        self.target = target
        self.model = LinearRegression()


    def cleanDF(self):
        """ Видаляємо рядки з пропущеними значеннями """
        print("count of rows before cleaning: ", self.df.shape[0])
        self.df = self.df.dropna()  
        print("count of rows after cleaning: ", self.df.shape[0])


    def vizualization(self, test_data, pred_data):
        """ Візуалізація фактичних і передбачених значень із датами на осі X """
        plt.figure(figsize=(10,5))

        # if isinstance(test_data, pd.Series):
        #     test_data = test_data.reset_index(drop=True)
        # if isinstance(pred_data, np.ndarray):
        #     pred_data = pd.Series(pred_data) 

        # plt.plot(self.df.index[-len(test_data):], test_data.values, label="Actual", marker='o')
        # plt.plot(self.df.index[-len(pred_data):], pred_data, label="Predicted", marker='x')

        plt.plot(test_data.values, label="Actual", marker='o') #self.df['Date'], 
        plt.plot(pred_data, label="Predicted", marker='x')

        plt.legend()
        plt.xlabel("Дата")
        plt.ylabel("Ціна золота")
        plt.title("Фактичні та передбачені ціни золота")
        plt.grid()
        plt.xticks(rotation=45)
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


        # if 'Date' not in self.df.columns:
        #     start_date = pd.to_datetime("2022-01-03")
        #     dates = pd.date_range(start_date, periods=len(self.df), freq='D')
        #     self.df['Date'] = dates

        # self.df.set_index('Date', inplace=True)

        self.vizualization(y_test, y_pred)


    def predict_next_year(self):
        """ Прогноз на 365 днів уперед з урахуванням часу та ковзних середніх """
        last_known_data = self.df.iloc[-1].copy()  # Копіюємо останній рядок
        future_predictions = []

        for i in range(365):
            # Додаємо 1 день до дати
            last_known_data["Date"] = pd.to_datetime(last_known_data["Date"]) + timedelta(days=1)
            last_known_data["day_of_year"] = last_known_data["Date"].dayofyear
            last_known_data["month"] = last_known_data["Date"].month

            # Готуємо фічі для передбачення
            input_features = last_known_data[self.features].values.reshape(1, -1)
            print(input_features)

            # Робимо прогноз
            # next_day_price = self.model.predict(input_features)[0]
            # future_predictions.append(next_day_price)

            # Оновлюємо рядок новими значеннями
            # last_known_data["Price 2 Days Prior"] = last_known_data["Price 1 Day Prior"]
            # last_known_data["Price 1 Day Prior"] = last_known_data["Price Tomorrow"]
            # last_known_data["Price Tomorrow"] = next_day_price  # Нове значення

            # Оновлюємо ковзні середні
            # last_known_data["Twenty Moving Average"] = (
            #     (last_known_data["Twenty Moving Average"] * 19 + next_day_price) / 20
            # )
            # last_known_data["Fifty Day Moving Average"] = (
            #     (last_known_data["Fifty Day Moving Average"] * 49 + next_day_price) / 50
            # )

        return future_predictions


    def predict_next_month(self):
        """ Прогноз на 30 днів уперед з урахуванням часу та ковзних середніх """
        if 'Date' not in self.df.columns:
            print("Error: 'Date' column is missing in the DataFrame.")
            return []


        last_known_data = self.df.iloc[-1].copy()  # Копіюємо останній рядок
        future_predictions = []

        for i in range(30):  # Прогноз на 30 днів
            # Додаємо 1 день до дати
            last_known_data["Date"] = pd.to_datetime(last_known_data["Date"]) + timedelta(days=1)
            last_known_data["day_of_year"] = last_known_data["Date"].dayofyear
            last_known_data["month"] = last_known_data["Date"].month

            # Готуємо фічі для передбачення
            input_features = last_known_data[self.features].values.reshape(1, -1)

            # Робимо прогноз
            next_day_price = self.model.predict(input_features)[0]
            future_predictions.append(next_day_price)

            # Оновлюємо рядок новими значеннями
            last_known_data["Price 2 Days Prior"] = last_known_data["Price 1 Day Prior"]
            last_known_data["Price 1 Day Prior"] = next_day_price
            last_known_data["Price Tomorrow"] = next_day_price  # Нове значення

            # Оновлюємо ковзні середні (якщо вони є в даних)
            if "Twenty Moving Average" in last_known_data:
                last_known_data["Twenty Moving Average"] = (
                    (last_known_data["Twenty Moving Average"] * 19 + next_day_price) / 20
                )
            if "Fifty Day Moving Average" in last_known_data:
                last_known_data["Fifty Day Moving Average"] = (
                    (last_known_data["Fifty Day Moving Average"] * 49 + next_day_price) / 50
                )

        return future_predictions


def main():
    url = './data/Gold Price Prediction.csv'
    features = ['Price 1 Day Prior', 'Price 2 Days Prior', 'Twenty Moving Average', 'EFFR Rate', 'DXY', 'SP Open']
    target = 'Price Tomorrow'
    pp = PricePrediction(url, features, target)
    pp.train_model()
    
    # future_prices = pp.predict_next_year()
    # future_prices = pp.predict_next_month()

    # Візуалізація прогнозу на рік
    # plt.figure(figsize=(12,5))
    # plt.plot(future_prices, label="Predicted Price (Next Year)", linestyle="dashed", color="red")
    # plt.title("Прогноз ціни золота на наступний рік")
    # plt.xlabel("Дні")
    # plt.ylabel("Ціна золота")
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()