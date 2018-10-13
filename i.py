filename = 'types' # input()
file = open(filename + '.vvsql', 'r')
responseText = ''.join(file.read().split('\n'))
file.close()
# Получение БД
writeFile = open(filename + '.vvsql', 'w')
# Разделение н астроки
linedResponseText = responseText.split('%%n%%')
# Создание массива данных и заголовков
resultArray = []
resultArrayHeaders = []
# Первая строка отвечает за заголовки, остальные за данные
isHeaders = True
# Добавление данных в массив данных
for i in linedResponseText:
	if isHeaders:
		headers = i.split('%%d%%')
		for j in headers:

		isHeaders = False
		headers = None
	else:
		resultArray += [i.split('%%d%%')]
# Создание массива команд-методов
cmdArray = ['open']
while cmdArray[0] != 'close':
	# Запрос команды
	command = input('\n>>> ')
	# Разделение запроса на команды-методы
	cmdArray = command.split('/')
	# Определение команды и методов
	if cmdArray[0] == 'get':
		try:
			if cmdArray[1] == 'response':
				print('<<< response:')
				print(responseText)
			elif cmdArray[1] == 'headers':
				print('<<< headers:')
				print(resultArrayHeaders)
			elif cmdArray[1] == 'contents':
				print('<<< contents:')
				print(resultArray)
			elif cmdArray[1] == 'column':
				if cmdArray[2] == 'n':
					result = []
					for i in resultArray:
						result += [i[int(cmdArray[3])]]
					print('<<< column ' + cmdArray[3] + ':')
					print(result)
					result = None
				elif cmdArray[2] == 't':
					result = []
					orderNumber = resultArrayHeaders.index(cmdArray[3])
					for i in resultArray:
						result += [i[orderNumber]]
					print('<<< column ' + cmdArray[3] + ':')
					print(result)
					result = None
				else:
					print('err: Аргумент метода get/column некорректный')
			elif cmdArray[1] == 'row':
				print('<<< row ' + cmdArray[2] + ':')
				print(resultArray[int(cmdArray[2])])
			else:
				print('err: Аргумент метода get не найден')
		except Exception as e:
			print('err: Аргументы метода get отсутствуют или некорректны')
	elif cmdArray[0] == 'add':
		try:
			if cmdArray[1] == 'row':
				data = input('Данные через "%%d%%". ' + str(len(resultArrayHeaders)) + ' пунктов ::: ')
				data = data.split('%%d%%')
				resultArray += [data]
				print('<<< contents:')
				print(resultArray)
			elif cmdArray[1] == 'column':
				print('add column command')
			else: 
				print('err: Аргументы метода add некорректны')
		except Exception as e:
			print('err: Аргументы метода add отсутствуют или некорректны')
	elif cmdArray[0] == 'remove':
		print('remove command')
	elif cmdArray[0] == '':
		cmdArray[0] = 'close'
	elif cmdArray[0] == '-v':
		print('<<< i.py vvSQL 0.0.1dev')
	else:
		if cmdArray[0] != 'close':
			print('err: Команда ' + cmdArray[0] + ' не найдена')
# Формировение респонса и отправление в БД
headersToWrite = '%%d%%'.join(resultArrayHeaders)
contentsToWrite = []
for i in resultArray:
	contentsToWrite += ['%%d%%'.join(i)]
responseToWrite = headersToWrite + '%%n%%' + '%%n%%'.join(contentsToWrite)
writeFile.write(responseToWrite)
print('--- closed and saved')