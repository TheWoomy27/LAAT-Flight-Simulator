import math

app.background = rgb(51, 51, 51)

print("Controls:\nEnter - Toggle Engine\nSpace - Takeoff\nArrow Keys - Turn\nMouse Click - Fire Cannons")

# Sounds
Engine = Sound("cmu://584498/31329410/SW02_Vehicles_LAAT_EngineLoop_Drone_Close_02+(1).wav")
StartEngine = Sound("cmu://584498/31329425/SW02_Vehicles_LAAT_Animations_TakeOffAway_VAR_01.wav")
ShutdownEngine = Sound("cmu://584498/31329434/LAAT+Shutdown+6.wav")
TakeOff = Sound("cmu://584498/31329433/LAAT+Takeoff+4C.wav")
IdleEngine = Sound("cmu://584498/31329491/LAAT+ENG+1C.wav")
cannon1 = Sound("cmu://584498/31350347/LAAT+Cannon+-+01.MP3")
cannon2 = Sound("cmu://584498/31350349/LAAT+Cannon+-+02.MP3")
cannon3 = Sound("cmu://584498/31350351/LAAT+Cannon+-+03.MP3")
cannonSounds = [cannon1, cannon2, cannon3]

# Images
gunshipBackView = Image("cmu://584498/31329365/Screenshot+2024-07-04+151458.png", -25, 0)
gunshipTopView = Image("cmu://584498/31329422/Screenshot+2024-07-04+152500.png", 0, 220)
gunshipSideView = Image("cmu://584498/31329446/Screenshot+2024-07-04+152527.png", 200, 250)

app.angle = 0 
app.yaw = 0
app.pitch = 0
app.roll = 0
app.yawAcceleration = 0
app.pitchAcceleration = 0
app.normalizeYaw = False
app.normalizeRoll = True
app.stepsPerSecond = 200
app.flying = False
app.engineOn = False
app.takingOff = False
app.canTakeOff = False
app.landing = False
app.landing2 = False
app.shooting = False
app.steps = 0

def onStep():
    app.steps += 1
    if app.shooting:
        if app.steps % 100 == 0:
            for sound in cannonSounds:
                sound.pause()
            cannonSounds[randrange(1,3)].play(restart=True)
    
    if app.flying:
        
        if app.normalizeRoll:
            
            app.angle += random() / 50
            
            gunshipBackView.rotateAngle = math.sin(app.angle) * 5 + app.yaw
        
    if app.takingOff == True:
        app.pitch -= 0.04
        if app.pitch < -10:
            app.takingOff = False
            
    if app.landing == True and app.canTakeOff == False:
        # app.pitch += app.pitchAcceleration
        # if app.pitchAcceleration > 0.01:
        #     app.pitchAcceleration -= 0.000625
        app.pitch += 0.08
        if app.pitch > 10:
            app.landing = False
            app.landing2 = True
    elif app.landing2:
        if app.pitch > 0: 
            app.pitch -= 0.025
    
    if app.normalizeYaw:
        if app.yaw > 0:
            app.yaw -= 0.1
        elif app.yaw < 0:
            app.yaw += 0.1
        if 0 < app.yaw < 0.6 or -0.6 < app.yaw < 0:
            app.yaw = 0

    gunshipTopView.rotateAngle = app.yaw
    gunshipSideView.rotateAngle = app.pitch

def onMousePress(x, y):
    
    app.shooting = True
    for sound in cannonSounds:
        sound.pause()
    cannonSounds[randrange(0,3)].play(restart=True)

def onMouseRelease(x, y):
    app.shooting = False

def onKeyPress(key):
    
    if key == "enter":
        if app.engineOn == False:
            app.engineOn = True
            StartEngine.play()
            sleep(1)
            IdleEngine.play(loop=True)
            app.canTakeOff = True
        else:
            app.engineOn = False
            app.normalizeYaw = True
            app.canTakeOff = False
            app.flying = False
            ShutdownEngine.play()
            IdleEngine.pause()
            Engine.pause()
            app.pitchAcceleration = 0.06
            app.landing = True
            
    if key == "space" and app.canTakeOff == True:
        TakeOff.play()
        sleep(5)
        app.takingOff = True
        IdleEngine.pause()
        sleep(1)
        Engine.play(loop=True, restart = True)
        app.flying = True
        app.canTakeOff = False
    
def onKeyHold(keys):
    if app.flying:
        if "left" in keys:
            app.normalizeYaw = False
            app.yaw -= app.yawAcceleration
            if app.yawAcceleration < 0.1:
                app.yawAcceleration += 0.0005
        if "right" in keys:
            app.normalizeYaw = False
            app.yaw += app.yawAcceleration
            if app.yawAcceleration < 0.1:
                app.yawAcceleration += 0.0005
        if "up" in keys:
            pass
        if "down" in keys:
            pass

def onKeyRelease(key):
    app.normalizeYaw = True
    app.yawAcceleration = 0
