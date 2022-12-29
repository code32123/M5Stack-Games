## Stops red in Pylint
import font_8x16#,font_16x32
disp = disp
display = display
buttons = buttons
##

i2c = I2C(scl=Pin(22), sda=Pin(21))

myimu = MPU6886(i2c)

AccelColor = display.colors.convertColor(255, 0, 0)
AccelDispScale = [-5, -5, 5]
AccelCalib = [0, 0, 0]
x,  y  = 0, 0

GyroColor  = display.colors.convertColor(0, 0, 255)
GyroDispScale  = [-5, -5, 5]
GyroCalib =  [0, 0, 0]
rx, ry = 0, 0


RotationStoreAccuracy = 100
RotationStoreColor  = display.colors.convertColor(0, 255, 0)
RotationStoreDispScale  = [-5, -5, 5]
RotationStore = [0, 0, 0]
rsy, rsx = 0, 0

PositionStoreAccuracy = 2
PositionStoreColor  = display.colors.convertColor(0, 255, 0)
PositionStoreDispScale  = [-5, -5, 5]
PositionStore = [0, 0, 0]
psy, psx = 0, 0

Undo_Color = display.colors.convertColor(0, 0, 0)

grid = [0, 0, 0]

oldAcceleration = [0, 0, 0]

def setLength(a, length, fill=' '):
    return (str(a) + (fill*length))[:length]
def formatPoint(a):
    return "(" + setLength(a[0], 10) + ", " + setLength(a[1], 10) + ", " + setLength(a[2], 10) + ")"
def formatText(A, G, R):
    return "A: " + formatPoint(A) + "  G: " + formatPoint(G) + "  R: " + formatPoint(R)

def avgPointList(listOfPoints):
    length = len(listOfPoints)
    pointSum = [0, 0, 0]
    pointAvg = [0, 0, 0]
    for point in listOfPoints:
        pointSum[0] += point[0]
        pointSum[1] += point[1]
        pointSum[2] += point[2]
    pointAvg[0] = pointSum[0]/length
    pointAvg[1] = pointSum[1]/length
    pointAvg[2] = pointSum[2]/length
    return pointAvg


buttonCReady = False
GyroCalibrationList = []

# stateEnum
class state:
    down = -1
    stop = 0
    up = 1
gestureState = [state.stop, state.stop, state.stop]
gestureLevels = [[1, 1], [1, 1], [1, 1]] # x+, x-, y+, x-, z+, z-
stillCounters = [0, 0, 0]
timeouts = [5, 5, 5]

