# Importando biblioteca que já vem no Raspberry Pi que ocntrola os pinos GPIO.
# Nomeia-se essa biblioteca como GPIO para facilitar a implementação.
import RPi.GPIO as GPIO

# Importando o módulo 'time' que trabalha com tarefas relacionadas a tempo.
import time

# Configurando o modo de acesso ao GPIO via BCM (Broadcom SOC Channel) - método de 
# numeração que identifica-se como o número após a nomeação do GPIO na placa.
GPIO.setmode(GPIO.BCM)

TRANSMISSOR = 20
RECEPTOR = 21

# Desabilita notificações.
GPIO.setwarnings(False)

# Transmissor como saída.
GPIO.setup(TRANSMISSOR, GPIO.OUT)
# Receptor como entrada.
GPIO.setup(RECEPTOR, GPIO.IN)


print("Sensor Ultrassônico")

# Função de rotina.
def distancia():
    # Colocando transmissor em nível 1 (high) por 0.000001 segundos.
    GPIO.output(TRANSMISSOR, 1)
    time.sleep(0.000001)
    
    # Desativando a saída - colocando transmissor no nível 0 (low).
    GPIO.output(TRANSMISSOR, 0)
    
    # Inicializando tempos.
    tempo_inicial = time.time()
    tempo_final = time.time()

    # Obtem tempo inicial.
    while GPIO.input(RECEPTOR) == 0:
        tempo_inicial = time.time()
    
    # Obtem tempo final.
    while GPIO.input(RECEPTOR) == 1:
        tempo_final = time.time()

    tempo_distancia = tempo_final - tempo_inicial

    # A distância é a velocidade (do som = 34300 cm/s) vezes o tempo.
    # A distância é dividida por 2 pois o tempo compreende a ida e volta do sinal.
    distancia = (tempo_distancia*34300)/2
    return distancia


try:
    while True:
        # Referencia a função de rotina dentro do loop infinito.
        print("Distancia = %.1f cm" % distancia())
        # Dorme por 1 segundo.
        time.sleep(1.0)

# Interrupção via teclado.
except KeyboardInterrupt:
    GPIO.cleanup()
