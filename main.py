#for i in {1..30}; do echo "Iteración $i" >> result.txt; iperf -c 192.168.135.54 -u -b 10M -n 10 -t 5 >> result.txt; echo "------------------------" >> result.txt; done

import matplotlib.pyplot as plt
import numpy as np

def parse_results(file_name):
    delays = []
    throughputs = []
    packet_losses = []

    with open(file_name, 'r') as f:
        for line in f:
            if "Delay:" in line:
                # Extraer el delay
                delay = float(line.split("Delay: ")[1].split(" ms")[0])
                delays.append(delay)
            if "Th:" in line:
                # Extraer el throughput
                th = float(line.split("Th: ")[1].split(" Mbits/sec")[0])
                throughputs.append(th)
            if "Pérdida de paquetes:" in line:
                # Extraer la pérdida de paquetes
                loss_info = line.split("Pérdida de paquetes: ")[1]
                lost, total = map(int, loss_info.split('/'))
                packet_loss_percentage = (lost / total) * 100
                packet_losses.append(packet_loss_percentage)

    return np.mean(delays), np.mean(throughputs), np.mean(packet_losses)

def main():
    # Archivos a procesar
    files = ['result2p.txt', 'result5p.txt', 'result10p.txt']
    labels = ['2 Mb', '5 Mb', '10 Mb']
    
    # Almacenar resultados
    delays = []
    throughputs = []
    packet_losses = []

    for file in files:
        delay, th, packet_loss = parse_results(file)
        delays.append(delay)
        throughputs.append(th)
        packet_losses.append(packet_loss)

    x = np.arange(len(labels))  # las posiciones en el eje x

    # Graficar Delay
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.bar(x, delays, color='blue', alpha=0.7)
    plt.xticks(x, labels)
    plt.ylabel('Delay (ms)')
    plt.title('Delay promedio por tamaño de paquete')

    # Graficar Throughput
    plt.subplot(3, 1, 2)
    plt.bar(x, throughputs, color='orange', alpha=0.7)
    plt.xticks(x, labels)
    plt.ylabel('Throughput (Mbits/sec)')
    plt.title('Throughput promedio por tamaño de paquete')

    # Graficar Pérdida de paquetes
    plt.subplot(3, 1, 3)
    plt.bar(x, packet_losses, color='red', alpha=0.7)
    plt.xticks(x, labels)
    plt.ylabel('Pérdida de paquetes (%)')
    plt.title('Pérdida de paquetes promedio por tamaño de paquete')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
