from math import sqrt, pow, inf
import pyhop

# Definicion del estado

state1 = pyhop.State('state1')

state1.loc = {'ambulance1': 'hospital1', 'ambulance2': 'benimaclet', 'victim1': 'university'}
state1.attend_victims = {'victim1': False}

state1.coordinates = {'hospital1': {'X': 10, 'Y': 10}, 'hospital2': {'X': 22, 'Y': 22},
                       'park': {'X': 14, 'Y': 14}, 'school': {'X': 5, 'Y': 5}, 'benimaclet': {'X': 8, 'Y': 8},
                      'square': {'X': 0, 'Y': 0}, 'commercialCenter': {'X': 20, 'Y': 20}, 'university': {'X': 18, 'Y': 18}}
state1.victims = {'victim1': {'name': 'Andrés', 'age': 52, 'gravity': 4}}
state1.hospitals = {'hospital1': {'name': 'La Paz', 'loc': 'hospital1'}, 'hospital2': {'name': 'Universitario', 'loc': 'hospital2'}}
state1.ambulances = {'ambulance1': {'name': 'HK47', 'maxGravity': 2}, 'ambulance2': {'name': 'C3PO', 'maxGravity': 3}}

# Definición del GOAL
goal1 = pyhop.Goal('goal1')
goal1.loc = {'victim1': 'hospital1'}


# Funciones de apoyo
def distance(c1, c2):
    x = pow(c1['X'] - c2['X'], 2)
    y = pow(c1['Y'] - c2['Y'], 2)
    return sqrt(x + y)

def select_ambulance(state, dest):
    best = inf
    for ambulance in state.ambulances.keys():
        ambulanceLocation = state.loc[ambulance]
        dist = distance(state.coordinates[ambulanceLocation], state.coordinates[dest])
        if dist < best:
            closest_ambulance = ambulance
            best = dist

    return closest_ambulance


# Funciones para la implementación del sistema

def ride_to_victim(state, ambulance, dest):
    if  state.loc[ambulance] != dest:
        state.loc[ambulance] = dest
        return state
    else:
        return False
    
def load_ambulance(state, ambulance, victim):
    if state.loc[ambulance] ==  state.loc[victim]:
        if state.victims[victim]['gravity'] > 3:
            state.attend_victims[victim] = True
        state.loc[victim] = ambulance
        return state
    else:
        return False
    
def ride_ambulance(state, ambulance, victim, dest):
    if state.loc[victim] ==  ambulance:
        state.loc[ambulance] = dest
        return state
    else:
        return False
    

def unload_ambulance(state, ambulance, victim, dest):
    if state.loc[victim] ==  ambulance and state.loc[ambulance] == dest:
        state.loc[victim] = dest
        return state
    else:
        return False
    
pyhop.declare_operators(ride_to_victim, ride_ambulance, load_ambulance, unload_ambulance)
print()
pyhop.print_operators()

# Definición de métodos para deliver_victim
def call_ambulance(state, goal):
    victim = list(goal.loc.keys())[0]
    victimLoc = state.loc[victim]
    victimDest = goal.loc[victim]
    ambulance = select_ambulance(state, victimLoc)
    return [('ride_to_victim', ambulance, victimLoc),
            ('load_ambulance', ambulance, victim), 
            ('ride_ambulance', ambulance, victim, victimDest), 
            ('unload_ambulance', ambulance, victim, victimDest)]

    
pyhop.declare_methods('call_ambulance', call_ambulance)
print()
pyhop.print_methods()

def deliver_victim(state, goal):
    return [('call_ambulance', goal)]

pyhop.declare_methods('deliver_victim', deliver_victim)
print()
pyhop.print_methods()

def emergency_recursive(state, goal):
    if len(goal.loc) > 0:
        # solo nos interesa el primer goal
        for who in goal.loc.keys():
            x = state.loc[who]
            y = goal.loc.pop(who)  # extraemos (se elimina) el goal del diccionario
            break
        return [('deliver_victim', who, x, y), ('emergency', goal)]
    return []  # caso base: si len(goal.loc) == 0

# Indicamos cuál es la descomposición de "emergency"

# pyhop.declare_methods('emergency', emergency_recursive)
# print()
# pyhop.print_methods()


pyhop.pyhop(state1, [('deliver_victim', goal1)], verbose=3)
