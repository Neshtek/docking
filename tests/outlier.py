import cv2
import numpy as np

import time    # this is an inbuilt library in Python

def create_data_map(array):
    start_time = time.time()
    outlier = []
    dict = {}
    mean_x = (np.average(array[0]))
    mean_y = (np.average(array[1]))

    center_p = np.array((mean_x, mean_y))

    for i in range(len(array[0])):
        point = np.array((array[0][i], array[1][i]))
        point_tuple = (array[0][i], array[1][i])
        distance = np.linalg.norm(center_p - point)
        data = {point_tuple: distance}
        dict.update(data)

    if len(dict) > 2:
        val_list = list(dict.values())
        key_list = list(dict.keys())
        mean = np.mean(val_list)
        sd = np.std(val_list)
        for i in range(len(val_list)):
            z = (val_list[i] - mean) / sd
            if z > 0.5 or z < -0.5:
                key = key_list[i]
                array[0].remove(key[0])
                array[1].remove(key[1])
                #print(key[0])
                #outlier.append(key)
                end_time = time.time()
                print("Execution time: ", end_time - start_time,"secs")
        #return outlier

def remove_outliers_mad(data):
    start_time = time.time()
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    threshold = 3 * mad
    diff = np.abs(data - median)
    z = diff / mad if mad else 0.0
    outliers = np.nonzero(z > threshold)[0]
    
    end_time = time.time()
    print("Execution time: ", end_time - start_time,"secs")
    if len(outliers) == 0:
        return data
    else:
        return np.take(data, np.delete(np.arange(len(data)), outliers), axis=0)


def create_data_map1(array):
    start_time = time.time()
    array = np.array(array)
    n = array.shape[1]
    center = np.mean(array, axis=1)
    distances = np.linalg.norm(array.T - center, axis=1)
    mean_distance = np.mean(distances)
    sd_distance = np.std(distances)
    z_scores = (distances - mean_distance) / sd_distance
    outliers = np.abs(z_scores) > 0.5
    array = array[:, ~outliers]
    # return array.tolist()


    end_time = time.time()
    print("Execution time: ", end_time - start_time,"secs")
        
    # return array


cap = cv2.VideoCapture(2)

while True:
    _, src = cap.read()

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower1 = np.array([0, 160, 100])  # S = 155, V = 84
    upper1 = np.array([5, 255, 255])  # 10

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([175, 160, 100])  # 160
    upper2 = np.array([179, 255, 255])

    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)

    full_mask = lower_mask + upper_mask

    # Threshold the HSV image to get only red colors
    color = cv2.bitwise_and(src, src, mask=full_mask)
    val = np.nonzero(color)
    copy = np.copy(color)
    avg_x = 0
    avg_y = 0

    x_axis = list(val[1])
    y_axis = list(val[0])
    data = [x_axis,y_axis]

    if len(x_axis) > 0:

        # Remove Outliers
        #outliers = createDataMap(data)


        #create_data_map(data)
        remove_outliers_mad(data)


        #if outliers is not None:
            #for i in range(len(outliers)):
            #    data[0].remove(outliers[i][0])
            #    data[1].remove(outliers[i][1])

            #for i in range(len(outliers)):
                #copy[outliers[i][1],outliers[i][0],0] = 0
                #copy[outliers[i][1],outliers[i][0],1] = 0
                #copy[outliers[i][1],outliers[i][0],2] = 0
        
            # Calculate centroids
        if len(data[0]) > 0:
            avg_x = int(round(np.average(data[0])))
            avg_y = int(round(np.average(data[1])))
            src = cv2.circle(src, (avg_x, avg_y), radius=10, color=(0, 255, 0), thickness=-1)

        cv2.imshow('Test', copy)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
