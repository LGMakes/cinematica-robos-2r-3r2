import numpy as np
import sympy as sp
from pyModbusTCP.client import ModbusClient
import time
import math

# ===================== CONFIGURAÇÕES DE REDE =====================
ESP32_IP = "192.168.4.1"
MODBUS_PORT = 502
UNIT_ID = 1

# ===================== CONFIGURAÇÕES DO ROBÔ =====================
L1_VAL = 10.0  
L2_VAL = 10.0  

# ===================== MODELO CINEMÁTICO (DIRETA) =====================
def modelo_cinematico_direto():
    theta1, theta2 = sp.symbols('θ1 θ2')
    l1, l2 = sp.symbols('l1 l2')
    def dh_matrix(theta, length):
        return sp.Matrix([
            [sp.cos(theta), -sp.sin(theta), 0, length*sp.cos(theta)],
            [sp.sin(theta),  sp.cos(theta), 0, length*sp.sin(theta)],
            [0,              0,             1, 0                  ],
            [0,              0,             0, 1                  ]
        ])
    T = sp.simplify(dh_matrix(theta1, l1) * dh_matrix(theta2, l2))
    return theta1, theta2, l1, l2, T[0, 3], T[1, 3]

t1_s, t2_s, l1_s, l2_s, f_x, f_y = modelo_cinematico_direto()

# ===================== MODBUS CLIENT =====================
c = ModbusClient(host=ESP32_IP, port=MODBUS_PORT, unit_id=UNIT_ID, auto_open=True)

def enviar_para_esp32(ang1, ang2):
    """Envia os dados e aguarda a confirmação de que o ESP32 recebeu"""
    if not c.is_open and not c.open():
        print(f"Erro: Não conectou em {ESP32_IP}")
        return False
    
    a1_envio, a2_envio = int(round(ang1)), int(round(ang2))
    
    # 1. Escreve os ângulos
    if c.write_multiple_registers(0, [a1_envio, a2_envio]):
        # 2. Ativa o Trigger
        if c.write_single_register(2, 1):
            print(f"Comando enviado ({a1_envio}, {a2_envio}). Aguardando hardware aceitar...")
            
            # 3. ESPERA O TRIGGER VIRAR 1 (Confirmação de que o ESP32 viu o comando)
            # Isso impede que o Python pule para a verificação de fim antes do ESP32 começar
            for _ in range(20): 
                status = c.read_holding_registers(2, 1)
                if status and status[0] == 1:
                    return True
                time.sleep(0.1)
    return False

def esperar_movimento_fisico():
    """Aguarda o ESP32 avisar que os motores chegaram ao destino (Trigger = 0)"""
    print("Robô em movimento...")
    timeout = 40 
    inicio = time.time()
    
    # Pequena folga inicial para os motores saírem do repouso
    time.sleep(0.5) 

    while (time.time() - inicio) < timeout:
        status = c.read_holding_registers(2, 1)
        
        # Se o trigger voltou para 0, significa que distanceToGo() zerou no ESP32
        if status and status[0] == 0: 
            print("✔ Destino alcançado!")
            return True
            
        time.sleep(0.2)
        
    print("❌ Erro: O robô travou ou demorou demais.")
    return False

# ===================== CÁLCULOS =====================
def calcular_inversa(x, y):
    dist = math.sqrt(x**2 + y**2)
    if dist > (L1_VAL + L2_VAL) or dist < 2.0:
        return None, None
    cos_t2 = (x**2 + y**2 - L1_VAL**2 - L2_VAL**2) / (2 * L1_VAL * L2_VAL)
    cos_t2 = max(-1.0, min(1.0, cos_t2))
    t2_rad = math.acos(cos_t2)
    t1_rad = math.atan2(y, x) - math.atan2(L2_VAL * math.sin(t2_rad), L1_VAL + L2_VAL * math.cos(t2_rad))
    return math.degrees(t1_rad), math.degrees(t2_rad)

# ===================== PROCESSAMENTO =====================
def processar_pontos(lista_entradas, modo):
    try:
        numeros = lista_entradas.replace(',', ' ').split()
        if len(numeros) % 2 != 0:
            print("Erro: Use pares de valores.")
            return

        for i in range(0, len(numeros), 2):
            val1 = float(numeros[i])
            val2 = float(numeros[i+1])

            if modo == '1': # Direta
                if enviar_para_esp32(val1, val2):
                    esperar_movimento_fisico()
            else: # Inversa
                a1, a2 = calcular_inversa(val1, val2)
                if a1 is not None:
                    if enviar_para_esp32(a1, a2):
                        esperar_movimento_fisico()
            
            # Pausa extra entre pontos para estabilidade da rede
            time.sleep(1.0)

        print("\n🏁 Sequência concluída!")

    except Exception as e:
        print(f"Erro: {e}")

def principal():
    print("\n1 - Direta (T1 T2...) | 2 - Inversa (X Y...)")
    opcao = input("Opção: ")
    if opcao in ['1', '2']:
        pontos = input("Pontos: ")
        processar_pontos(pontos, opcao)

if __name__ == "__main__":
    while True:
        principal()
        if input("\nSair? (s/n): ").lower() == 's':
            c.close()
            break