import paramiko
import time
import json
import os
import shutil

os.system('clear')

print('###################################################')
print('      PROGRAMA PARA REALIZAR RESPALDOS  V3.0' )
print('ES MANDATORIO EJECUTARSE CON CUENTA DE SOLO LECTURA')
print('###################################################')

username = 'admin'
password = 'admin'

with open('devices.json', 'r') as f:
    equipos = json.load(f)
with open('commands.txt', 'r') as f:
    comandos = f.readlines()

tiempo_local = time.asctime(time.localtime(time.time()))
nombre_de_la_carpeta = "BAL_"+str(tiempo_local)
nombre_de_la_carpetaG = nombre_de_la_carpeta.replace(':','_')
directorio = "/home/alberto/PycharmProjects/untitled/AUTO/BAL/"+nombre_de_la_carpetaG
lista_down = []

try:
    os.mkdir(directorio)
except OSError:
    print("La creación del directorio %s falló" % directorio)
else:
    print("Se ha creado el directorio: %s " % directorio)

max_buffer = 999999

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

for equipo in equipos.keys():
    print('EQUIPO DE BAL: ', equipo)
    rep = os.system('ping -c 5 ' + equipos[equipo]['ip'])
    if rep == 0:
        outputFileName = equipo + str(tiempo_local) + '.txt'
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connection.connect(equipos[equipo]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
        new_connection = connection.invoke_shell()
        output = clear_buffer(new_connection)
        time.sleep(2)
        new_connection.send("ena\n")
        new_connection.send("netsupport\n")
        new_connection.send("terminal p 0\n")
        output = clear_buffer(new_connection)
        with open("/home/alberto/PycharmProjects/untitled/AUTO/BAL/"+str(nombre_de_la_carpetaG)+"/"+outputFileName, 'wb') as f:
            for comando in comandos:
                new_connection.send(comando)
                time.sleep(5)
                output = new_connection.recv(max_buffer)
                print(output)
                f.write(output)

        new_connection.close()
    else:
        print("Equipo is abajo", equipo)
        lista_down.append(equipo)

shutil.copytree('/home/alberto/PycharmProjects/untitled/AUTO/BAL/'+nombre_de_la_carpetaG,'/home/alberto/Documents/'+nombre_de_la_carpetaG)
os.system('clear')

print('#########################################################################################')
print('                                       SE HA FINALIZADO...')
print("Se ha creado el directorio:")
print(directorio)
print('Equipos que no se realizaron respaldos por que no respondieron por ping son:')
print(lista_down)
print('##########################################################################################')
