from bokeh.plotting import figure, output_file, save
import logging

# Настраиваем ведение логов
logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


def create_and_save_plot(data, ticker, period, style):
    """
    Создает и сохраняет 4 графика:
    1) График закрытия цены и скользящего среднего
    2) График RSI
    3) График MACD
    4) График стандартного отклонения цен закрытия.

    :param data: DataFrame с информацией об акциях
    :param ticker: тикер акции
    :param period: временной период за который запрашиваются данные
    :param style: стиль оформления графиков
    :param filename: имя файла для сохранения графиков
    :return: None
    """

    # График закрытия цены и скользящего среднего
    output_file(f"{ticker}_{period}_{style}_stock_price_chart.html")
    p = figure(title=f"{ticker} Цена акций и Скользящее Среднее",
               x_axis_label='Дата',
               y_axis_label='Цена',
               x_axis_type='datetime',
               width=800,
               height=400)

    source = ColumnDataSource(data)
    p.line('index', 'Close', source=source, legend_label='Close Price', line_width=2, color='blue')
    p.line('index', 'Moving_Average', source=source, legend_label='Moving Average', line_width=2, color='orange')

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    save(p)
    logging.info(
        f"График закрытия цены и скользящего среднего сохранен как {ticker}_{period}_{style}_stock_price_chart.html")

    # График RSI
    output_file(f"{ticker}_{period}_{style}_RSI_chart.html")
    rsi_plot = figure(title=f"RSI для {ticker}",
                      x_axis_label='Дата',
                      y_axis_label='RSI',
                      x_axis_type='datetime',
                      width=800,  # Исправленный параметр ширины
                      height=400)  # Исправленный параметр высоты

    rsi_plot.line(data.index, data['RSI'], line_width=2, color='blue', legend_label='RSI')
    rsi_plot.line(data.index, [70] * len(data), line_width=2, color='red', line_dash='dashed',
                  legend_label='Overbought (70)')
    rsi_plot.line(data.index, [30] * len(data), line_width=2, color='green', line_dash='dashed',
                  legend_label='Oversold (30)')
    save(rsi_plot)
    logging.info(f"График RSI сохранен как {ticker}_{period}_RSI_chart.html")

    # График MACD
    output_file(f"{ticker}_{period}_{style}_MACD_chart.html")
    macd_plot = figure(title=f"MACD для {ticker}",
                       x_axis_label='Дата',
                       y_axis_label='MACD',
                       x_axis_type='datetime',
                       width=800,  # Исправленный параметр ширины
                       height=400)  # Исправленный параметр высоты

    macd_plot.line(data.index, data['MACD'], line_width=2, color='blue', legend_label='MACD')
    macd_plot.line(data.index, data['Signal'], line_width=2, color='orange', legend_label='Signal Line')
    save(macd_plot)
    logging.info(f"График MACD сохранен как {ticker}_{period}_MACD_chart.html")

    # График стандартного отклонения
    output_file(f"{ticker}_{period}_{style}_StdDev_chart.html")
    stddev_plot = figure(title=f"Стандартное отклонение для {ticker}",
                         x_axis_label='Дата',
                         y_axis_label='Стандартное отклонение',
                         x_axis_type='datetime',
                         width=800,
                         height=400)

    stddev_plot.line(data.index, data['Std_Dev'], line_width=2, color='purple', legend_label='Std Dev')
    save(stddev_plot)
    logging.info(f"График стандартного отклонения сохранен как {ticker}_{period}_{style}_StdDev_chart.html")


def export_data_to_csv(data, filename):
    """
    Сохраняет DataFrame в CSV файл.

    :param data: DataFrame с данными
    :param filename: имя файла для сохранения
    :return: None
    """
    logging.info(f"Таблица сохранена как {filename}.csv")
    data.to_csv(f'{filename}.csv', index=False)
