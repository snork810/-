import data_download as dd
import data_plotting as dplt



def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    while True:
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        threshold = int(input(
            'Введите порог колебания акций относительно средней цены закрытия в процентах (по умолчанию 20%) ').strip() or '20')

        # Fetch stock data
        stock_data = dd.fetch_stock_data(ticker, period)

        # Проверка наличия данных о акции
        if stock_data.empty:
            print(f"Нет данных для тикера '{ticker}'. Пожалуйста, проверьте правильность введенного тикера и запрашиваемого перода времени")
            continue  # Возврат к началу цикла для повторного ввода

        # Add moving average to the data
        stock_data = dd.add_moving_average(stock_data)

        # Plot the data
        dplt.create_and_save_plot(stock_data, ticker, period)
        print(dd.calculate_and_display_average_price(stock_data))

        # Calculation of the percentage of fluctuations
        if dd.notify_if_strong_fluctuations(stock_data, threshold) is not None:
            print(dd.notify_if_strong_fluctuations(stock_data, threshold))

        break  # Выход из цикла, если данные успешно получены


if __name__ == "__main__":
    main()
