from datetime import datetime

import data_download as dd
import data_plotting as dplt



def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    preset_periods = {
        '1d': '1 день',
        '5d': '5 дней',
        '1mo': '1 месяц',
        '3mo': '3 месяца',
        '6mo': '6 месяцев',
        '1y': '1 год',
        '2y': '2 года',
        '5y': '5 лет',
        '10y': '10 лет',
        'ytd': 'С начала года',
        'max': 'Максимальный период'}

    while True:
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
        choice = input(
            "Вы хотите (1) использовать предустановленные промежутки времени или (2) ввести свои даты? (введите 1 или 2): ")
        if choice == '1':
            print("Выберите период:")
            for key, value in preset_periods.items():
                print(f"{key}: {value}")
            period = input("Введите выбранный период: ")

            # Проверка корректности выбранного периода
            if period not in preset_periods:
                print("Ошибка: неверный выбор периода.")
                continue
            stock_data = dd.fetch_stock_data(ticker, period)
        elif choice == '2':
            start_date = input("Введите дату начала интересующего вас периода в формате YYYY-MM-DD")
            end_date = input("Введите дату конца интересующего вас периода в формате YYYY-MM-DD")
            # Проверка корректности введенных дат
            try:
                start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
                if start_date_dt >= end_date_dt:
                    print("Ошибка: начальная дата должна быть раньше конечной даты.")
                    continue
            except ValueError:
                print("Ошибка: неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")
                continue
            stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
            # Проверка наличия данных о акции
        if stock_data.empty:
            print(f"Нет данных для тикера '{ticker}'. Пожалуйста, проверьте правильность введенного тикера и запрашиваемого перода времени")
            continue  # Возврат к началу цикла для повторного ввода
        threshold = int(input(
            'Введите порог колебания акций относительно средней цены закрытия в процентах (по умолчанию 20%) ').strip() or '20')

        # Добавление скользящего среднего, RSI, MACD
        stock_data = dd.add_moving_average(stock_data) # Добавляем расчет Скользящего среднего
        stock_data = dd.calculate_rsi(stock_data)  # Добавляем расчет RSI
        stock_data = dd.calculate_macd(stock_data)  # Добавляем расчет MACD
        print(stock_data)

        # Отрисовка графика и сохранение БД в csv-файл
        if choice == '1':
            dplt.create_and_save_plot(stock_data, ticker, period)
            dplt.export_data_to_csv(stock_data, f'{ticker}_{period}')
        else:
            dplt.create_and_save_plot(stock_data, ticker, f"{start_date} to {end_date}")
            dplt.export_data_to_csv(stock_data, f'{ticker}_{start_date}_{end_date}')

        print(dd.calculate_and_display_average_price(stock_data))

        # Расчет процента колебаний
        if dd.notify_if_strong_fluctuations(stock_data, threshold) is not None:
            print(dd.notify_if_strong_fluctuations(stock_data, threshold))

        break  # Выход из цикла, если данные успешно получены


if __name__ == "__main__":
    main()
