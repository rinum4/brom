# -*- coding: utf-8 -*-
"""
Выборки

@author: Rinat
"""

from brom import *
from datetime import date
from uuid import uuid4,UUID

# Создаем клиент
клиент = БромКлиент("http://localhost/ERP", "bromuser", "111")

# # Выборка всех элементов справочника "Номенклатура"
текСелектор = клиент.СоздатьСелектор()

текСелектор.УстановитьКоллекцию("Справочник.Номенклатура")
текСелектор.АвтозагрузкаПолей = АвтозагрузкаПолейОбъектов.ТолькоСтандартныеРеквизиты()

for текСсылка in текСелектор:
 	print("Наименование: {0}; Код: {1}".format(текСсылка.Наименование, текСсылка.Код))

# Добавляем отбор и дозапрашиваем данные производителя
текСелектор.ДобавитьОтбор("ЭтоГруппа", False)
текСелектор.ДобавитьСортировку("Наименование")
текСелектор.ДобавитьПоля("Производитель")

for текСсылка in текСелектор:
 	print("Наименование: {0}; Код: {1}, Производитель: {2};".format(
		текСсылка.Наименование,
		текСсылка.Код,
		текСсылка.Производитель
 	))

# Сохраняем результат выборки в массив для последующего использования
результат = текСелектор.ВыгрузитьРезультат()

# # Выборка из справочника "Номенклатура" в стиле языка запросов
# текСелектор = клиент.СоздатьСелектор()

# текСелектор.\
# 	Выбрать("Наименование, Код, Производитель").\
# 	Первые(20).\
# 	Из("Справочник.Номенклатура").\
# 	Где("ЭтоГруппа", False).\
# 	Где("Родитель.Наименование", "Мебель").\
# 	Упорядочить("Наименование")
#  Важно! НаправлениеСортирвки.Убывание не работает

# for текСсылка in текСелектор:
# 	print("Наименование: {0}; Код: {1}, Производитель: {2};".format(
# 		текСсылка.Наименование,
# 		текСсылка.Код,
# 		текСсылка.Производитель
# 	))

# # Сохраняем результат выборки в массив для последующего использования
# результат = текСелектор.ВыгрузитьРезультат()

# # Выборка номенклатуры из группы "Мебель"
# группаМебель = клиент.Справочники.Номенклатура.НайтиПоНаименованию("Мебель")

# текСелектор = клиент.Справочники.Номенклатура.СоздатьСелектор()

# текСелектор.\
# 	Выбрать("Наименование, Код, Производитель").\
# 	Где("ЭтоГруппа", False).\
# 	Где("Ссылка", группаМебель, ВидСравнения.ВИерархии).\
# 	Упорядочить("Производитель").\
# 	Упорядочить("Наименование", НаправлениеСортирвки.Убывание)

# for текСсылка in текСелектор:
# 	print("Наименование: {0}; Код: {1}, Производитель: {2}; ".format(
# 		текСсылка.Наименование,
# 		текСсылка.Код,
# 		текСсылка.Производитель
# 	))

# # Сохраняем результат выборки в массив для последующего использования
# результат = текСелектор.ВыгрузитьРезультат()

# # Выборка заказов с определенной даты, в которых есть товары из раздела "Мебель"
# группаМебель = клиент.Справочники.Номенклатура.НайтиПоНаименованию("Мебель")

текСелектор = клиент.Документы.ЗаказКлиента.СоздатьСелектор()

# текСелектор.\
# 	Выбрать("Дата, Номер, Контрагент").\
# 	Где("Проведен", True).\
# 	Где("Дата", date(2015, 1, 1), ВидСравнения.БольшеИлиРавно).\
# 	Где("Товары.Номенклатура", группаМебель, ВидСравнения.ВИерархии).\
# 	Упорядочить("Контрагент").\
# 	Упорядочить("Дата")

# for текСсылка in текСелектор:
# 	print("Дата: {0}; Номер: {1}; Контрагент: {2}".format(
# 		текСсылка.Дата,
# 		текСсылка.Номер,
# 		текСсылка.Контрагент
# 	))

# # Сохраняем результат выборки в массив для последующего использования
# результат = текСелектор.ВыгрузитьРезультат()

"""Установка отборов"""
# # Пример отборов для справочника
# текСелектор.ДобавитьОтбор("Артикул", "Т-0001")
# текСелектор.ДобавитьОтбор("Вес", 15, ВидСравнения.БольшеИлиРавно)
# текСелектор.ДобавитьОтбор("Ссылка", группаМебель, ВидСравнения.НеВИерархии)
# текСелектор.ДобавитьОтбор(
# 	"Производитель.Родитель",
# 	[ссылка1, ссылка2, ссылка3],
# 	ВидСравнения.ВСписке
# )

# Пример отборов для документа
# текСелектор.\
# 	Где("Дата", date(2019, 1, 1), ВидСравнения.БольшеИлиРавно).\
# 	Где("Товары.Номенклатура", [ссылка1, ссылка2, ссылка3], ВидСравнения.ВСписке).\
# 	Где("Проведен", True, ВидСравнения.Равно).\
# 	Где("ДокументОснование", клиент.Документы.ЗаказКлиента.ПустаяСсылка(), ВидСравнения.НеРавно)

"""Сортировка выборок"""
# текСелектор.ДобавитьСортировку("Наименование")
# текСелектор.ДобавитьСортировку("Производитель.Наименование", True)


"""Загрузка контекстных данных"""
# # Неоптимальный вариант работы с данными
# текСелектор = клиент.Справочники.Номенклатура.СоздатьСелектор()

# for текСсылка in текСелектор:
# 	print("Наименование: {0}; Производитель: {1}".format(текСсылка.Наименование, текСсылка.Производитель))
# 	# В каждой итерации будет происходить два запроса на сервер:
# 	#  - запрос на получение ВСЕХ контекстных данных ссылки "текСсылка", включая данные табличных частей;
# 	#  - запрос на получение ВСЕХ контекстных данных ссылки "Производитель" для формирования представления ссылки.
# 	# Это медленно и крайне неэффективно!

# # Оптимальный вариант работы с данными
# текСелектор = клиент.Справочники.Номенклатура.СоздатьСелектор()

# текСелектор.ДобавитьПоля("Наименование, Производитель")

# for текСсылка in текСелектор:
# 	print("Наименование: {0}; Производитель: {1}".format(текСсылка.Наименование, текСсылка.Производитель))
# 	# Дополнительных запросов на сервер происходить не будет,

# # Будут загружены данные только стандартных реквизитов
# текСелектор.АвтозагрузкаПолей = АвтозагрузкаПолейОбъектов.ТолькоСтандартныеРеквизиты()
# # Будут загружены данные всех реквизитов объекта (без табличных частей)
# текСелектор.АвтозагрузкаПолей = АвтозагрузкаПолейОбъектов.ТолькоРеквизиты()
# # Будут загружены все данные объекта (реквизиты и табличные части)
# текСелектор.АвтозагрузкаПолей = АвтозагрузкаПолейОбъектов.ВсеПоля()

"""Ограничение размера выборки"""
# текСелектор.Лимит = 10
# текСелектор.Первые(10)









