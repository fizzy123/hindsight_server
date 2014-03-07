import math

from memories.models import Memory

def distance_calc(longitude, latitude, memory):
    return math.sqrt(math.pow(longitude-memory.longitude,2) + math.pow(latitude-memory.latitude,2))
