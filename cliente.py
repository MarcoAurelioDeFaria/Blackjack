# cliente.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_ip = simpledialog.askstring("Conectar", "Digite o IP do servidor:")
sala = simpledialog.askstring("Sala", "Digite o nome da sala:")
servidor_addr = (servidor_ip, 9999)
nome = simpledialog.askstring("Nome", "Digite seu nome:")
cliente.sendto(f"ENTRAR:{nome}:{sala}".encode(), servidor_addr)

mensagens = []
vitorias = 0
pontos = 0

def receber():
    global pontos, vitorias
    while True:
        try:
            msg, _ = cliente.recvfrom(1024)
            msg = msg.decode()
            if msg.startswith("CARTA:"):
                valor = int(msg.split(":")[1])
                pontos += valor
                mensagens.append(f"Você recebeu a carta: {valor}. Total: {pontos}")
            elif msg.startswith("RESULTADO:ganhou"):
                vitorias += 1
                mensagens.append("ocê venceu! Total de vitórias: " + str(vitorias))
            elif msg.startswith("RESULTADO:perdeu"):
                mensagens.append("Você perdeu!")
            else:
                mensagens.append(msg)
            atualizar_interface()
        except:
            break

root = tk.Tk()
root.title("Jogo 21 - Cliente")
texto = tk.Text(root, height=15, width=50)
texto.pack()

label_status = tk.Label(root, text=f"Vitórias: {vitorias} | Valor total das Cartas atuais: {pontos}")
label_status.pack()

def atualizar_interface():
    texto.delete("1.0", tk.END)
    for m in mensagens[-10:]:
        texto.insert(tk.END, m + "\n")
    label_status.config(text=f"Vitórias: {vitorias} | Pontos atuais: {pontos}")

def pedir_carta():
    cliente.sendto("PEDIR_CARTA".encode(), servidor_addr)

def parar():
    cliente.sendto("PARAR".encode(), servidor_addr)

def revanche():
    global pontos
    pontos = 0
    cliente.sendto("REVANCHE".encode(), servidor_addr)
    mensagens.append("🔁 Revanche solicitada!")
    atualizar_interface()

btn1 = tk.Button(root, text="Pedir Carta", command=pedir_carta)
btn1.pack()
btn2 = tk.Button(root, text="Parar", command=parar)
btn2.pack()
btn3 = tk.Button(root, text="Revanche", command=revanche)
btn3.pack()

threading.Thread(target=receber, daemon=True).start()
root.mainloop()
