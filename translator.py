from ast_nodes import (
    ExecuteAction,
    AlertAction,
    BroadcastAction,
    WhenStmt,
    AttributeDef,
)


def translate(program):

    c = []

    # cabeçalhos básicos
    c.append('#include <stdio.h>')
    c.append('#include "runtime.c"\n')

    c.append("int main() {")

    # declarar variáveis definidas com def
    defined_vars = set()
    for cmd in program.commands:
        if isinstance(cmd, AttributeDef):
            defined_vars.add(cmd.name)
            c.append(f"    int {cmd.name} = {cmd.value.value};")

    # inicializar sensores não declarados (pdf exige valor 0)
    for dev in program.devices:
        if dev.obs and dev.obs not in defined_vars:
            c.append(f"    int {dev.obs} = 0;")

    c.append("")

    # traduz cada comando
    for cmd in program.commands:
        code = translate_cmd(cmd)
        if code:
            for line in code.split("\n"):
                c.append("    " + line)

    c.append("    return 0;")
    c.append("}")
    return "\n".join(c)



# traduz um comando único
def translate_cmd(cmd):

    if isinstance(cmd, ExecuteAction):
        return f'{cmd.action}("{cmd.device}");'

    if isinstance(cmd, AlertAction):

        # lista de variáveis
        if isinstance(cmd.var, list):
            calls = []
            for v in cmd.var:
                calls.append(f'alerta("{cmd.device}", "{cmd.msg}", {v});')
            return "\n".join(calls)

        # alerta com uma única variável
        if cmd.var:
            return f'alerta_var("{cmd.device}", "{cmd.msg}", {cmd.var});'

        # alerta simples
        return f'alerta("{cmd.device}", "{cmd.msg}");'

    if isinstance(cmd, BroadcastAction):
        calls = []
        for d in cmd.dev_list:
            if cmd.var:
                calls.append(f'alerta_var("{d}", "{cmd.msg}", {cmd.var});')
            else:
                calls.append(f'alerta("{d}", "{cmd.msg}");')
        return "\n".join(calls)

    if isinstance(cmd, WhenStmt):
        cond = translate_condition(cmd.condition)
        true_block = translate_act_list(cmd.act_true)
        code = f"if ({cond}) {{\n{true_block}\n    }}"

        if cmd.act_false:
            false_block = translate_act_list(cmd.act_false)
            code += f" else {{\n{false_block}\n    }}"

        return code

    return None



# traduz lista de ações
def translate_act_list(actions):
    lines = []
    for act in actions:
        translated = translate_cmd(act)
        for l in translated.split("\n"):
            lines.append(f"        {l}")
    return "\n".join(lines)


# traduz condição com encadeamento and
def translate_condition(cond):
    if cond.next_cond:
        return f"({cond.left} {cond.op} {cond.right.value}) && {translate_condition(cond.next_cond)}"
    return f"{cond.left} {cond.op} {cond.right.value}"
