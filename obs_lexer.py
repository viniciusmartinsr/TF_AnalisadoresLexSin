# obs_lexer.py
from sly import Lexer

class ObsLexer(Lexer):
    # Mapa de palavras reservadas
    # Isso garante que "dispositivos" seja lido como token DISPOSITIVOS e não como ID
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
        'AND': 'AND',
        'ligar': 'LIGAR',
        'desligar': 'DESLIGAR'
    }

    # Conjunto de tokens
    tokens = {
        ID, NUM, BOOL, MSG,
        OP_LOGIC, SETA,
        *keywords.values()
    }

    ignore = ' \t\r\n'
    ignore_comment = r'//.*'

    # Literais (IMPORTANTE: adicionei o '=')
    literals = { '[', ']', ':', ';', ',', '(', ')', '=' }

    OP_LOGIC = r'(>=|<=|==|!=|>|<)'
    SETA     = r'->'

    @_(r'True|False')
    def BOOL(self, t):
        t.value = (t.value == "True")
        return t

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[^"]*"')
    def MSG(self, t):
        t.value = t.value.strip('"')
        return t

    # Identificador Genérico
    # Captura o texto e verifica se é uma keyword. Se for, muda o tipo do token.
    @_(r'[a-zA-Z][a-zA-Z0-9_]*')
    def ID(self, t):
        t.type = self.keywords.get(t.value, 'ID')
        return t

    def error(self, t):
        print(f"Linha {t.lineno}: caractere ilegal '{t.value[0]}'")
        self.index += 1