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

def ride_ambulance(state, victim, ambulance, source, dest):
    if state.loc[ambulance] == source and state.loc[victim] == source:
        state.loc[ambulance] = dest
        state.loc[victim] = dest
        return state
    else:
        return False
    
pyhop.declare_operators(call_ambulance, ride_ambulance)
print()
pyhop.print_operators()

# Definición de métodos para emergency

def emergency_method(ambulance, victim, source, dest):
    return [('call_ambulance', victim, ambulance, source), ('ride_ambulance', victim, ambulance, source, dest)]

pyhop.declare_methods('emergency_method', emergency_method)
print()
pyhop.print_methods()

def emergency_recursive(state, goal):
    if len(goal.loc) > 0:
        # solo nos interesa el primer goal
        for who in goal.loc.keys():
            x = state.loc[who]
            y = goal.loc.pop(who)  # extraemos (se elimina) el goal del diccionario
            break
        return [('emergency_method', who, x, y), ('travel', goal)]
    return []  # caso base: si len(goal.loc) == 0

# Indicamos cuál es la descomposición de "emergency"

pyhop.declare_methods('emergency', emergency_recursive)
print()
pyhop.print_methods()


pyhop.pyhop(state1, [('emergency', goal1)], verbose=1)
