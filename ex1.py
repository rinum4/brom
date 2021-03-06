# -*- coding: utf-8 -*-
"""
Подключение

@author: Rinat
"""

from brom import *

# Создаем клиент
клиент = БромКлиент("http://localhost/ERP", "bromuser", "111")

# Получаем ссылку на элемент справочника "ВидыНоменклатуры"
видТовары = клиент.Справочники.ВидыНоменклатуры.НайтиПоНаименованию("Товары")

# Создаем запрос
текЗапрос = клиент.СоздатьЗапрос("""
	ВЫБРАТЬ
		Номенклатура.Ссылка КАК Ссылка,
		Номенклатура.Наименование КАК Наименование,
		Номенклатура.Артикул КАК Артикул
	ИЗ
		Справочник.Номенклатура КАК Номенклатура
	ГДЕ
		Номенклатура.ЭтоГруппа = ЛОЖЬ
		И Номенклатура.ВидНоменклатуры = &ВидНоменклатуры
	УПОРЯДОЧИТЬ ПО
		Наименование
""")

# Устанавливаем значение параметра запроса
текЗапрос.УстановитьПараметр("ВидНоменклатуры", видТовары)

# Выполняем запрос и выводим результат на экран
результат = текЗапрос.Выполнить()
for стр in результат:
	print("Товар: {0}; Артикул: {1}".format(стр.Наименование, стр.Артикул))

# TODO...