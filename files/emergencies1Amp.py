from math import sqrt, pow, inf
import pyhop

# Definicion del estado
state1 = pyhop.State('state1')

state1.loc = {'ambulance1': 'hospital1', 'ambulance2': 'hospital2', 'victim1': 'university'}
state1.need_stabilization = {'victim1': False}

state1.coordinates = {'hospital1': {'X': 10, 'Y': 10}, 'hospital2': {'X': 22, 'Y': 22},
                       'park': {'X': 14, 'Y': 14}, 'school': {'X': 5, 'Y': 5}, 'benimaclet': {'X': 8, 'Y': 8},
                      'square': {'X': 0, 'Y': 0}, 'commercialCenter': {'X': 20, 'Y': 20}, 'university': {'X': 18, 'Y': 18}}
state1.victims = {'victim1': {'name': 'Andrés', 'age': 52, 'gravity': 2}, 'victim2': {'name': 'Miguel', 'age': 28, 'gravity': 4}}
state1.hospitals = {'hospital1': {'name': 'La Paz', 'loc': 'hospital1'}, 'hospital2': {'name': 'Universitario', 'loc': 'hospital2'}}
state1.ambulances = {'ambulance1': {'name': 'HK47', 'maxGravity': 2}, 'ambulance2': {'name': 'C3PO', 'maxGravity': 1}}

# Definición del GOAL
goal1 = pyhop.Goal('goal1')
goal1.loc = {'victim1': 'hospital1', 'victim2': 'hospital2'}

# Definición de constantes
GRAVITY_LIMIT = 2


# Funciones de apoyo
def distance(c1, c2):
    x = pow(c1['X'] - c2['X'], 2)
    y = pow(c1['Y'] - c2['Y'], 2)
    return sqrt(x + y)

def select_ambulance(state, victim, dest):
    best = inf
    victimGravity = state.victims[victim]['gravity']
    for ambulance in state.ambulances.keys():
        ambulanceLocation = state.loc[ambulance]
        dist = distance(state.coordinates[ambulanceLocation], state.coordinates[dest])
        if dist < best and victimGravity >= state.ambulances[ambulance]['maxGravity']:
            closest_ambulance = ambulance
            best = dist

    return closest_ambulance


# Funciones para la implementación del sistema

def check_stabilization(state, victim):
    if state.victims[victim]['gravity'] <= GRAVITY_LIMIT:
        state.need_stabilization[victim] = True
    return state

def ride_to_victim(state, ambulance, dest):
    if  state.loc[ambulance] != dest:
        state.loc[ambulance] = dest
        return state
    else:
        return False
    
def stabilize_victim(state, victim):
    state.need_stabilization[victim] = False
    return state
    
def load_ambulance(state, ambulance, victim):
    if state.loc[ambulance] ==  state.loc[victim] and not state.need_stabilization[victim]:
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
    
pyhop.declare_operators(check_stabilization, ride_to_victim, stabilize_victim, load_ambulance, ride_ambulance, unload_ambulance)
print()
pyhop.print_operators()

# Definición de dos metodos para "stabilize_if_necessary". Solo uno de ellos se ejecutará
# como máximo. Deben devolver un conjunto de operadores/tareas (aunque sea vacío) o False
# si no se puede aplicar

def do_stabilize(state, ambulance, victim):
    if state.loc[ambulance] ==  state.loc[victim] and state.need_stabilization[victim]:
        return [('stabilize_victim', victim)]
    
    return False

def dont_stabilize(state, ambulance, victim):
    if state.loc[ambulance] ==  state.loc[victim] and  not state.need_stabilization[victim]:
        return []
    return False


# Indicamos cual es la descomposición de "stabilize_if_necessary"

pyhop.declare_methods('stabilize_if_necessary', do_stabilize, dont_stabilize)



# Definición de métodos para deliver_victim
def call_ambulance(state, goal):
    victim = list(goal.loc.keys())[0]
    victimLoc = state.loc[victim]
    victimDest = goal.loc[victim]
    ambulance = select_ambulance(state, victim, victimLoc)

    return [('check_stabilization', victim),
            ('ride_to_victim', ambulance, victimLoc),
            ('stabilize_if_necessary', ambulance, victim),
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

 


pyhop.pyhop(state1, [('deliver_victim', goal1)], verbose=3)
