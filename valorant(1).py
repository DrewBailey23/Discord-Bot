import random
NUMBER_OF_AGENTS = 20
AGENTS = ['Omen', 'Viper', 'Brimstone', 'Astra', 'Harbor', 'Raze', 'Reyna', 'Phoenix', 'Jett', 'Neon', 'Yoru', 'Skye', 'Sova', 'Breach', 'KAY/O', 'Fade', 'Sage', 'Killjoy', 'Chamber', 'Cypher']
Controller = [0, 1, 2, 3, 4]
Duelist = [5, 6, 7, 8, 9, 10]
Initiator = [11, 12, 13, 14, 15]
Sentinel = [16, 17, 18, 19]
def getRandomAgent(role = "") -> str:
  if role.__eq__(""):
    return AGENTS[random.randint(0, NUMBER_OF_AGENTS - 1)]
  elif 'controller' in str(role).lower():
    return AGENTS[random.randint(0, 4)]
  elif 'duelist' in str(role).lower():
    return AGENTS[random.randint(5, 10)]
  elif 'initiator' in str(role).lower():
    return AGENTS[random.randint(11, 15)]
  elif 'sentinel' in str(role).lower():
    return AGENTS[random.randint(16, 19)]
  return None