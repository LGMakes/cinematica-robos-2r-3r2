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

# Inicializa modelo simbólico
t1_s, t2_s, l1_s, l2_s, f_x, f_y = modelo_cinematico_direto()

# ===================== MODBUS CLIENT =====================
c = ModbusClient(host=ESP32_IP, port=MODBUS_PORT, unit_id=UNIT_ID, auto_open=True)

def enviar_para_esp32(ang1, ang2):
    if not c.is_open and not c.open():
        print(f"Erro: Não conectou em {ESP32_IP}")
        return False

    # Arredonda e limita para os motores
    a1_envio = int(round(ang1))
    a2_envio = int(round(ang2))

    print(f"Enviando ao ESP32 -> B: {a1_envio}° | C: {a2_envio}°")
    
    if c.write_multiple_registers(0, [a1_envio, a2_envio]):
        time.sleep(0.05)
        return c.write_single_register(2, 1)
    return False

# ===================== CÁLCULOS DE CINEMÁTICA =====================

def calcular_inversa(x, y):
    dist = math.sqrt(x**2 + y**2)
    if dist > (L1_VAL + L2_VAL) or dist < 5.0:
        print("Erro: Fora de alcance!")
        return None, None

    # Lei dos cossenos para theta2
    cos_t2 = (x**2 + y**2 - L1_VAL**2 - L2_VAL**2) / (2 * L1_VAL * L2_VAL)
    cos_t2 = max(-1.0, min(1.0, cos_t2))
    t2_rad = math.acos(cos_t2)

    # Theta1
    t1_rad = math.atan2(y, x) - math.atan2(L2_VAL * math.sin(t2_rad), L1_VAL + L2_VAL * math.cos(t2_rad))
    
    return math.degrees(t1_rad), math.degrees(t2_rad)

def calcular_direta(ang1, ang2):
    r1, r2 = np.radians(ang1), np.radians(ang2)
    x_val = f_x.subs({t1_s: r1, t2_s: r2, l1_s: L1_VAL, l2_s: L2_VAL})
    y_val = f_y.subs({t1_s: r1, t2_s: r2, l1_s: L1_VAL, l2_s: L2_VAL})
    return float(x_val), float(y_val)

# ===================== INTERFACE PRINCIPAL =====================
def principal():
    print("\n--- Controle do Robô 2R ---")
    print("1 - Cinemática Direta (Ângulos -> X,Y)")
    print("2 - Cinemática Inversa (X,Y -> Ângulos)")
    opcao = input("Escolha: ")

    try:
        if opcao == '1':
            a1 = float(input("Ângulo Base (θ1): "))
            a2 = float(input("Ângulo Cotovelo (θ2): "))
            x, y = calcular_direta(a1, a2)
            print(f"Resultado -> Posição da ponta: X={x:.2f}, Y={y:.2f}")
            enviar_para_esp32(a1, a2)

        elif opcao == '2':
            px = float(input("Coordenada X desejada: "))
            py = float(input("Coordenada Y desejada: "))
            a1, a2 = calcular_inversa(px, py)
            if a1 is not None:
                print(f"Resultado -> Ângulos calculados: Base={a1:.2f}°, Cotovelo={a2:.2f}°")
                enviar_para_esp32(a1, a2)
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"Erro no processamento: {e}")

if __name__ == "__main__":
    print(f"Conecte-se ao WiFi: ESP32_ROBOT")
    while True:
        principal()
        if input("\nContinuar? (s/n): ").lower() == 'n':
            c.close()
            break
