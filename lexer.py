'''Define tokens:

palavras reservadas

símbolos (:, ;, ->, [ ], etc.)

NUM, BOOL, ID_DEVICE, ID_OBS, MSG

operadores lógicos (> < >= <= == !=)

AND

Usa SLY.Lexer.'''

from sly import Lexer

class ObsLexer(Lexer):
    tokens = {
        ID_DEVICE, ID_OBS, NUM, BOOL, MSG,
        OP_LOGIC, AND,
        DEF, QUANDO, EXECUTE, EM, ALERTA, PARA,
        DIFUNDIR, SETA, FIMDISPOSITIVOS, DISPOSITIVOS,
        SENAO
    }

    ignore = ' \t'
    ignore_comment = r'//.*'

    # Palavras reservadas
    DISPOSITIVOS = r'dispositivos'
    FIMDISPOSITIVOS = r'fimdispositivos'
    DEF = r'def'
    QUANDO = r'quando'
    EXECUTE = r'execute'
    EM = r'em'
    ALERTA = r'alerta'
    PARA = r'para'
    DIFUNDIR = r'difundir'
    SENAO = r'senao'
    AND = r'AND'

    # Tokens simples
    OP_LOGIC = r'(>=|<=|==|!=|>|<)'
    SETA = r'->'

    # Literais diretos
    literals = { '[', ']', ':', ';', ',', }

    @_(r'True|False')
    def BOOL(self, t):
        t.value = True if t.value == "True" else False
        return t

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[^"]*"')
    def MSG(self, t):
        t.value = t.value.strip('"')
        return t

    # ID_DEVICE = só letras
    @_(r'[A-Za-z]+')
    def ID_DEVICE(self, t):
        # Pode ser ID_DEVICE ou palavra reservada
        keywords = {
            'dispositivos': 'DISPOSITIVOS',
            'fimdispositivos': 'FIMDISPOSITIVOS',
            'def': 'DEF',
            'quando': 'QUANDO',
            'execute': 'EXECUTE',
            'em': 'EM',
            'alerta': 'ALERTA',
            'para': 'PARA',
            'difundir': 'DIFUNDIR',
            'senao': 'SENAO',
        }
        if t.value in keywords:
            t.type = keywords[t.value]
        return t

    # ID_OBS = começa com letra, pode ter número
    @_(r'[A-Za-z][A-Za-z0-9_]*')
    def ID_OBS(self, t):
        return t

    def error(self, t):
        print(f"Caractere ilegal '{t.value[0]}'")
        self.index += 1