while True:
    Raw_Accel = myimu.acceleration
    Raw_Gyro  = myimu.gyro

    Cal_Accel = [Raw_Accel[i] - AccelCalib[i] for i in range(len(Raw_Accel))]
    Cal_Gyro  = [Raw_Gyro[i]  - GyroCalib[i]  for i in range(len(Raw_Gyro))]

    RotationStore = [RotationStore[i] + (int(Cal_Gyro[i] *RotationStoreAccuracy)/RotationStoreAccuracy) for i in range(len(RotationStore))]
    PositionStore = [PositionStore[i] + (int(Cal_Accel[i]*PositionStoreAccuracy)) for i in range(len(PositionStore))]

    changeInAccel = [oldAcceleration[i] - Cal_Accel[i]  for i in range(len(Cal_Accel))]

    disp.vline(x, 0,   disp.Height, Undo_Color, setBaud=False)
    x   = (disp.Width /2) + (Cal_Accel[0] * AccelDispScale[0])
    disp.vline(x, 0,   disp.Height, AccelColor, setBaud=False)

    disp.hline(0, y,   disp.Width , Undo_Color, setBaud=False)
    y   = (disp.Height/2) + (Cal_Accel[1] * AccelDispScale[1])
    disp.hline(0, y,   disp.Width , AccelColor, setBaud=False)

    disp.vline(rx, 0,  disp.Height, Undo_Color, setBaud=False)
    rx  = (disp.Width /2) + (Cal_Gyro[1] * GyroDispScale[1])
    disp.vline(rx, 0,  disp.Height, GyroColor,  setBaud=False)

    disp.hline(0, ry,  disp.Width , Undo_Color, setBaud=False)
    ry  = (disp.Height/2) + (Cal_Gyro[0] * GyroDispScale[0])
    disp.hline(0, ry,  disp.Width , GyroColor,  setBaud=False)

    # disp.vline(rsx, 0, disp.Height, Undo_Color, setBaud=False)
    # rsx = (disp.Width /2) + (RotationStore[1] * RotationStoreDispScale[1])
    # disp.vline(rsx, 0, disp.Height, RotationStoreColor, setBaud=False)

    # disp.hline(0, rsy, disp.Width , Undo_Color, setBaud=False)
    # rsy = (disp.Height/2) + (RotationStore[0] * RotationStoreDispScale[0])
    # disp.hline(0, rsy, disp.Width , RotationStoreColor, setBaud=False)


    # disp.vline(psx, 0, disp.Height, Undo_Color, setBaud=False)
    # psx = (disp.Width /2) + (PositionStore[0] * PositionStoreDispScale[0])
    # disp.vline(psx, 0, disp.Height, PositionStoreColor, setBaud=False)

    # disp.hline(0, psy, disp.Width , Undo_Color, setBaud=False)
    # psy = (disp.Height/2) + (PositionStore[1] * PositionStoreDispScale[1])
    # disp.hline(0, psy, disp.Width , PositionStoreColor, setBaud=False)

    # disp.text(
    #     font_8x16,
    #     "Grid = " + str(grid),
    #     0,
    #     disp.Height-16,
    #     Undo_Color
    # )


    if Cal_Accel[0] >= gestureLevels[0][0]: # x+ (x up)
        stillCounters[0] = 0
        if gestureState[0] == state.up: # If already going up, do nothing
           pass
        elif gestureState[0] == state.stop: # If not doing anything, start going up
            gestureState[0] = state.up
            grid[0] += 1
        elif gestureState[0] == state.down: # If going down, count this as backlash and cancel
            gestureState[0] = state.stop
        
    elif Cal_Accel[0] <= -gestureLevels[0][1]: # x-
        stillCounters[0] = 0
        if gestureState[0] == state.up: # If going up, count this as backlash and cancel
            gestureState[0] = state.stop
        elif gestureState[0] == state.stop: # If not doing anything, start going down
            gestureState[0] = state.down
            grid[0] -= 1
        elif gestureState[0] == state.down: # If already going down, do nothing
            pass

    else:
        stillCounters[0] += 1
    if stillCounters[0] >= timeouts[0]:
        gestureState[0] = state.stop

    # if Cal_Accel[1] >= gestureLevels[2]: # y+
    #     grid[1] += 1
    # if Cal_Accel[1] <= -gestureLevels[3]: # y-
    #     grid[1] -= 1

    # if Cal_Accel[2] >= gestureLevels[4]: # z+
    #     grid[2] += 1
    # if Cal_Accel[2] <= -gestureLevels[5]: # z-
    #     grid[2] -= 1

    disp.text(
        font_8x16,
        "Grid = " + str(grid) + " "*5,
        0,
        disp.Height-16,
        display.colors.Green
    )

    oldAcceleration = Cal_Accel

    if abs(changeInAccel[0]) > 1 or abs(changeInAccel[1]) > 1 or abs(changeInAccel[2]) > 1:
        print(formatPoint(changeInAccel))

    # print(formatText(Cal_Accel, Cal_Gyro, RotationStore), gestureLevels, gestureState)
    # print("Acceleration:", formatPoint(Cal_Accel), "Gesture Triggers:", gestureLevels, "Gesture States:", gestureState, "Delay Counters:", stillCounters, "Change In Acceleration", formatPoint(changeInAccel))

    if buttons.buttons.getDown('A'):
        AccelCalib = Raw_Accel
        print("A","="*20,formatPoint(AccelCalib),"="*20)

    if buttons.buttons.getDown('B'):
        buttonCReady = True
        GyroCalibrationList.append(Raw_Gyro)
    else:
        if buttonCReady:
            GyroCalib = avgPointList(GyroCalibrationList)
            buttonCReady = False
            GyroCalibrationList = []
            print("G","="*20,formatPoint(GyroCalib),"="*20)


    if buttons.buttons.getDown('C'):
        RotationStore = [0, 0, 0]
        PositionStore = [0, 0, 0]

    if buttons.buttons.getDown(buttons.K_START):
        grid = [0, 0, 0]

    if buttons.buttons.getDown(buttons.K_UP):
        gestureLevels = [[x + 0.05 for x in l] for l in gestureLevels]

    if buttons.buttons.getDown(buttons.K_DOWN):
        gestureLevels = [[x - 0.05 for x in l] for l in gestureLevels]
