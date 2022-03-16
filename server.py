import cv2
import socket
import mediapipe as mp
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1515))
s.listen(2)
clientsocket, adress = s.accept()

HEIGHT = 1280
WIDTH = 962

CCONF = 30

cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils



while True:
    
    kimeno_adat = []
    pontlista = []
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    nincskez = True
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                if id == 4:
                    pontlista.append(cx)     # 0
                    pontlista.append(cy)     # 1
                    nincskez = False
                if id == 8:
                    pontlista.append(cx)     # 2
                    pontlista.append(cy)     # 3
                    nincskez = False               

                if id == 9:
                    kimeno_adat.append(cx)       #0
                    kimeno_adat.append(cy)       #1
                    nincskez = False
            
                
    if len(pontlista) != 0:
        if (pontlista[0]-pontlista[2] >= 0 and pontlista[0]-pontlista[2]) <= CCONF and (pontlista[1]-pontlista[3] >= 0 and pontlista[1]-pontlista[3]) <= CCONF:
            click = 1
            print('click')
        else:
            click = 0

        kimeno_adat.append(click)
            

    if clientsocket and nincskez == False:
        clientsocket.send(bytes(str(kimeno_adat), 'utf-8'))
    if clientsocket and nincskez:
        kimeno_adat = [0,0,0]



    #cv2.imshow('image', img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()