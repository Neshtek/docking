import cv2

cap = cv2.VideoCapture(2)
while True:
    _, src = cap.read()
    cv2.imshow("OG", src)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()