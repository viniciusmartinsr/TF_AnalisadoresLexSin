from sly import Lexer

class ObsLexer(Lexer):

    # tokens
    tokens = {
        ID_DEVICE, ID_OBS, NUM, BOOL, MSG,
        OP_LOGIC, AND,
        DEF, QUANDO, EXECUTE, EM, ALERTA, PARA,
        DIFUNDIR, SETA, FIMDISPOSITIVOS, DISPOSITIVOS,
        SENAO, LIGAR, DESLIGAR
    }

    # ignore all whitespace including NEWLINE
    ignore = ' \t\r\n'

    # ignore comments
    ignore_comment = r'//.*'

    # ---------------------------------------------------------
    # KEYWORDS (precedência ANTES dos identificadores)
    # ---------------------------------------------------------
    DISPOSITIVOS    = r'dispositivos'
    FIMDISPOSITIVOS = r'fimdispositivos'
    DEF             = r'def'
    QUANDO          = r'quando'
    EXECUTE         = r'execute'
    EM              = r'em'
    ALERTA          = r'alerta'
    PARA            = r'para'
    DIFUNDIR        = r'difundir'
    SENAO           = r'senao'
    AND             = r'AND'
    LIGAR           = r'ligar'
    DESLIGAR        = r'desligar'

    # ---------------------------------------------------------
    # OPERADORES E SÍMBOLOS
    # ---------------------------------------------------------
    OP_LOGIC = r'(>=|<=|==|!=|>|<)'
    SETA     = r'->'

    literals = { '[', ']', ':', ';', ',', '(', ')' }

    # ---------------------------------------------------------
    # VALORES
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # IDENTIFICADORES — ORDEM IMPORTA!
    # ---------------------------------------------------------

    # MAIS GERAL → vem ANTES
    @_(r'[A-Za-z][A-Za-z0-9_]*')
    def ID_OBS(self, t):
        return t

    # MAIS RESTRITIVO → vem DEPOIS
    @_(r'[A-Za-z]+')
    def ID_DEVICE(self, t):
        return t

    # ---------------------------------------------------------
    # ERRO LÉXICO
    # ---------------------------------------------------------
    def error(self, t):
        print(f"caractere ilegal: '{t.value[0]}'")
        self.index += 1
