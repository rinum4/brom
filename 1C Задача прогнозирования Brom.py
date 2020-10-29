# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 01:51:01 2020

@author: Ринат
"""
from brom import *
from datetime import date, datetime, timedelta
from uuid import uuid4,UUID

# Создаем клиент
клиент = БромКлиент("http://localhost/ERP", "bromuser", "111")

текЗапрос = клиент.СоздатьЗапрос("""
ВЫБРАТЬ
	ВыручкаИСебестоимостьПродаж.АналитикаУчетаНоменклатуры.Номенклатура КАК Номенклатура,
	ВыручкаИСебестоимостьПродаж.Количество КАК Количество
ИЗ
	РегистрНакопления.ВыручкаИСебестоимостьПродаж КАК ВыручкаИСебестоимостьПродаж
ГДЕ
	ВыручкаИСебестоимостьПродаж.ВидЗапасов.Организация = &Организация

УПОРЯДОЧИТЬ ПО
	ВыручкаИСебестоимостьПродаж.Период
""")

текЗапрос.УстановитьПараметр("Организация", клиент.Справочники.Организации.НайтиПоНаименованию(".ЗадачаПрогнозирования"))

результат = текЗапрос.Выполнить()


prod = {}
quantity = {}
i=0

for стр in результат:
# 	print("Номенклатура: {0}; Количество: {1}".format(стр.Номенклатура,стр.Количество))
    prod[i] =стр.Номенклатура.Наименование
    quantity[i] = float(стр.Количество)
    i=i+1


from sample3_3 import *

n_lag = 1
n_seq = 3
n_test = -36     # 10   -36
n_epochs = 100   # 1500 300
n_batch = 1
n_neurons = 4   # 1 4
# prepare data
import pandas as pd
import numpy

numpy.random.seed(27)

# create a series
series = pd.Series(quantity)

#from matplotlib import pyplot
#pyplot.plot(series.values)

scaler, train, test = prepare_data(series, n_test, n_lag, n_seq)

model = fit_lstm(train, n_lag, n_seq, n_batch, n_epochs, n_neurons)
# make forecasts
model.reset_states()
#forecasts = make_forecasts(model, n_batch, test, n_lag, n_seq)
forecasts = make_forecasts_fin(model, n_batch, train, n_lag, n_seq)
# inverse transform forecasts and test
#forecasts = inverse_transform(series, forecasts, scaler, n_test+2)
forecasts_i = inverse_transform(series, forecasts, scaler, -n_test)

#actual = [row[n_lag:] for row in test]
#actual = inverse_transform(series, actual, scaler, n_test+2)
# evaluate forecasts
#evaluate_forecasts(actual, forecasts, n_lag, n_seq)

# plot forecasts
plot_forecasts(series, forecasts_i, 0)

from dateutil.relativedelta import relativedelta
today = date.today()
begDate = today + relativedelta(months=1)
first_beg_day = begDate.replace(day=1)
endDate = today + relativedelta(months=3)
first_end_day = endDate.replace(day=1)

докОбъект = клиент.Документы.ПланПродаж.СоздатьДокумент()
# # Заполняем реквизиты
докОбъект.Дата			= datetime.today()
докОбъект.Сценарий	    = клиент.Справочники.СценарииТоварногоПланирования.НайтиПоНаименованию("ПланДляПрогноза")
докОбъект.ВидПлана	    = клиент.Справочники.ВидыПланов.НайтиПоНаименованию("Плана продаж на 3 мес")
докОбъект.НачалоПериода	   = first_beg_day
докОбъект.ОкончаниеПериода	 = first_end_day
докОбъект.Статус        = клиент.Перечисления.СтатусыПланов.ВПодготовке


# Заполняем табличную часть "Товары"
for i in range(len(forecasts_i[0])):
    стр = докОбъект.Товары.Добавить()
    стр.Номенклатура	= клиент.Справочники.Номенклатура.НайтиПоНаименованию("А")
    стр.Количество		= str(round(forecasts_i[0][i],0))
    стр.КоличествоУпаковок = str(round(forecasts_i[0][i],0))
    стр.Цена = 30000
    стр.Сумма = стр.КоличествоУпаковок * стр.Цена
    iday = today + relativedelta(months=i+1)
    first_i_day = iday.replace(day=1)
    стр.ДатаОтгрузки = first_i_day

# Записываем состояние объекта в режиме проведения
докОбъект.Записать(РежимЗаписиДокумента.Запись)