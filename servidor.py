# servidor.py
import socket
import threading
import random
import time

salas = {}  # chave: nome da sala, valor: dict com jogadores e estado

# Função para sortear carta
def sortear_carta():
    return random.randint(1, 11)

def enviar(para, msg):
    servidor.sendto(msg.encode(), para)

def registrar_log(msg):
    timestamp = time.strftime("%H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def nova_sala(nome_sala):
    salas[nome_sala] = {
        "jogadores": {},
        "ordem": [],
        "jogo_ativo": False,
        "turno": 0
    }

def proximo_turno(sala):
    sala_data = salas[sala]
    jogadores = sala_data['ordem']
    sala_data['turno'] = (sala_data['turno'] + 1) % len(jogadores)
    ativos = [j for j in jogadores if sala_data['jogadores'][j]['ativo'] and not sala_data['jogadores'][j]['parou']]

    if not ativos:
        fim_partida(sala)
    else:
        for i, addr in enumerate(jogadores):
            if i == sala_data['turno']:
                enviar(addr, "MENSAGEM: Sua vez.")
            else:
                enviar(addr, "MENSAGEM: Aguarde sua vez...")

def fim_partida(sala):
    sala_data = salas[sala]
    sala_data['jogo_ativo'] = False
    pontos = {addr: c['pontos'] if c['pontos'] <= 21 else 0 for addr, c in sala_data['jogadores'].items()}
    maior = max(pontos.values())
    for addr, p in pontos.items():
        if p == maior and maior > 0:
            enviar(addr, "RESULTADO:ganhou")
            registrar_log(f"{sala_data['jogadores'][addr]['nome']} venceu com {p} pontos na sala {sala}")
        else:
            enviar(addr, "RESULTADO:perdeu")

# Thread principal
def receber():
    while True:
        msg, addr = servidor.recvfrom(1024)
        msg = msg.decode()

        if msg.startswith("ENTRAR:"):
            _, nome, sala = msg.split(":")
            if sala not in salas:
                nova_sala(sala)

            dados_sala = salas[sala]
            if addr not in dados_sala['jogadores']:
                dados_sala['jogadores'][addr] = {"nome": nome, "pontos": 0, "parou": False, "ativo": True}
                dados_sala['ordem'].append(addr)
                enviar(addr, f"MENSAGEM: Entrou na sala {sala}. Esperando jogadores...")
                registrar_log(f"{nome} entrou na sala {sala}")

            if len(dados_sala['jogadores']) >= 1 and not dados_sala['jogo_ativo']:
                dados_sala['jogo_ativo'] = True
                enviar(dados_sala['ordem'][0], "MENSAGEM: Sua vez.")
                for i, j in enumerate(dados_sala['ordem']):
                    if i != 0:
                        enviar(j, "MENSAGEM: Aguarde sua vez...")

        elif msg == "PEDIR_CARTA":
            for sala, dados_sala in salas.items():
                if addr in dados_sala['jogadores'] and dados_sala['jogo_ativo'] and addr == dados_sala['ordem'][dados_sala['turno']]:
                    carta = sortear_carta()
                    dados_sala['jogadores'][addr]['pontos'] += carta
                    enviar(addr, f"CARTA:{carta}")
                    registrar_log(f"{dados_sala['jogadores'][addr]['nome']} tirou {carta} na sala {sala}")
                    if dados_sala['jogadores'][addr]['pontos'] > 21:
                        enviar(addr, "RESULTADO:perdeu")
                        dados_sala['jogadores'][addr]['ativo'] = False
                        proximo_turno(sala)

        elif msg == "PARAR":
            for sala, dados_sala in salas.items():
                if addr in dados_sala['jogadores'] and dados_sala['jogo_ativo'] and addr == dados_sala['ordem'][dados_sala['turno']]:
                    dados_sala['jogadores'][addr]['parou'] = True
                    registrar_log(f"{dados_sala['jogadores'][addr]['nome']} parou na sala {sala}")
                    proximo_turno(sala)

        elif msg == "REVANCHE":
            for sala, dados_sala in salas.items():
                if addr in dados_sala['jogadores']:
                    dados_sala['jogadores'][addr].update({"pontos": 0, "parou": False, "ativo": True})
                    if all(not j['parou'] and j['ativo'] for j in dados_sala['jogadores'].values()):
                        dados_sala['jogo_ativo'] = True
                        dados_sala['turno'] = 0
                        enviar(dados_sala['ordem'][0], "MENSAGEM: Nova rodada! Sua vez.")
                        for i, j in enumerate(dados_sala['ordem']):
                            if i != 0:
                                enviar(j, "MENSAGEM: Nova rodada! Aguarde sua vez...")

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("0.0.0.0", 9999))
threading.Thread(target=receber).start()
print("Servidor pronto na porta 9999")