
from sly import Lexer

class ObsLexer(Lexer):

    # lista completa de tokens
    tokens = {
        ID_DEVICE, ID_OBS, NUM, BOOL, MSG,
        OP_LOGIC, AND,
        DEF, QUANDO, EXECUTE, EM, ALERTA, PARA,
        DIFUNDIR, SETA, FIMDISPOSITIVOS, DISPOSITIVOS,
        SENAO, LIGAR, DESLIGAR
    }

    # ignorar espaços, tabs e carriage return (\r)
    ignore = ' \t\r'

    # ignorar comentários // até o fim da linha
    ignore_comment = r'//.*'

    # ----------------------------------------------------------------------
    # palavras reservadas — sly prioriza estas regras ANTES de id_obs
    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    # operadores e símbolos
    # ----------------------------------------------------------------------
    OP_LOGIC = r'(>=|<=|==|!=|>|<)'
    SETA     = r'->'

    literals = { '[', ']', ':', ';', ',', '(', ')' }

    # ----------------------------------------------------------------------
    # valores básicos
    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    # identificadores
    # ----------------------------------------------------------------------
    # id_obs: letras, números e underline
    @_(r'[A-Za-z][A-Za-z0-9_]*')
    def ID_OBS(self, t):
        # palavras reservadas já foram tratadas acima automaticamente
        return t

    # id_device: somente letras
    @_(r'[A-Za-z]+')
    def ID_DEVICE(self, t):
        # palavras reservadas já foram tratadas acima automaticamente
        return t

    # ----------------------------------------------------------------------
    # erro léxico
    # ----------------------------------------------------------------------
    def error(self, t):
        print(f"caractere ilegal: '{t.value[0]}'")
        self.index += 1
