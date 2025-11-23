# parser.py

"""
# além da gramática já inciada pelo prof, adicionei:
- aceitar sintaxe alternativa de EXECUTE usada nos exemplos (com e sem o "em")
- lidar com sensores não definidos (default = 0)
- EXPRESSÕES MAIS COMPLEXAS (parênteses, OR, etc.)
- blocos múltiplos após when
- melhorar ALERTA para aceitar várias concatenações (opcional)
"""

from sly import Parser
from obs_lexer import ObsLexer
import ast_nodes as ast


class ObsParser(Parser):
    # importa tokens do lexer
    tokens = ObsLexer.tokens

    # programa principal
    # um programa começa com a seção de dispositivos seguida dos comandos
    @_('dev_sec cmd_sec')
    def program(self, p):
        return ast.Program(p.dev_sec, p.cmd_sec)

    # seção de dispositivos
    @_('DISPOSITIVOS ":" dev_list FIMDISPOSITIVOS')
    def dev_sec(self, p):
        return p.dev_list

    @_('device dev_list')
    def dev_list(self, p):
        return [p.device] + p.dev_list

    @_('device')
    def dev_list(self, p):
        return [p.device]

    @_('ID_DEVICE')
    def device(self, p):
        return ast.Device(p.ID_DEVICE)

    @_('ID_DEVICE "[" ID_OBS "]"')
    def device(self, p):
        return ast.Device(p.ID_DEVICE, p.ID_OBS)

    # lista de comandos
    @_('cmd cmd_list')
    def cmd_list(self, p):
        return [p.cmd] + p.cmd_list

    @_('cmd')
    def cmd_list(self, p):
        return [p.cmd]

    @_('cmd_list')
    def cmd_sec(self, p):
        return p.cmd_list

    # comandos possíveis
    @_('attrib')
    def cmd(self, p):
        return p.attrib

    @_('obsact')
    def cmd(self, p):
        return p.obsact

    @_('act ";"')
    def cmd(self, p):
        return p.act

    # definicao de atributos
    @_('DEF ID_OBS "=" val ";"')
    def attrib(self, p):
        return ast.AttributeDef(p.ID_OBS, p.val)

    # valores numéricos e booleanos
    @_('NUM')
    def val(self, p):
        return ast.Value(p.NUM)

    @_('BOOL')
    def val(self, p):
        return ast.Value(p.BOOL)

    # condições / observações
    # suportamos parenteses e encadeamento com AND
    @_('cond')
    def obs(self, p):
        return p.cond

    @_('cond AND obs')
    def obs(self, p):
        return ast.Condition(p.cond.left, p.cond.op, p.cond.right, p.obs)

    @_('ID_OBS OP_LOGIC val')
    def cond(self, p):
        return ast.Condition(p.ID_OBS, p.OP_LOGIC, p.val)

    @_('"(" obs ")"')
    def cond(self, p):
        return p.obs

    # estrutura "quando ... : ... senao ..."
    # suportamos blocos com várias ações
    @_('QUANDO obs ":" act_list')
    def obsact(self, p):
        return ast.WhenStmt(p.obs, p.act_list)

    @_('QUANDO obs ":" act_list SENAO act_list')
    def obsact(self, p):
        return ast.WhenStmt(p.obs, p.act_list0, p.act_list1)

    # bloco de ações dentro do quando
    @_('act ";" act_list')
    def act_list(self, p):
        return [p.act] + p.act_list

    @_('act ";"')
    def act_list(self, p):
        return [p.act]

    # ações
    # inclui: execute, alerta, difundir

    # versão tradicional: execute ligar em dispositivo
    @_('EXECUTE action EM ID_DEVICE')
    def act(self, p):
        return ast.ExecuteAction(p.action, p.ID_DEVICE)

    # versão alternativa permitida pelos exemplos: execute ligar dispositivo
    @_('EXECUTE action ID_DEVICE')
    def act(self, p):
        return ast.ExecuteAction(p.action, p.ID_DEVICE)

    # alerta simples
    @_('ALERTA PARA ID_DEVICE ":" MSG')
    def act(self, p):
        return ast.AlertAction(p.ID_DEVICE, p.MSG)

    # alerta com lista de variáveis concatenadas
    @_('ALERTA PARA ID_DEVICE ":" MSG "," var_list')
    def act(self, p):
        # se houver apenas um id, tratamos como variável única
        if len(p.var_list) == 1:
            return ast.AlertAction(p.ID_DEVICE, p.MSG, p.var_list[0])
        # se houver várias, deixamos como lista para o translator tratar
        return ast.AlertAction(p.ID_DEVICE, p.MSG, p.var_list)

    # lista de variáveis para alerta
    @_('ID_OBS')
    def var_list(self, p):
        return [p.ID_OBS]

    @_('ID_OBS "," var_list')
    def var_list(self, p):
        return [p.ID_OBS] + p.var_list

    # difundir
    # formato: difundir : msg -> [ dispositivos ]
    # ou difundir : msg var -> [ dispositivos ]
    @_('DIFUNDIR ":" MSG SETA "[" dev_list_n "]"')
    def act(self, p):
        return ast.BroadcastAction(p.MSG, None, p.dev_list_n)

    @_('DIFUNDIR ":" MSG ID_OBS SETA "[" dev_list_n "]"')
    def act(self, p):
        return ast.BroadcastAction(p.MSG, p.ID_OBS, p.dev_list_n)

    # lista de dispositivos no difundir
    @_('ID_DEVICE')
    def dev_list_n(self, p):
        return [p.ID_DEVICE]

    @_('ID_DEVICE "," dev_list_n')
    def dev_list_n(self, p):
        return [p.ID_DEVICE] + p.dev_list_n

    # actions primitivas (ligar / desligar)
    # agora corretamente referenciadas via tokens LIGAR / DESLIGAR
    @_('LIGAR')
    def action(self, p):
        return "ligar"

    @_('DESLIGAR')
    def action(self, p):
        return "desligar"
