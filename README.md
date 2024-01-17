# LU2IN013
Projet Robot
import simpy

def process(env, name, resource):
    print(f"{name} arrive à l'instant {env.now}")
    
    with resource.request() as req:
        yield req
        
        print(f"{name} commence à utiliser la ressource à l'instant {env.now}")
        yield env.timeout(2)  # Simulation d'une utilisation de la ressource pendant 2 unités de temps
        
        print(f"{name} a terminé à l'instant {env.now}")

# Environnement de simulation
env = simpy.Environment()

# Resource partagée
resource = simpy.Resource(env, capacity=1)

# Création des processus
process1 = env.process(process(env, 'Process 1', resource))
process2 = env.process(process(env, 'Process 2', resource))

# Lancer la simulation
env.run(until=5)
