import json
import os
import MetaTrader5 as mt5

CAMINHO_LOGIN_SALVO = "login_salvo.json"

def salvar_login(server, login, password):
    dados = {
        "server": server,
        "login": login,
        "password": password
    }
    with open(CAMINHO_LOGIN_SALVO, "w") as f:
        json.dump(dados, f)

def carregar_login():
    if os.path.exists(CAMINHO_LOGIN_SALVO):
        with open(CAMINHO_LOGIN_SALVO, "r") as f:
            return json.load(f)
    return None

def conectar_mt5(server, login, password):
    if not mt5.initialize(server=server, login=int(login), password=password):
        return False
    return True

def verificar_conta_real():
    info = mt5.account_info()
    if info is None:
        return False
    return info.trade_mode == 0  # 0 = Conta Real

def obter_saldo():
    conta = mt5.account_info()
    if conta:
        return conta.balance
    return 0.0
