import pyhop

# Definicion del estado

state1 = pyhop.State('state1')

state1.loc = {'ambulance': 'school', 'victim': 'school'}

state1.coordinates = {'hospital1': {'X': 10, 'Y': 10}, 'hospital2': {'X': 22, 'Y': 22},
                       'park': {'X': 14, 'Y': 14}, 'school': {'X': 5, 'Y': 5}, 'benimaclet': {'X': 8, 'Y': 8},
                      'square': {'X': 0, 'Y': 0}, 'commercialCenter': {'X': 20, 'Y': 20}, 'university': {'X': 18, 'Y': 18}}
state1.victims = {'victim': {'name': 'Andrés', 'age': 52, 'gravity': 4}}
state1.hospitals = {'hospital1': {'name': 'La Paz', 'loc': 'hospital1'}, 'hospital2': {'name': 'Universitario', 'loc': 'hospital2'}}
state1.ambulances = {'ambulance': {'name': 'HK47', 'maxGravity': 2}}

# Definición del GOAL
goal1 = pyhop.Goal('goal1')
goal1.loc = {'victim': 'hospital1'}

# Funciones para la implementación del sistema
def call_ambulance(state, dest):
    if state.victims['victim']['gravity'] >= state.ambulances['ambulance']['maxGravity'] and state.loc['ambulance'] != dest:
        state.loc['ambulance'] = dest

    return state


def ride_ambulance(state, dest):
    if state.loc['victim'] ==  'in_ambulance':
        state.loc['ambulance'] = dest
        return state
    else:
        return False
    

def load_ambulance(state):
    if state.loc['ambulance'] ==  state.loc['victim']:
        state.loc['victim'] = 'in_ambulance'
        return state
    else:
        return False
    

def unload_ambulance(state, dest):
    if state.loc['victim'] ==  'in_ambulance' and state.loc['ambulance'] == dest:
        state.loc['victim'] = dest
        return state
    else:
        return False
    
pyhop.declare_operators(call_ambulance, ride_ambulance, load_ambulance, unload_ambulance)
print()
pyhop.print_operators()

# Definición de métodos para emergency

def deliver_victim(state, goal):
    return [('call_ambulance', state.loc['victim']),
            ('load_ambulance',),
            ('ride_ambulance', goal.loc['victim']),
            ('unload_ambulance', goal.loc['victim'])]

pyhop.declare_methods('deliver_victim', deliver_victim)
print()
pyhop.print_methods()

 


pyhop.pyhop(state1, [('deliver_victim', goal1)], verbose=3)
