'''Recebe a AST e gera código C.

Cria main()

Declara variáveis

Traduz comandos ObsAct → C

Gera chamadas para ligar, desligar, alerta, etc.

Concatena MSG e ID_OBS quando necessário.'''

# translator.py

def translate(program):
    c = []

    c.append('#include <stdio.h>')
    c.append('#include "runtime.c"\n')

    c.append("int main() {")

    # Declarar atributos
    for cmd in program.commands:
        from ast_nodes import AttributeDef
        if isinstance(cmd, AttributeDef):
            c.append(f"    int {cmd.name} = {cmd.value.value};")

    c.append("")

    # Traduzir comandos
    for cmd in program.commands:
        code = translate_cmd(cmd)
        if code:
            c.append("    " + code)

    c.append("    return 0;")
    c.append("}")
    return "\n".join(c)


def translate_cmd(cmd):
    from ast_nodes import ExecuteAction, AlertAction, BroadcastAction, WhenStmt

    if isinstance(cmd, ExecuteAction):
        return f'{cmd.action}("{cmd.device}");'

    if isinstance(cmd, AlertAction):
        if cmd.var:
            return f'alerta("{cmd.device}", "{cmd.msg}", {cmd.var});'
        return f'alerta("{cmd.device}", "{cmd.msg}");'

    if isinstance(cmd, BroadcastAction):
        calls = []
        for d in cmd.dev_list:
            if cmd.var:
                calls.append(f'alerta("{d}", "{cmd.msg}", {cmd.var});')
            else:
                calls.append(f'alerta("{d}", "{cmd.msg}");')
        return "\n    ".join(calls)

    if isinstance(cmd, WhenStmt):
        cond = translate_condition(cmd.condition)
        code = f"if ({cond}) {{\n        {translate_cmd(cmd.act_true)}\n    }}"
        if cmd.act_false:
            code += f" else {{\n        {translate_cmd(cmd.act_false)}\n    }}"
        return code

    return None


def translate_condition(cond):
    if cond.next_cond:
        return f"({cond.left} {cond.op} {cond.right.value}) && {translate_condition(cond.next_cond)}"
    return f"{cond.left} {cond.op} {cond.right.value}"
