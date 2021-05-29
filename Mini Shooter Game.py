from pygame import *
from random import *
from math import *


width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

running=True
gameRunning=[True]

bulletPos=[]
bulletRate=[]

hp=[100]
px,py=400,300

starttime=0
kills=[0]
times=[0]
lastShot=[-500]
shieldOn=[False]


once=[False]

mouse.set_visible(False)

def crosshair():
    draw.line(screen,GREEN,(mx-10,my),(mx+10,my),2)
    draw.line(screen,GREEN,(mx,my-10),(mx,my+10),2)


def checkKills():
    if kills[0]>=30:
        gameRunning[0]=False

def checkHealth():
    if hp[0]<=0:
        gameRunning[0]=False


def healthBar():
    draw.rect(screen,RED,(800-140,0,140,20))
    draw.rect(screen,GREEN,(800-140*hp[0]//100,0,140*hp[0]//100,20))
    
def displayBullet():
    for i in range(len(bulletPos)):
        if bulletPos[i]!=0:
            draw.circle(screen,YELLOW,(int(bulletPos[i][0]),int(bulletPos[i][1])),2)

def updateBullet():
    for i in range(len(bulletPos)):
        if bulletPos[i]!=0:
            bulletPos[i][0]+=bulletRate[i][0]*0.3
            bulletPos[i][1]+=bulletRate[i][1]*0.3

def createBullet():
    if time.get_ticks()>lastShot[0]+500:
        dx=mx-px
        dy=my-py
        bulletAngle=atan2(dy,dx)
        xratio=cos(bulletAngle)
        yratio=sin(bulletAngle)
        bulletPos.append([px,py])
        bulletRate.append([xratio,yratio])
        lastShot[0]=time.get_ticks()


def bulletCollision():
    for i in range(len(enemyPos)):
        for j in range(len(bulletPos)):
            if bulletPos[j]!=0 and enemyHP[i]>0:
                distance=sqrt((enemyPos[i][0]-bulletPos[j][0])**2+(enemyPos[i][1]-bulletPos[j][1])**2)
                if distance<=16:
                    bulletPos[j]=0
                    bulletRate[j]=0
                    enemyHP[i]-=5
                    if enemyHP[i]<=0:
                        kills[0]+=1



def shield():
    if 15000>=time.get_ticks()-starttime and times[0]<=3 and mb[2]==1:
        draw.circle(screen,BLUE,(int(px),int(py)),18,4)
        shieldOn[0]=True
    elif 15000<time.get_ticks()-starttime and times[0]<=3 and mb[2]==1:
        shieldOn[0]=False
        


def delBullet():
    for i in range(len(bulletPos)):
        if bulletPos[i]!=0:
            if bulletPos[i][0]<0 or bulletPos[i][0]>800 or bulletPos[i][1]<0 or bulletPos[i][1]>600:
                bulletPos[i]=0
                bulletRate[i]=0
######ENEMY############################
spawingTime=[-2900]
enemyPos=[]
enemyHP=[]
enemyBPos=[]
enemyBRate=[]
enemyLastShot=[]

def movingEnemy():
    for i in range(len(enemyPos)):
        if enemyPos[i]!=None:
            distance=sqrt((px-enemyPos[i][0])**2+(py-enemyPos[i][1])**2)
            if 150<distance:
                distX=px-enemyPos[i][0]
                distY=py-enemyPos[i][1]
                distAngle=atan2(distY,distX)
                ratioX=cos(distAngle)
                ratioY=sin(distAngle)
                enemyPos[i][0]+=ratioX*0.1
                enemyPos[i][1]+=ratioY*0.1
                
            elif 150>=distance:
                if time.get_ticks()>enemyLastShot[i]+2500:
                    distX=px-enemyPos[i][0]
                    distY=py-enemyPos[i][1]
                    distAngle=atan2(distY,distX)
                    ratioX=cos(distAngle)
                    ratioY=sin(distAngle)
                    if len(enemyBPos)<=i:
                        enemyBRate.append([ratioX,ratioY])
                        enemyBPos.append([enemyPos[i][0],enemyPos[i][1]])
                    else:
                        enemyBRate[i]=[ratioX,ratioY]
                        enemyBPos[i]=[enemyPos[i][0],enemyPos[i][1]]
                    enemyLastShot[i]=time.get_ticks()


def enemyBulletCollision():
    for i in range(len(enemyBPos)):
        if enemyBPos[i]!=0:
            distance=sqrt((px-enemyBPos[i][0])**2+(py-enemyBPos[i][1])**2)
            if distance<=18 and shieldOn[0]!=True:
                enemyBPos[i]=0
                enemyBPos[i]=0
                hp[0]-=5
            elif distance<=18 and shieldOn[0]==True:
                enemyBPos[i]=0
                enemyBPos[i]=0
            
def checkEnemyHealth():
    for i in range(len(enemyHP)):
        if enemyHP[i]<=0:
            enemyPos[i]=None



def delEnemyBullet():
    for i in range(len(enemyBPos)):
        if enemyBPos[i]!=0:
            if enemyBPos[i][0]<0 or enemyBPos[i][0]>800 or enemyBPos[i][1]<0 or enemyBPos[i][1]>600:
                enemyBPos[i]=0


def displayEnemy():
    for i in range(len(enemyPos)):
        if enemyPos[i]!=None:
            draw.circle(screen,RED,(int(enemyPos[i][0]),int(enemyPos[i][1])),14)
            draw.rect(screen,RED,(int(enemyPos[i][0])-14,int(enemyPos[i][1])-24,28,4))
            draw.rect(screen,GREEN,(int(enemyPos[i][0])-14,int(enemyPos[i][1])-24,int(28*(enemyHP[i]/20)),4))
            
def updateEnemyBullet():
    for i in range(len(enemyBPos)):
        if enemyBPos[i]!=0:
            enemyBPos[i][0]+=enemyBRate[i][0]*0.4
            enemyBPos[i][1]+=enemyBRate[i][1]*0.4

def displayEnemyBullet():
    for i in range(len(enemyBPos)):
        if enemyBPos[i]!=0:
            draw.circle(screen,YELLOW,(int(enemyBPos[i][0]),int(enemyBPos[i][1])),2)

def createEnemy():
    if time.get_ticks()>spawingTime[0]+2900:
        side=randint(0,3)
        enemyHP.append(20)
        if side==0:
            enemyPos.append([randint(10,790),10])
            enemyLastShot.append(1)
            spawingTime[0]=time.get_ticks()
        elif side==1:
            enemyPos.append([randint(10,790),590])
            enemyLastShot.append(1)
            spawingTime[0]=time.get_ticks()
        elif side==2:
            enemyPos.append([10,randint(10,590)])
            enemyLastShot.append(1)
            spawingTime[0]=time.get_ticks()
        elif side==3:
            enemyPos.append([790,randint(10,590)])
            enemyLastShot.append(1)
            spawingTime[0]=time.get_ticks()
init()
font.init()

display.set_caption("Mini Shooter Game")

winFont=font.SysFont("comicsansms", 72)
win = winFont.render('You Win!', True, GREEN)
winRect=win.get_rect() 
winRect.center = (800//2, 600//2)

loseFont=font.SysFont("comicsansms", 60)
lose = loseFont.render('You Are Dead, F in the chat!', True, GREEN)
loseRect=lose.get_rect() 
loseRect.center = (800//2, 600//2)

killFont=font.SysFont("comicsansms", 20)

healthFont=font.SysFont("comicsansms", 20)

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==3 and times[0]<=3:
                starttime=time.get_ticks()
                times[0]+=1
        if evt.type==MOUSEBUTTONUP:
            if evt.button==3:
                shieldOn[0]=False

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    keys=key.get_pressed()

    if keys[K_ESCAPE]:
        running=False


    screen.fill((200,200,200))


    if gameRunning[0]==True:
        #Player Movement
        if keys[97] and px>=16:
            px-=0.1
        if keys[100] and px<=800-16:
            px+=0.1
        if keys[119] and py>=16:
            py-=0.1
        if keys[115] and py<=600-16:
            py+=0.1

        

        kill=killFont.render(str(kills[0])+"/30 kills",True,GREEN)
        screen.blit(kill,(0,0))


        health=healthFont.render("Health: "+str(hp[0])+"/100",True,GREEN)
        screen.blit(health,(350,0))

        
        #Drawing Player
        healthBar()
        checkKills()
        checkHealth()
        draw.circle(screen,GREEN,(int(px),int(py)),16)
        shield()


        #Drawing Enemy
        createEnemy()
        displayEnemy()
        delEnemyBullet()
        movingEnemy()
        checkEnemyHealth()
        enemyBulletCollision()
        displayEnemyBullet()
        updateEnemyBullet()
        
        
        #Player Gun fire
        delBullet()
        if mb[0]==1:
            createBullet()
        bulletCollision()
        displayBullet()
        updateBullet()

        crosshair()
        
    elif gameRunning[0]==False:
        if kills[0]>=30:
            screen.blit(win, winRect)
        elif hp[0]<=0:
            screen.blit(lose, loseRect)
            if once[0]==False:
                print("Big F")
                once[0]=True
    

   
    display.flip()
            
quit()
