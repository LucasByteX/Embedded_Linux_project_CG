# Datalogger Industrial — BeagleBone Black

Projeto de Linux Embarcado desenvolvido para a disciplina TEC.1 — IFPB Campina Grande.

**Dupla:**
- Lucas Daris de Souza
- Arthur Henrique Siqueira Pantaleão

## Descrição

Sistema de datalogger de temperatura autônomo rodando em BeagleBone Black com Linux embarcado (Debian Trixie, kernel 6.19). O sistema lê a temperatura via sensor DS18B20 (protocolo 1-Wire), registra os dados em arquivo CSV e disponibiliza um dashboard web em tempo real.

## Componentes

- BeagleBone Black
- Sensor de temperatura DS18B20 (à prova d'água, protocolo 1-Wire)
- Shield TFT LCD 2.4" com leitor de cartão SD
- Resistor de 4.7kΩ (pull-up do barramento 1-Wire)

## Conexões

### Sensor DS18B20
| Fio | Pino BeagleBone |
|-----|----------------|
| Vermelho (VCC) | P9.3 (3.3V) |
| Preto (GND) | P9.1 |
| Amarelo (DATA) | P9.12 (GPIO60) |
| Resistor 4.7kΩ | Entre P9.3 e P9.12 |

### Cartão SD (SPI)
| Shield | BeagleBone |
|--------|-----------|
| SD_SS | P9.28 |
| SD_DI | P9.18 |
| SD_DO | P9.21 |
| SD_SCK | P9.22 |
| GND | P9.1 |
| 5V | P9.5 |
| 3V3 | P9.3 |

## Configuração do Sistema

### 1. Habilitar o sensor 1-Wire (overlay device tree)

```bash
cat > /tmp/w1.dts << 'EOF'
/dts-v1/;
/plugin/;
/ {
    compatible = "ti,beaglebone", "ti,beaglebone-black";
    fragment@0 {
        target-path = "/";
        __overlay__ {
            onewire0 {
                compatible = "w1-gpio";
                gpios = <&gpio1 28 0>;
                status = "okay";
            };
        };
    };
};
EOF
dtc -O dtb -o /tmp/w1.dtbo -b 0 -@ /tmp/w1.dts
sudo cp /tmp/w1.dtbo /boot/dtbs/$(uname -r)/overlays/
```

Adicionar ao `/boot/uEnv.txt`:
```
enable_uboot_overlays=1
uboot_overlay_addr0=/boot/dtbs/6.19.14-bone19/overlays/w1.dtbo
disable_uboot_overlay_video=1
```

### 2. Instalar dependências

```bash
pip3 install flask --break-system-packages
```

### 3. Executar o projeto

```bash
python3 /home/arthur/datalogger/app.py
```

Acesse o dashboard em: `http://[IP-DA-PLACA]:5000`

## Funcionalidades

- Leitura de temperatura a cada 2 segundos via DS18B20
- Registro automático em arquivo CSV com data/hora e flag de alarme
- Dashboard web com gráfico em tempo real
- Download do histórico CSV pelo navegador
- Configuração da temperatura de alarme pela interface web
- Detecção de sensor desconectado com alerta na interface

## Estrutura do Projeto

```
datalogger/
├── app.py          # Servidor Flask + loop principal
├── sensor.py       # Leitura do DS18B20 via 1-Wire
├── storage.py      # Gravação segura no CSV (fsync)
├── templates/
│   └── index.html  # Dashboard web
└── dados/
    └── temperaturas.csv  # Gerado em tempo de execução
```

## Tecnologias

- Python 3
- Flask (servidor web)
- Linux 1-Wire (w1-gpio, w1-therm)
- Device Tree Overlay (configuração do GPIO)
- HTML + Chart.js (dashboard)
