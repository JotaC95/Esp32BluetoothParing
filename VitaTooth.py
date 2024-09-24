import ubluetooth
import network
import time
from machine import Pin

# Inicialización del BLE
ble = ubluetooth.BLE()
ble.active(True)

# Definimos los UUID para las características BLE
SERVICE_UUID = ubluetooth.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
WIFI_CHAR_UUID = ubluetooth.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")

# Función para manejar las conexiones Bluetooth
def bt_irq(event, data):
    if event == 1:  # Dispositivo conectado
        print("Dispositivo conectado")
    elif event == 2:  # Dispositivo desconectado
        print("Dispositivo desconectado")

# Registro de servicio y característica
def ble_setup():
    wifi_char = (WIFI_CHAR_UUID, ubluetooth.FLAG_WRITE)
    BLEService = (SERVICE_UUID, (wifi_char,))
    ble.gatts_register_services((BLEService,))
    ble.gap_advertise(100, b'\x02\x01\x06\x03\x03\x09\x18')

# Función para conectarse a la red Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Esperar la conexión
    while not wlan.isconnected():
        print("Conectando...")
        time.sleep(1)
    print(f"Conectado a {ssid} con IP: {wlan.ifconfig()[0]}")

# Callback para manejar los datos escritos por Bluetooth
def ble_on_write(char_handle, data):
    value = data.decode()
    ssid, password = value.split(';')
    print(f"SSID: {ssid}, Password: {password}")
    connect_wifi(ssid, password)

# Inicializar el Bluetooth y el servicio
ble_setup()
ble.irq(bt_irq)

# Loop principal
while True:
    # Simular alguna acción que el ESP32 puede realizar
    time.sleep(1)