import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.metrics import mean_absolute_error, r2_score # type: ignore


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

        plt.plot(test_data.values, label="Actual", marker='o') 
        plt.plot(pred_data, label="Predicted", marker='x')

        plt.legend()
        plt.xlabel("Дата")
        plt.ylabel("Ціна золота")
        plt.title("Фактичні та 'навчені' ціни золота")
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

        self.vizualization(y_test, y_pred)


    def predict_next_year(self):
        """ Predict gold price for the next year """
        future_features = self.df[self.features].tail(365)  
        future_preds = self.model.predict(future_features)
        # print(f"Predicted Gold Price for next year: {future_preds}")

        plt.figure(figsize=(10, 5))
        plt.plot(range(0, 365), future_preds, label="Predicted Prices", marker='x', linestyle='--', color='red')
        plt.legend()
        plt.xlabel("Дата")
        plt.ylabel("Ціна золота")
        plt.title("Передбачені ціни золота на наступний рік")
        plt.grid(True)
        plt.xticks(range(0, 365, 30))  
        plt.show()


def main():
    url = './data/Gold Price Prediction.csv'
    features = ['Price 1 Day Prior', 'Price 2 Days Prior', 'Twenty Moving Average', 'EFFR Rate', 'DXY', 'SP Open']
    target = 'Price Tomorrow'
    pp = PricePrediction(url, features, target)
    pp.train_model()
    pp.predict_next_year()


if __name__ == "__main__":
    main()