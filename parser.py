'''Implementa toda a gramática ObsAct do PDF (seção 1.1).
Gera objetos da AST a cada regra.

Usa SLY.Parser.'''

# parser.py
from sly import Parser
from lexer import ObsLexer
import ast_nodes as ast

class ObsParser(Parser):
    tokens = ObsLexer.tokens

    # Precedência (se precisar)
    precedence = ()

    # PROGRAM
    @_('DEV_SEC CMD_SEC')
    def PROGRAM(self, p):
        return ast.Program(p.DEV_SEC, p.CMD_SEC)

    # DEVICES
    @_('DISPOSITIVOS ":" DEV_LIST FIMDISPOSITIVOS')
    def DEV_SEC(self, p):
        return p.DEV_LIST

    @_('DEVICE DEV_LIST')
    def DEV_LIST(self, p):
        return [p.DEVICE] + p.DEV_LIST

    @_('DEVICE')
    def DEV_LIST(self, p):
        return [p.DEVICE]

    @_('ID_DEVICE')
    def DEVICE(self, p):
        return ast.Device(p.ID_DEVICE)

    @_('ID_DEVICE "[" ID_OBS "]"')
    def DEVICE(self, p):
        return ast.Device(p.ID_DEVICE, p.ID_OBS)

    # COMMANDS
    @_('CMD_LIST')
    def CMD_SEC(self, p):
        return p.CMD_LIST

    @_('CMD ";" CMD_LIST')
    def CMD_LIST(self, p):
        return [p.CMD] + p.CMD_LIST

    @_('CMD ";"')
    def CMD_LIST(self, p):
        return [p.CMD]

    # CMD
    @_('ATRRIB')
    def CMD(self, p):
        return p.ATRRIB

    @_('OBSACT')
    def CMD(self, p):
        return p.OBSACT

    @_('ACT')
    def CMD(self, p):
        return p.ACT

    # Atribuição: def temperatura = 40
    @_('DEF ID_OBS "=" VAL')
    def ATRRIB(self, p):
        return ast.AttributeDef(p.ID_OBS, p.VAL)

    # quando cond : act
    @_('QUANDO OBS ":" ACT')
    def OBSACT(self, p):
        return ast.WhenStmt(p.OBS, p.ACT)

    @_('QUANDO OBS ":" ACT SENAO ACT')
    def OBSACT(self, p):
        return ast.WhenStmt(p.OBS, p.ACT0, p.ACT1)

    # Condições
    @_('ID_OBS OP_LOGIC VAL')
    def OBS(self, p):
        return ast.Condition(p.ID_OBS, p.OP_LOGIC, p.VAL)

    @_('ID_OBS OP_LOGIC VAL AND OBS')
    def OBS(self, p):
        return ast.Condition(p.ID_OBS, p.OP_LOGIC, p.VAL, p.OBS)

    # VAL
    @_('NUM')
    def VAL(self, p):
        return ast.Value(p.NUM)

    @_('BOOL')
    def VAL(self, p):
        return ast.Value(p.BOOL)

    # ACT
    @_('EXECUTE ACTION EM ID_DEVICE')
    def ACT(self, p):
        return ast.ExecuteAction(p.ACTION, p.ID_DEVICE)

    @_('ALERTA PARA ID_DEVICE ":" MSG')
    def ACT(self, p):
        return ast.AlertAction(p.ID_DEVICE, p.MSG)

    @_('ALERTA PARA ID_DEVICE ":" MSG "," ID_OBS')
    def ACT(self, p):
        return ast.AlertAction(p.ID_DEVICE, p.MSG, p.ID_OBS)

    @_('DIFUNDIR ":" MSG SETA "[" DEV_LIST_N "]"')
    def ACT(self, p):
        return ast.BroadcastAction(p.MSG, None, p.DEV_LIST_N)

    @_('DIFUNDIR ":" MSG ID_OBS SETA "[" DEV_LIST_N "]"')
    def ACT(self, p):
        return ast.BroadcastAction(p.MSG, p.ID_OBS, p.DEV_LIST_N)

    @_('ID_DEVICE')
    def DEV_LIST_N(self, p):
        return [p.ID_DEVICE]

    @_('ID_DEVICE "," DEV_LIST_N')
    def DEV_LIST_N(self, p):
        return [p.ID_DEVICE] + p.DEV_LIST_N

    # ACTION: ligar | desligar
    @_('ACTION')
    def ACTION(self, p):
        return p.ACTION

    @_('"ligar"')
    def ACTION(self, p):
        return "ligar"

    @_('"desligar"')
    def ACTION(self, p):
        return "desligar"
