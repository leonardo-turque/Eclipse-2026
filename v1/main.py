import rcu

VELOCIDADE_BASE = -28
LIMIAR_PRETO = 1700
LIMIAR_BRANCO = 2300

KP = 0.04
KD = 0.005

erro_anterior = 0

def clamp(valor, minimo, maximo):
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor

def parar():
    rcu.SetMotor(1, 0)
    rcu.SetMotor(2, 0)

def line_follower():
    global erro_anterior

    cor_direito  = rcu.GetColorSensor(4, 4)
    cor_esquerdo = rcu.GetColorSensor(1, 4)
    ref_esquerdo = rcu.GetLightSensor(5)
    ref_direito  = rcu.GetLightSensor(8)

    # 1° PRIORIDADE — vermelho → para tudo
    if (cor_direito == 1 or cor_esquerdo == 1):
        parar()
        return

    # 2° PRIORIDADE — curva de 90°: sensor de ponta detecta linha
    if (ref_esquerdo < LIMIAR_PRETO and ref_direito >= LIMIAR_BRANCO):
        # ponta esquerda achou preto → curva fechada esquerda
        rcu.SetMotor(1, 35)
        rcu.SetMotor(2, -35)
        return

    if (ref_direito < LIMIAR_PRETO and ref_esquerdo >= LIMIAR_BRANCO):
        # ponta direita achou preto → curva fechada direita
        rcu.SetMotor(1, -35)
        rcu.SetMotor(2, 35)
        return

    # 3° PID — erro contínuo pelos sensores de reflexão
    erro = ref_esquerdo - ref_direito
    derivada = erro - erro_anterior
    erro_anterior = erro

    correcao = clamp((KP * erro) + (KD * derivada), -15, 15)

    motor1 = clamp(VELOCIDADE_BASE - correcao, -100, 100)
    motor2 = clamp(VELOCIDADE_BASE + correcao, -100, 100)

    rcu.SetMotor(1, int(motor1))
    rcu.SetMotor(2, int(motor2))

def task1():
    while True:
        rcu.SetLightSensorLed(5, 1)
        rcu.SetLightSensorLed(8, 1)
        rcu.Set3CLed(2, 7)
        rcu.SetDisplayVar(1, rcu.GetLightSensor(5), 0xFFE0, 0x0000)
        rcu.SetDisplayVar(2, rcu.GetLightSensor(8), 0xFFE0, 0x0000)
        rcu.SetDisplayVar(3, rcu.GetColorSensor(4, 4), 0xFFE0, 0x0000)
        rcu.SetDisplayVar(4, rcu.GetColorSensor(1, 4), 0xFFE0, 0x0000)
        line_follower()

task1()