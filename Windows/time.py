from pywinauto import *
import time
from win32api import GetKeyState
import win32api
import psutil
import threading
#pip install pywinauto
#pip install win32api
#pip install psutil

print('WARNING: After setting Minecraft version, do not press anything other than the "Create New World" button.')
ver = input("Minecraft version (example: 1.20.1): ")
print(f"""Minecraft version set.
Game version: {ver}""")

#pro zjisteni PID procesu
pid=0
for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] == 'javaw.exe':
        pid = proc.info['pid']
print(f'Minecraft {ver} PID: {pid}')

#thread pro kontrolu ram a cpu
bench  = False
p = psutil.Process(pid)
def monitor():
    global p
    global bench
    global cpu
    global ram

    #pro nastaveni kontroly procesu (minecraft)
    cpu = []
    ram = []

    p.cpu_percent() / psutil.cpu_count()
    while bench:
        time.sleep(1)
        cpu.append(p.cpu_percent() / psutil.cpu_count())
        ram.append(p.memory_info().wset)

thread = threading.Thread(target=monitor)

#nula vyskoci když se hra v seznamu nenajde
if pid == 0:
    print("Game couldn't be found.")
    input("Press Enter to exit.")
    exit()

loop = True
win32api.GetAsyncKeyState(0x01)
win32api.GetAsyncKeyState(0x0D)
time.sleep(1)
print("Benchmark is ready to start.")
print("""   Press left mouse click to start
    Press Enter to abort""")
while loop:
    if win32api.GetAsyncKeyState(0x01) != 0:
        loop = False
        print("Benchmark has started.")
    elif win32api.GetAsyncKeyState(0x0D) != 0:
        print("Benchmark aborted")
        exit()

bench = True
thread.start()
start = time.time()

while bench:
    if findwindows.find_windows(title_re=f"Minecraft {ver} - Singleplayer") != []:
        bench  = False

end = time.time()
print("Done")
print("Fetching results...")
thread.join()
print(f'Avg. % of CPU used: {sum(cpu)/len(cpu)}')
print(f'Avg. kB of RAM used: {(sum(ram)/1000)/len(ram)}')
print(f'Time loading: {end - start}s.')