# Importando biblioteca que já vem no Raspberry Pi que ocntrola os pinos GPIO.
# Nomeia-se essa biblioteca como GPIO para facilitar a implementação.
import RPi.GPIO as GPIO

# Importando o módulo 'time' que trabalha com tarefas relacionadas a tempo.
import time

# Configurando o modo de acesso ao GPIO via BOARD - método de numeração que 
# identifica-se como o número impresso na placa/.
GPIO.setmode(GPIO.BOARD)

TRANSMISSOR = 11

# Transmissor como saída. servo1 as pin 11 as PWM
GPIO.setup(TRANSMISSOR, GPIO.OUT)

# Variável 'servo1' configira o transmissor também como uma saída PWM (Pulse 
# Width Modulation), inicializando-o com uma frequência aplicada na saída do 
# pino (50Hz).
servoMotor = GPIO.PWM(TRANSMISSOR, 50)

# Inicializando o sinal com um valor entre 0 a 100. Aqui, o sinal é igual a 0.
servoMotor.start(0)

print("Espera de 2 segundos...")
# Dormindo.
time.sleep(2)

# Let's move the servo!
print("Rotating 180 degrees in 10 steps")

# Variável 'duty' inicializada com valor 2.
duty = 2

# Loop para os valores de 'duty' de 2 a 12 (0 a 180 graus).
while duty <= 12:
    # Varia o valor do 'duty cycle' (ciclo de trabalho - proporção de tempo que
    # uma carga ou circuito de trabalho está ligado em comparação com o tempo em 
    # que a carga está desligada).
    servoMotor.ChangeDutyCycle(duty)
    
    # Dormindo.
    time.sleep(1)
    
    duty = duty + 1

# Dormindo.
time.sleep(2)

print("Voltando para 90° por 2 segundos.")
servoMotor.ChangeDutyCycle(7)
time.sleep(2)

print("Voltando para 0°.")
servoMotor.ChangeDutyCycle(2)
time.sleep(0.5)
servoMotor.ChangeDutyCycle(0)

# Para o servo motor.
servoMotor.stop()
GPIO.cleanup()