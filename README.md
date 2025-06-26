# Blackjack

Jogo multiplayer de Blackjack (21) usando sockets UDP. Ele suporta múltiplos jogadores, várias salas, turnos controlados e interface gráfica com Tkinter.

## 🎯 Objetivo

Aplicar conceitos de redes, comunicação UDP e sincronização de múltiplos clientes em um jogo simples.

## 🚀 Como Rodar

1. **Pré-requisitos**:
   - Python 3
   - Tkinter (no Linux: `sudo apt install python3-tk`, no Windows é nativo)

2. **Rodar o Servidor**:

   - **No Linux**:
     ```
     python3 servidor.py
     ```

   - **No Windows**:
     ```
     python servidor.py
     ```

3. **Rodar o Cliente**:

   - **No Linux**:
     Abra outro terminal ou dispositivo e rode:
     ```
     python3 cliente.py
     ```

   - **No Windows**:
     Abra outro terminal ou dispositivo e rode:
     ```
     python cliente.py
     ```

   - Informe o IP do servidor (use `127.0.0.1` se for local)
   - Escolha um nome de jogador
   - Escolha o nome da sala (para jogar com outros)

## 🕹️ Como Jogar

- **Pedir Carta**: Recebe uma carta aleatória (1 a 11)
- **Parar**: Passa a vez
- **Revanche**: Reinicia uma nova rodada com os mesmos jogadores

## 📁 Estrutura

- **servidor.py**: Lógica do jogo, gerenciamento de salas e comunicação
- **cliente.py**: Interface gráfica do jogador
- **log.txt**: Registro das ações do servidor

## ✅ Funcionalidades

- Comunicação UDP
- Múltiplos jogadores e salas
- Interface gráfica (Tkinter)
- Registro de logs
- Revanche
- Controle de turnos

## 🧪 Testado em

- Linux Ubuntu 22.04
- Windows 10
