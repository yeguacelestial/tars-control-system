import numpy as np
import skfuzzy as fuzzy

from skfuzzy import control as ctrl

# Variables de objetos Antecedentes/Consecuentes y funciones de membresia

# Entradas
angulo = ctrl.Antecedent(np.arange(0, 180, 1), 'angulo')
distancia = ctrl.Antecedent(np.arange(0, 150, 1), 'distancia')

# Salidas
velocidad = ctrl.Consequent(np.arange(0, 1000, 1), 'velocidad')

# Poblacion de la funcion de auto-membresia automf(3, 5 o 7)
angulo.automf(5)
distancia.automf(5)

# Funciones de membresia personalizadas
velocidad['very low'] = fuzzy.trapmf(velocidad.universe, [10,10,10,120])
velocidad['low'] = fuzzy.trapmf(velocidad.universe, [100, 150, 250, 300])
velocidad['high'] = fuzzy.trapmf(velocidad.universe, [200, 300, 500, 600])
velocidad['very high'] = fuzzy.trapmf(velocidad.universe, [500, 600, 700, 800])
velocidad['max high'] = fuzzy.trapmf(velocidad.universe, [700, 950, 950, 950])

# Reglas
# 1. IF angulo es poor AND distancia es poor THEN velocidad es very low
# 2. IF angulo es average AND distancia es poor THEN velocidad es low
# 3. IF angulo es good AND distancia es poor THEN velocidad es high
# 4. IF angulo es poor AND distancia es average THEN velocidad es low
# 5. IF angulo es average AND distancia es average THEN velocidad es high
# 6. IF angulo es good AND distancia es average THEN velocidad es very high
# 7. IF angulo es poor AND distancia es good THEN velocidad es very high
# 8. IF angulo es average AND distancia es good THEN velocidad es very high
# 9. IF angulo es good AND distancia es good THEN velocidad es max high

regla1 = ctrl.Rule(angulo['poor'] & distancia['poor'], velocidad['very low'])
regla2 = ctrl.Rule(angulo['average'] & distancia['poor'], velocidad['low'])
regla3 = ctrl.Rule(angulo['good'] & distancia['poor'], velocidad['high'])
regla4 = ctrl.Rule(angulo['poor'] & distancia['average'], velocidad['low'])
regla5 = ctrl.Rule(angulo['average'] & distancia['average'], velocidad['high'])
regla6 = ctrl.Rule(angulo['good'] & distancia['average'], velocidad['very high'])
regla7 = ctrl.Rule(angulo['poor'] & distancia['good'], velocidad['very high'])
regla8 = ctrl.Rule(angulo['average'] & distancia['good'], velocidad['very high'])
regla9 = ctrl.Rule(angulo['good'] & distancia['good'], velocidad['max high'])

# Creando el sistema de control...
arranque_ctrl = ctrl.ControlSystem([regla1,regla2,regla3,regla4,regla5,regla6,regla7,regla8,regla9])
arrancar = ctrl.ControlSystemSimulation(arranque_ctrl)

# Entradas para el sistema de control
entrada_angulo = 45
entrada_distancia = 60
arrancar.input['angulo'] = entrada_angulo
arrancar.input['distancia'] = entrada_distancia

# Juntar los numeros
arrancar.compute()

# Salida del sistema de control
salida_velocidad = round(arrancar.output['velocidad'], 2)

# Visualizar resultado
print(f'[*] Si TARS visualiza una montaña a {entrada_distancia}km en un angulo de {entrada_angulo}°, conduciría a {salida_velocidad}km/h.')
velocidad.view(sim=arrancar)