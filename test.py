import threading
import time

# Fonction exécutée par le thread
def mon_thread():
    while True:
        print("Thread en cours d'exécution...")
        time.sleep(1)

# Lancement du thread
t = threading.Thread(target=mon_thread)
t.start()

# Attente de 5 secondes
time.sleep(5)

# Arrêt du thread
t.kill()
print("Thread arrêté.")