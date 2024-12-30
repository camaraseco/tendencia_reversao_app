# src/estrategia.py
from datetime import datetime
from src.utils import enviar_email

def verificar_stops(preco_atual, stop_loss, take_profit, operacao, usuario_email):
    """
    Verifica se uma operação atingiu Stop Loss ou Take Profit e executa a ação correspondente.

    Parâmetros:
        preco_atual (float): Preço atual do ativo.
        stop_loss (float): Nível de preço do Stop Loss.
        take_profit (float): Nível de preço do Take Profit.
        operacao (str): Tipo de operação ativa ('COMPRA' ou 'VENDA').
        usuario_email (str): Email do usuário para notificação.
    """
    if operacao == 'COMPRA':
        if preco_atual <= stop_loss:
            motivo = 'Stop Loss'
            executar_operacao(preco_atual, 'VENDA', motivo, usuario_email)
        elif preco_atual >= take_profit:
            motivo = 'Take Profit'
            executar_operacao(preco_atual, 'VENDA', motivo, usuario_email)
    elif operacao == 'VENDA':
        if preco_atual >= stop_loss:
            motivo = 'Stop Loss'
            executar_operacao(preco_atual, 'COMPRA', motivo, usuario_email)
        elif preco_atual <= take_profit:
            motivo = 'Take Profit'
            executar_operacao(preco_atual, 'COMPRA', motivo, usuario_email)

def executar_operacao(preco_execucao, tipo_operacao, motivo, usuario_email):
    """
    Executa a operação e envia uma notificação ao usuário.

    Parâmetros:
        preco_execucao (float): Preço em que a operação foi executada.
        tipo_operacao (str): Tipo de operação realizada ('COMPRA' ou 'VENDA').
        motivo (str): Motivo da operação ('Stop Loss' ou 'Take Profit').
        usuario_email (str): Email do usuário para notificação.
    """
    data_hora = datetime.now()
    # Aqui você pode integrar a lógica de registro no banco de dados.
    print(f"Operação realizada: {tipo_operacao} | Preço: {preco_execucao} | Motivo: {motivo} | Hora: {data_hora}")
    enviar_email(tipo_operacao, preco_execucao, motivo, data_hora, usuario_email)
