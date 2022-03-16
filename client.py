import os, time, cv2, mediapipe, socket

from ursina import *

#kapcsolodas a szerverhez
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(),1515))

#game
HEIGHT = 1280
WIDTH = 962

app = Ursina()

    

bg = Entity(model='quad', texture='assets\BG', scale=36, z=1)
window.fullscreen = True
player = Animation('assets\player', collider='box', y=5)
ufo = Entity(model='cube', texture='assets\\ufo1', collider='box', scale=2, x=20, y=-10)

ufos = []
def newUfo():
    new = duplicate(ufo,y=-5+(5124*time.dt)%15)
    ufos.append(new)
    invoke(ufos, delay=1)

newUfo()
camera.orthographic = True
camera.fov = 20

def update():


    bejovo_adat = s.recv(256)
    adat = bejovo_adat.decode('utf-8').replace('[','').replace(']','').replace(' ','').strip().split(',')



    player.x = adat[0]
    player.y = adat[1]




    for ufo in ufos:

        ufo.x -= 4*time.dt
        touch = ufo.intersects()

        if touch.hit:
            ufos.remove(ufo)
            destroy(ufo)
            destroy(touch.entity)

    t = player.intersects()
    if adat[2] == 1:
        e = Entity(y=player.y, x=player.x+1, model='cube', scale=1, texture='assets\Bullet', collider='cube')

        e.animate_x(30,duration=2,curve=curve.linear )

        invoke(destroy, e, delay=2)

    if t.hit and t.entity.scale==2:
        quit()



app.run()