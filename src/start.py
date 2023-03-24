from .Rover import Rover
from src.dock import dock

def main_start(serial=None, connection=None):
    if serial != None:
        print(serial)
        rover = Rover(rover_serial=serial, connection=connection)
        dock(rover=rover)

if __name__ == '__main__':
    pass
else:
    main_start()