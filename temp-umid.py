# Importando biblioteca que já vem no Raspberry Pi que ocntrola os pinos GPIO.
# Nomeia-se essa biblioteca como GPIO para facilitar a implementação.
import RPi.GPIO as GPIO

# Importando o módulo 'time' que trabalha com tarefas relacionadas a tempo.
import time

# Importando biblioteca espeak que lê a entrada e manda a saída para a caixa.
from espeak import espeak
# Importando biblioteca do sistema operacional.
import os


# Função de rotina que converte um número binário em decimal.
def bin2dec(string_num):
    return str(int(string_num, 2))


# Variável global que recebe os dados do sensor.
data = []

# Configurando o modo de acesso ao GPIO via BCM (Broadcom SOC Channel) - método de 
# numeração que identifica-se como o número após a nomeação do GPIO na placa.
GPIO.setmode(GPIO.BCM)

# Loop infinito.
while(True):
        
    # Se o array 'data' tiver um comprimento maior que 0, deleta qualquer informação que tiver
    # para inicializar uma nova leitura.  
    if(len(data) > 0):
        del data[0: len(data)]

    TRANSMISSOR = 4
    
    # Transmissor como saída.
    GPIO.setup(TRANSMISSOR, GPIO.OUT)

    # Coloca o transmissor em nível 1 (high) por 0.025 segundos, e em seguida
    # coloca o transmissor em nível 0 (low) por 0.02 segundos.
    GPIO.output(TRANSMISSOR, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(TRANSMISSOR, GPIO.LOW)
    time.sleep(0.02)
    
    # Transmissor como entrada,setando um resistor de pull-up. Um GPIO 'input' vai 
    # variar com valores entre 0 e 1 se não for conectado a nenhuma voltagem. Utilizando
    # um resistor pull-up o valor 'default' do input poderá ser setado. Normalmente, um 
    # resistor de 10K é utilizado entre o canal de entrada e 3,3V (pull-up).
    GPIO.setup(TRANSMISSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # Armazenando os dados lidos do transmissor na variavel global data.
    for i in range(0, 500):
        data.append(GPIO.input(4))


    # Declarando variáveis que vão receber os bits lidos.
    contBits = 0
    temp = 0
    count = 0
    bitUmidade = ""
    bitTemperatura = ""
    crc = ""


    try:
            while data[count] == 1:
                    temp = 1
                    count = count + 1

            for i in range(0, 32):
                    contBits = 0

                    while data[count] == 0:
                            temp = 1
                            count = count + 1

                    while data[count] == 1:
                            contBits = contBits + 1
                            count = count + 1

                    if contBits > 3:
                            if i >= 0 and i < 8:
                                    bitUmidade = bitUmidade + "1"
                            if i >= 16 and i < 24:
                                    bitTemperatura = bitTemperatura + "1"
                    else:
                            if i >= 0 and i < 8:
                                    bitUmidade = bitUmidade + "0"
                            if i >= 16 and i < 24:
                                    bitTemperatura = bitTemperatura + "0"

    except:
            # Caso corra algum erro:
            print("Erro nos bits.")

    # Verificação dos bit caso recebidos corretamente.
    try:
            for i in range(0, 8):
                    contBits = 0

                    while data[count] == 0:
                            temp = 1
                            count = count + 1

                    while data[count] == 1:
                            contBits = contBits + 1
                            count = count + 1

                    if contBits > 3:
                            crc = crc + "1"
                    else:
                            crc = crc + "0"

        except:
            # Caso corra algum erro:
            print("Erro nos bits.")
 
 
# Conversão de binário para inteiro.
    try:
        umidade = bin2dec(bitUmidade)
        temperatura = bin2dec(bitTemperatura)
 
        if int(umidade) + int(temperatura) - int(bin2dec(crc)) == 0:
                print "Umidade:"+ umidade +"%"
                print "Temperatura:"+ temperatura +" C"
 
                # parte do espeak (ignore caso não queira usar)-------------------------
                espeakfalaTemperatura ="A temperatura do Ambiente esta em torno de ", temperatura
                 
                os.system('espeak -vpt -s 160 "{0}"'.format(espeakfalaTemperatura))
                os.system('espeak -vpt -s 160 "{0}"'.format("Graus Celsius"))
                espeakfalaUmidade = " e a Umidade relativa do ar esta em torno de ",umidade
                os.system('espeak -vpt -s 160 "{0}"'.format(espeakfalaUmidade))
                os.system('espeak -vpt -s 160 "{0}"'.format("%"))
                # parte do espeak (ignore caso não queira usar)-------------------------
           
        # else:
                # print "ERR_CRC"
    except:
        # Caso corra algum erro:
            print("Erro na conversão.")
 
    time.sleep(10)
