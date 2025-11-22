'''Contém classes como:

Program

DeviceDecl

AttributeDef

WhenStatement

ExecuteAction

AlertAction

BroadcastAction

Fica tudo organizado.'''

# ast_nodes.py

class Program:
    def __init__(self, devices, commands):
        self.devices = devices
        self.commands = commands

class Device:
    def __init__(self, name, obs=None):
        self.name = name
        self.obs = obs

class AttributeDef:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class WhenStmt:
    def __init__(self, condition, act_true, act_false=None):
        self.condition = condition
        self.act_true = act_true
        self.act_false = act_false

class ExecuteAction:
    def __init__(self, action, device):
        self.action = action
        self.device = device

class AlertAction:
    def __init__(self, device, msg, var=None):
        self.device = device
        self.msg = msg
        self.var = var

class BroadcastAction:
    def __init__(self, msg, var, dev_list):
        self.msg = msg
        self.var = var
        self.dev_list = dev_list

class Condition:
    def __init__(self, left, op, right, next_cond=None):
        self.left = left
        self.op = op
        self.right = right
        self.next_cond = next_cond  # chain with AND

class Value:
    def __init__(self, value):
        self.value = value
