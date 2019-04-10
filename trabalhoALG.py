#Nome: Julio Mendonca dos Santos Bueno ----- nºUSP: 10295162
#Nome: Felipe Dias Prado               ----- nºUSP: 8936586



import os


#-------cria flag indicando que o arquivo ainda nao foi salvo----------
def createFile():
	file=open('flag.txt','w')
	return file


#-------deleta flag indicando que o arquivo foi salvo----------------
def deleteFile(file):
	file.close()
	os.remove("flag.txt")



#---------------verifica se os arquivos foram salvos------------------------------
def saved(rrn):
	try:
		with open('flag.txt', 'r') as f:

			print("Recuperando dados")
			
			fileDados =open("dados.txt","r")
			fileRegistro =open("primario.ndx","w+")
			linhas = fileDados.readlines()
			for i in range(0,len(linhas)):
				rrn+=len(linhas[i])+1
				
			# fileRegistro.write("{}\n".format(rrn)
			fileRegistro.write("{}\n".format(rrn))
			rrn=0
			for linha in linhas:
				
				
				nro = linha.split("|")[1]
				if nro[0] != "$":
					fileRegistro.write("{} {}\n".format(nro,rrn))
				
				rrn+=len(linha)+1

			fileDados.close()
			fileRegistro.close()

		return 1
	except IOError:
		return 0

def dadosExist():
	try:
		with open('dados.txt', 'r') as f:
			return 1
	except IOError:
		return 0

#----------------verifica se dados.txt ja foi iniciado-------------
def checkInitializated(file):
	checkLine=file.readline()
	if len(checkLine)==0:
		return 0
	else:
		return 1



#---cria o arquivo dados.txt e primario.ndx e insere os valores neles-------
def beginFiles(file,file2,dicionario,rrn):
	linhas=file.readlines()

	for linha in linhas[3:-1]:

		nro = linha.split("|")[1]
		nro = nro.strip(" ")


		nome = linha.split("|")[2]
		nome = nome.strip(" ")

		carro=linha.split("|")[3]
		carro=carro.strip(" ")
		dado="|{}|{}|{}|\n".format(nro,nome,carro)
		file2.write(dado)
		dicionario[nro]=rrn
		rrn+=len(dado)+1
	return rrn


#---le os arquivos dados.txt e primario.ndx --------------
def continueFiles(file,dicionario,rrn):
	rrn=file.readline().split("\n")[0]

	linhas=file.readlines()
	for linha in linhas:
		key=linha.split(" ")[0]
		value=linha.split(" ")[1]
		value=value.split("\n")[0]
		dicionario[key]=value
	
	return rrn


#---------------busca usuario----------------------
def busca(dicionario,chave):
	try:
		dicionario[chave] 
		return dicionario[chave]
	
	except Exception:
		#print("chave inexistente")
		return -1
	
		

#--------------retira os cadastros previamente excluidos--------------------------
def compactation(file,dicionario):

	linhas=file.readlines()
	rrn=0
	file.close()
	file=open("dados.txt","w+")

	for linha in linhas:

			nro = linha.split("|")[1]

			nome = linha.split("|")[2]

			carro=linha.split("|")[3]

			
			if nro[0] != '$':
				
				dado="|{}|{}|{}|\n".format(nro,nome,carro)
				file.write(dado)
				dicionario[nro]=rrn
				rrn+=len(dado)+1





#--------------salva os dados chas chaves e cadastros----------------------
def saveRegister(file,dicionario,rrn):

	file.seek(0)
	file.write("{}\n".format(rrn))
	items = dicionario.items()
	for key, value in items:

		value=int(value)
		file.write("{} {}\n".format(key,value))




#--------------------------inicio da main------------------------------------------






rrn=0
dicionarioIndex={}


fileTabelaInicial=open("TabelaInicial.txt","r")

if saved(rrn) == 1:
	print("DadosRecuperados")


if dadosExist() == 1:

	fileDados=open("dados.txt","r+")
	fileRegistro=open("primario.ndx","r+")

	rrn=continueFiles(fileRegistro,dicionarioIndex,rrn)

