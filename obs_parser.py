# obs_parser.py
from sly import Parser
from obs_lexer import ObsLexer
import ast_nodes as ast

class ObsParser(Parser):
    # Importa os tokens definidos no Lexer
    tokens = ObsLexer.tokens

    # ----------------------------------------------------------------------
    # PROGRAMA PRINCIPAL
    # ----------------------------------------------------------------------
    @_('dev_sec cmd_sec')
    def program(self, p):
        return ast.Program(p.dev_sec, p.cmd_sec)

    # ----------------------------------------------------------------------
    # SEÇÃO DE DISPOSITIVOS
    # ----------------------------------------------------------------------
    @_('DISPOSITIVOS ":" dev_list FIMDISPOSITIVOS')
    def dev_sec(self, p):
        return p.dev_list

    @_('device dev_list')
    def dev_list(self, p):
        return [p.device] + p.dev_list

    @_('device')
    def dev_list(self, p):
        return [p.device]

    # Regra unificada usando ID (o Lexer decide se é Device ou Obs pelo contexto)
    @_('ID')
    def device(self, p):
        return ast.Device(p.ID)

    @_('ID "[" ID "]"')
    def device(self, p):
        # p.ID0 é o nome do device, p.ID1 é o nome da variável observada
        return ast.Device(p.ID0, p.ID1)

    # ----------------------------------------------------------------------
    # SEÇÃO DE COMANDOS
    # ----------------------------------------------------------------------
    @_('cmd cmd_list')
    def cmd_list(self, p):
        return [p.cmd] + p.cmd_list

    @_('cmd')
    def cmd_list(self, p):
        return [p.cmd]

    @_('cmd_list')
    def cmd_sec(self, p):
        return p.cmd_list

    @_('attrib')
    def cmd(self, p):
        return p.attrib

    @_('obsact')
    def cmd(self, p):
        return p.obsact

    @_('act ";"')
    def cmd(self, p):
        return p.act

    # ----------------------------------------------------------------------
    # DEFINIÇÃO DE ATRIBUTOS (def x = y;)
    # ----------------------------------------------------------------------
    @_('DEF ID "=" val ";"')
    def attrib(self, p):
        return ast.AttributeDef(p.ID, p.val)

    # Valores
    @_('NUM')
    def val(self, p):
        return ast.Value(p.NUM)

    @_('BOOL')
    def val(self, p):
        return ast.Value(p.BOOL)

    # ----------------------------------------------------------------------
    # CONDIÇÕES E OBSERVAÇÕES
    # ----------------------------------------------------------------------
    @_('cond')
    def obs(self, p):
        return p.cond

    @_('cond AND obs')
    def obs(self, p):
        return ast.Condition(p.cond.left, p.cond.op, p.cond.right, p.obs)

    @_('ID OP_LOGIC val')
    def cond(self, p):
        return ast.Condition(p.ID, p.OP_LOGIC, p.val)

    @_('"(" obs ")"')
    def cond(self, p):
        return p.obs

    # ----------------------------------------------------------------------
    # ESTRUTURA "QUANDO" (OBSACT)
    # ----------------------------------------------------------------------
    @_('QUANDO obs ":" act_list')
    def obsact(self, p):
        return ast.WhenStmt(p.obs, p.act_list)

    @_('QUANDO obs ":" act_list SENAO act_list')
    def obsact(self, p):
        # p.act_list0 é o bloco TRUE, p.act_list1 é o bloco FALSE (SENAO)
        return ast.WhenStmt(p.obs, p.act_list0, p.act_list1)

    # ----------------------------------------------------------------------
    # BLOCO DE AÇÕES (MODIFICADO PARA FLEXIBILIDADE DE ;)
    # ----------------------------------------------------------------------
    
    # 1. Ação com ; seguida de mais ações
    @_('act ";" act_list')
    def act_list(self, p):
        return [p.act] + p.act_list

    # 2. Ação SEM ; seguida de mais ações (Permite escrever em várias linhas sem ;)
    @_('act act_list')
    def act_list(self, p):
        return [p.act] + p.act_list

    # 3. Última ação com ;
    @_('act ";"')
    def act_list(self, p):
        return [p.act]

    # 4. Última ação SEM ; (Permite terminar bloco ou anteceder SENAO sem ;)
    @_('act')
    def act_list(self, p):
        return [p.act]

    # ----------------------------------------------------------------------
    # AÇÕES (ACT)
    # ----------------------------------------------------------------------
    
    # Execute (com e sem "em")
    @_('EXECUTE action EM ID')
    def act(self, p):
        return ast.ExecuteAction(p.action, p.ID)

    @_('EXECUTE action ID')
    def act(self, p):
        return ast.ExecuteAction(p.action, p.ID)

    # Alerta Simples
    @_('ALERTA PARA ID ":" MSG')
    def act(self, p):
        return ast.AlertAction(p.ID, p.MSG)

    # Alerta com Variáveis
    @_('ALERTA PARA ID ":" MSG "," var_list')
    def act(self, p):
        # Se var_list tiver só 1 item, manda o item. Se tiver mais, manda a lista.
        if len(p.var_list) == 1:
            return ast.AlertAction(p.ID, p.MSG, p.var_list[0])
        return ast.AlertAction(p.ID, p.MSG, p.var_list)

    # Lista de variáveis para o alerta
    @_('ID')
    def var_list(self, p):
        return [p.ID]

    @_('ID "," var_list')
    def var_list(self, p):
        return [p.ID] + p.var_list

    # Difundir
    @_('DIFUNDIR ":" MSG SETA "[" dev_list_n "]"')
    def act(self, p):
        return ast.BroadcastAction(p.MSG, None, p.dev_list_n)

    @_('DIFUNDIR ":" MSG ID SETA "[" dev_list_n "]"')
    def act(self, p):
        return ast.BroadcastAction(p.MSG, p.ID, p.dev_list_n)

    # Lista de dispositivos (usada no Difundir)
    @_('ID')
    def dev_list_n(self, p):
        return [p.ID]

    @_('ID "," dev_list_n')
    def dev_list_n(self, p):
        return [p.ID] + p.dev_list_n

    # Ações primitivas (ligar/desligar)
    @_('LIGAR')
    def action(self, p):
        return "ligar"

    @_('DESLIGAR')
    def action(self, p):
        return "desligar"