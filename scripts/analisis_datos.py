import csv

# ============================================
# ANÁLISIS DE RESULTADOS DEPORTIVOS
# UTN - Tecnicatura en Programación 2026
# ============================================

# --- LECTURA DEL CSV ---
# Usamos DictReader para acceder a cada columna por nombre
# Esto es más claro que acceder por posición (fila[0], fila[1]...)
partidos = []
with open('datos/partidos.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        # DictReader lee todo como texto, por eso convertimos los goles a entero para poder hacer cuentas con ellos
        partidos.append({
            'fecha':            fila['fecha'],
            'equipo_local':     fila['equipo_local'],
            'equipo_visitante': fila['equipo_visitante'],
            'goles_local':      int(fila['goles_local']),
            'goles_visitante':  int(fila['goles_visitante'])
        })

print(f"Total de partidos cargados: {len(partidos)}")
print()

# --- INDICADOR 1: DETERMINAR GANADOR DE CADA PARTIDO ---
# Comparamos goles local vs visitante para saber el resultado
for partido in partidos:
    if partido['goles_local'] > partido['goles_visitante']:
        partido['ganador'] = partido['equipo_local']
    elif partido['goles_local'] < partido['goles_visitante']:
        partido['ganador'] = partido['equipo_visitante']
    else:
        partido['ganador'] = 'Empate'

# --- INDICADOR 2: OBTENER LISTA DE EQUIPOS SIN REPETIR ---
# Usamos un set porque automáticamente elimina duplicados
equipos = set()
for p in partidos:
    equipos.add(p['equipo_local'])
    equipos.add(p['equipo_visitante'])
equipos = list(equipos)

# --- INDICADOR 3: PARTIDOS GANADOS POR EQUIPO ---
# Iniciamos el contador en 0 para cada equipo
victorias = {}
for eq in equipos:
    victorias[eq] = 0

for p in partidos:
    if p['ganador'] != 'Empate':
        victorias[p['ganador']] += 1

# Convertimos el diccionario a lista de pares para poder ordenarlo
# Cada par es [equipo, cantidad_de_victorias]
lista_victorias = list(victorias.items())

# Ordenamos de mayor a menor usando bubble sort 
for i in range(len(lista_victorias)):
    for j in range(i + 1, len(lista_victorias)):
        if lista_victorias[j][1] > lista_victorias[i][1]:
            # Intercambiamos los dos elementos de lugar
            lista_victorias[i], lista_victorias[j] = lista_victorias[j], lista_victorias[i]

print("PARTIDOS GANADOS POR EQUIPO:")
for par in lista_victorias:
    equipo = par[0]
    cantidad = par[1]
    print(f"  {equipo}: {cantidad} victoria/s")

# --- INDICADOR 4: PROMEDIO DE GOLES POR PARTIDO ---
# Sumamos todos los goles del torneo y dividimos por partidos jugados
total_goles = 0
for p in partidos:
    total_goles += p['goles_local'] + p['goles_visitante']

promedio_goles = total_goles / len(partidos)
print(f"\nPROMEDIO DE GOLES POR PARTIDO: {promedio_goles:.2f}")

# --- INDICADOR 5: TABLA DE POSICIONES ---
# Sistema de puntuación oficial: 3 puntos victoria, 1 empate, 0 derrota
puntos = {}
for eq in equipos:
    puntos[eq] = 0

for p in partidos:
    if p['ganador'] == 'Empate':
        # En caso de empate ambos equipos suman 1 punto
        puntos[p['equipo_local']]     += 1
        puntos[p['equipo_visitante']] += 1
    else:
        # El ganador suma 3 puntos
        puntos[p['ganador']] += 3

# Convertimos a lista y ordenamos de mayor a menor puntaje
lista_puntos = list(puntos.items())

# Mismo ordenamiento bubble sort para los puntos
for i in range(len(lista_puntos)):
    for j in range(i + 1, len(lista_puntos)):
        if lista_puntos[j][1] > lista_puntos[i][1]:
            lista_puntos[i], lista_puntos[j] = lista_puntos[j], lista_puntos[i]

print("\nTABLA DE POSICIONES:")
print(f"{'POS':<5} {'EQUIPO':<20} {'PUNTOS':<10} {'VICTORIAS'}")
print("-" * 42)

posicion = 1
for par in lista_puntos:
    equipo = par[0]
    pts = par[1]
    print(f"{posicion:<5} {equipo:<20} {pts:<10} {victorias[equipo]}")
    posicion += 1

# --- GUARDAR TABLA EN CSV ---
# Usamos DictWriter para escribir con encabezados automáticos
# Definimos las columnas antes de escribir (fieldnames)
columnas = ['posicion', 'equipo', 'puntos', 'victorias']

with open('resultados/tabla_posiciones.csv', 'w', newline='', encoding='utf-8') as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()  # Escribe la fila de titulos automaticamente
    posicion = 1
    for par in lista_puntos:
        equipo = par[0]
        pts = par[1]
        escritor.writerow({
            'posicion': posicion,
            'equipo':   equipo,
            'puntos':   pts,
            'victorias': victorias[equipo]
        })
        posicion += 1

print("\nTabla guardada en resultados/tabla_posiciones.csv")
print("Analisis completado correctamente.")