else:
	fileDados=open("dados.txt","w+")
	fileRegistro=open("primario.ndx","w+")

	rrn=beginFiles(fileTabelaInicial,fileDados,dicionarioIndex,rrn)






# rrn=inicioFiles(fileTabelaInicial,fileDados,fileRegistro,dicionarioIndex,rrn)

rrn=int(rrn)

fileTabelaInicial.close()
fileDados.close()
fileRegistro.close()




fileRegistro=open("primario.ndx","w")

option=1
while option!=0:
	
	flagFile=createFile()

	print("Menu----------")
	print("(1): Inserir")
	print("(2): remover")
	print("(3): alterar")
	print("(4): buscar")
	print("(5): compactar")
	print("(0): Sair")
	option =int(input('digite a opcao: '))

	if option == 1:
		
		fileDados=open("dados.txt","a")

		nro= input('digite o numero : ')
		if busca(dicionarioIndex,nro) == -1:
			nome = input('digite o nome  : ')
			carro= input('digite o carro : ')
			# fileDados.seek(int(rrn))
			fileDados.write("|{}|{}|{}|\n".format(nro, nome, carro))
			dicionarioIndex[nro]=rrn
			dado="|{}|{}|{}|\n".format(nro,nome,carro)
			#fileRegistro.write("{} {}\n".format(nro,rrn))
			rrn=int(rrn)
			rrn+=len(dado)+1
			

			print("Cadastro inserido com sucesso")

		else:
			print("Cadastro ja existente")

		input("para voltar ao menu inicial pressione enter")
		fileDados.close()



	if option == 2:


		fileDados=open("dados.txt","r+")
		indexBusca=input('digite o numero a ser removido :')
		position=busca(dicionarioIndex,indexBusca)
		position=int(position)
		if position != -1:
			fileDados.seek(position+1)
			fileDados.write('$')
			del dicionarioIndex[indexBusca]
			print("Cadastro Removido com sucesso")
		else:
			print("Cadastro inexistente")

		input("para voltar ao menu inicial pressione enter")
		fileDados.close()


	if option == 3:
		fileDados=open("dados.txt","r+")

		indexBusca=input('digite o numero a ser alterado :')
		position=busca(dicionarioIndex,indexBusca)
		position=int(position)
		if position != -1:
			fileDados.seek(position+1)
			fileDados.write('$')
			del dicionarioIndex[indexBusca]
			nro= input('digite o numero : ')
			nome = input('digite o nome : ')
			carro= input('digite o carro : ')
			fileDados.seek(rrn)
			fileDados.write("|{}|{}|{}|\n".format(nro, nome, carro))
			dicionarioIndex[nro]=rrn
			dado="|{}|{}|{}|\n".format(nro,nome,carro)
			rrn+=len(dado)+1
			print("Cadastro alterado com sucesso")	
		
		else:
			print("Cadastro inexistente")

		input("para voltar ao menu inicial pressione enter")
		fileDados.close()




	if option == 4:
		fileDados=open("dados.txt","r+")
		
		indexBusca=input('digite o numero a ser buscado :')
		position=busca(dicionarioIndex,indexBusca)
		position=int(position)
		if position != -1:
			fileDados.seek(position)
			linha=fileDados.readline()
			linha = linha.split("|")
			nro = linha[1]
			nome = linha[2]
			carro=linha[3]
			print('Numero: {}\nNome:{}\ncarro :{}'.format(nro,nome,carro))
	
		else:
			print("Cadastro inexistente")

		input("para voltar ao menu inicial pressione enter")

		fileDados.close()
	
	

	if option == 5:
		fileDados=open("dados.txt","r+")

		compactation(fileDados,dicionarioIndex)
		print("arquivo compactado com sucesso")
		fileDados.close()


	#os.system('cls');
	#os.system('clear');
	deleteFile(flagFile)	


saveRegister(fileRegistro,dicionarioIndex,rrn)
fileRegistro.close()







print("------------------PROGRAMA ENCERRADO-----------------")