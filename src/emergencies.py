import pyhop

# Definicion del estado

state1 = pyhop.State('state1')

state1.loc = {'ambulance': 'hospital', 'victim': 'university'}

state1.coordinates = {'hospital': {'X': 10, 'Y': 10}, 'park': {'X': 14, 'Y': 14}, 'school': {'X': 5, 'Y': 5}, 'benimaclet': {'X': 8, 'Y': 8},
                      'square': {'X': 0, 'Y': 0}, 'commercialCenter': {'X': 20, 'Y': 20}, 'university': {'X': 18, 'Y': 18}}
state1.victims = {'victim': {'name': 'Andrés', 'age': 52, 'gravity': 5}}
state1.hospitals = {'hospital': {'name': 'The War', 'loc': 'hospital'}}
state1.ambulances = {'ambulance': {'name': 'Opel Corsa', 'maxGravity': 8}}

# Definición del GOAL
goal1 = pyhop.Goal('goal1')
goal1.loc = {'ambulance': 'hospital', 'victim': 'hospital'}

# Funciones para la implementación del sistema
def call_ambulance(state, victim, ambulance, dest):
    if state.victims[victim].gravity <= state.ambulances[ambulance].maxGravity:
        state.loc[ambulance] = dest
        return state
    else:
        return False
