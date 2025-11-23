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
        self.act_true = act_true     # lista de ações
        self.act_false = act_false   # lista de ações ou none


class ExecuteAction:
    def __init__(self, action, device):
        self.action = action
        self.device = device


class AlertAction:
    def __init__(self, device, msg, var=None):
        self.device = device
        self.msg = msg
        self.var = var   # pode ser string (id) ou lista


class BroadcastAction:
    def __init__(self, msg, var, dev_list):
        self.msg = msg
        self.var = var          # id_obs opcional
        self.dev_list = dev_list


class Condition:
    def __init__(self, left, op, right, next_cond=None):
        self.left = left
        self.op = op
        self.right = right
        self.next_cond = next_cond   # encadeamento com and


class Value:
    def __init__(self, value):
        self.value = value
