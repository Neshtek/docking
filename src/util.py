import numpy as np
import sys
import os

def create_data_map(array):
#     start_time = time.time()
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    threshold = 3 * mad
    diff = np.abs(data - median)
    z = diff / mad if mad else 0.0
    outliers = np.nonzero(z > threshold)[0]
    
#     end_time = time.time()
#     print("Execution time: ", end_time - start_time,"secs")
    if len(outliers) == 0:
        return data
    else:
        return np.take(data, np.delete(np.arange(len(data)), outliers), axis=0)
    
def keyboard_shutdown():
    print('Interrupted\n')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == '__main__':
    pass
