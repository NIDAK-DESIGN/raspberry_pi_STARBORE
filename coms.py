# -*- coding: cp1252 -*-
#--------------------------------------------------------
# Proyecto: cnc
# Archivo : coms.py
# Cliente : vertimaq
# Fecha   : 27 Julio 2017
# Autor   : Carlos Olmo (colmo@altanur.com)
#
# Descripción: Módulo de comunicaciones entre App y cnc
#--------------------------------------------------------

import serial
import serialenum
import time
#from PySide.QtGui import *
from PySide.QtGui import QMessageBox

class Input():
    def __init__(self, name, sense, mask):
        self.name = name
        self.sense = sense
        self.mask = mask
        self.state = 0

    def __str__(self):
        tmps = "Input "+self.name+"\n"
        tmps += "Sense:"+str(self.sense)+", Mask:"+hex(self.mask)+", State:"+str(self.state)
        return tmps

class Output():
    def __init__(self, name, sense, mask):
        self.name = name
        self.sense = sense
        self.mask = mask
        self.state = 0

    def __str__(self):
        tmps = "Output "+self.name+"\n"
        tmps += "Sense:"+str(self.sense)+", Mask:"+hex(self.mask)+", State:"+str(self.state)

        return tmps
        
class Axis():
    def __init__(self, letter):
        self.letter = letter
        # Status
        self.position = 0.0
        self.prevPosition = 0.0
        # Motor tunning
        self.resolution = 17.32
        self.maxSpeed = 20000
        self.acceleration = 2000
        self.linear = True
        self.jogFastSpeed = 2000
        self.jogSlowSpeed = 1000
        self.stepOutput = Output('Step', 1, 0x0)
        self.dirOutput = Output('Dir', 1, 0x0)
        self.pulseWidth = 3
        self.dirWidth = 3
        self.encoder = 0.0
        # Home params
        self.homePos = 0.0
        self.homeSpeed = 10
        self.homeDir = 0
        self.homeSensor = Input('Home '+self.letter, 0, 0x0)

    def setPosition(self, pos):
        self.prevPosition = self.position
        self.position = pos

        if self.position > self.prevPosition:
            self.moving = 1
        else:
            if self.position < self.prevPosition:
                self.moving = -1
            else:
                self.moving = 0

    def __str__(self):
        tmps = "Axis "+self.letter+"\n"
        tmps += "Resolution:"+str(self.resolution)+"\n"
        tmps += "Home, pos:"+str(self.homePos)+"(mm), dir: "+str(self.homeDir)+", speed:"+str(self.homeSpeed)+"% sense:"+str(self.homeSensor.sense)+"\n"

        return tmps
            
class CNC():

    def __init__(self):
        self.reset = False
        ports = serialenum.enumerate()
        print(ports)

        self.port = 0
        for port in ports:
            try:
                if "USB" in port or "COM" in port:   # copdebug TODO: Detectar si es windows
                    print("Trying "+str(port))
                    self.port = serial.Serial(port, 115200, timeout=0, parity=serial.PARITY_NONE, rtscts=0)
                    self.port.flushInput()    
                    self.port.write(b"status\r")
                    line = self.port.readline()
                    print("l1 "+line)
                    line = self.port.readline()
                    print("l2 "+line)
                    fields = line.split(";")
                    if(len(fields) == 7):
                        # Este es nuestro puerto
                        break
                    else:
                        self.port.close()
            except:
                self.port.close()
            
        '''    
        if port != "":
            try:
                self.port = serial.Serial(port, 115200, timeout=200, parity=serial.PARITY_NONE, rtscts=0)
                #self.port.close()
            except:
                print("Error openening port")
        else:
            self.port = 0
        '''

        # Axis
        self.axis = []
        xAxis = Axis('X')
        yAxis = Axis('Y')
        zAxis = Axis('Z')
        aAxis = Axis('A')
        aAxis.Linear = False
        self.axis.append(xAxis)
        self.axis.append(yAxis)
        self.axis.append(zAxis)
        self.axis.append(aAxis)

        # Inputs
        self.inputs = []
        self.inputs.append(Input('INVERTER', 0, 0x10))
        self.inputs.append(Input('STOP', 0, 0x100))
        self.inputs.append(Input('DOOR', 0, 0x1000))
        self.inputs.append(Input('AIR', 0, 0x2000))
        self.inputs.append(Input('GREASE', 0, 0x4000))
        self.inputs.append(Input('START', 0, 0x8000))

        # Outputs
        self.outputs = []
        self.outputs.append(Output('FRESA', 0, 0x200))
        self.outputs.append(Output('PINZA', 0, 0x40))
        self.outputs.append(Output('BROCA', 0, 0x80))
        self.outputs.append(Output('GREASE', 0, 0x400))

        # Other settings
        self.spireDelay = 1
        self.drillDelay = 1
        self.spireEnabled = 0

        self.arcSysFactor = 100.0
        self.ledRef = 0
        self.mark = 1
        self.encoderTimeout = 2
        self.encoderError = 0.1

        self.avisoEngrase = 2
        self.intervaloEngrase = 10
        self.tiempoEngrase = 5
                            
        # Status
        self.mode = 0
        self.currentExecutionLine = 0

        # Alarms
        self.alarmDoor = 0
        self.alarmAir = 0
        self.alarmGrease = 0
        self.alarmStop = 0
        self.alarmLimits = 0
        self.alarmEncoder = 0
        self.alarmParser = 0
        self.alarmExec = 0
        self.alarmInverter = 0

        # Estado del referenciado
        self.referenced = False

        self.blockSending = False

    def readLine(self):
        tic = time.time()
        buff = self.port.read()

        #print(tic)
        while ((time.time() - tic) < 0.3) and (not '\n' in buff):
            buff += self.port.read()
            #print(buff)

        #print("Data read:"+buff)
        return buff
    
    def printStatus(self):
        print("Vertimaq CNC status report")
        print("Mode:"+str(self.mode))
        if self.referenced == True:
            print("Machine referenced")
        else:
            print("!!**  Machine NOT REFERENCED  **!!")
        print("Executing line:"+str(self.currentExecutionLine))
        for ax in self.axis:
            if ax.homeSensor.state == 1:
                homeSt = "ON"
            else:
                homeSt = "OFF"
                
            print("Axis "+ax.letter+", Position: "+str(ax.position)+" Speed: 100.2 Home sensor: "+homeSt)

        for output in self.outputs:
            print("Output "+output.name+": , status:"+str(output.state))

        for inp in self.inputs:
            print("Input "+inp.name+": , status:"+str(inp.state))

        tmps = "Alarmas: "
        if self.alarmDoor == 1:
            tmps += "Puerta,"
        if self.alarmAir == 1:
            tmps += "Aire,"
        if self.alarmGrease == 1:
            tmps += "Grasa,"
        if self.alarmStop == 1:
            tmps += "Stop,"
        if self.alarmLimits == 1:
            tmps += "Límites,"
        if self.alarmEncoder == 1:
            tmps += "Encoder,"
        if self.alarmParser == 1:
            tmps += "Parser,"
        if self.alarmExec == 1:
            tmps += "Ejecución,"
        if self.alarmInverter == 1:
            tmps += "Inverter,"
        print(tmps)

    def printConfig(self):
        print("Vertimaq CNC config report\n** Axis **\n")
        for ax in self.axis:
            print(ax)

        print("\n** Inputs **")
        for inp in self.inputs:
            print(inp)

        print("\n** Outputs **")
        for out in self.outputs:
            print(out)

        print("Use clamp as spindle:"+str(self.spireEnabled))
        print("Spindle delay:"+str(self.drillDelay))
        print("Spire delay:"+str(self.spireDelay))

        print("\n** General **")
        print("ArcSysFactor:"+str(self.arcSysFactor))
        print("Led Ref:"+str(self.ledRef))
        print("Encoder timeout:"+str(self.encoderTimeout))
        print("Encoder error:"+str(self.encoderError))

        print("Autogrease interval: " + str(self.autogreaseMinutes) + "min.")
        print("Autogrease time: " + str(self.autogreaseSeconds) + "seg.")

    def saveConfig(self, param, value):
        if self.port == 0:
            return

        if not self.port.isOpen():
            self.port.open()

        self.port.flushInput()
        self.port.flushOutput()
        print("config set "+param+" "+str(value)+"\n")
        self.port.write(b"config set "+param+" "+str(value)+"\r")
        self.readLine()
        
    def readConfig(self):
        if self.port == 0:
            return

        if not self.port.isOpen():
            self.port.open()

        self.port.flushInput()
        self.port.flushOutput()    
        self.port.write(b"config list\r")
        self.readLine()
        config = []
        tmps = ""
        while not "cnc:" in tmps:
            tmps = self.readLine()
            config.append( tmps )

        for line in config:

            if " = " in line:
                fields = line.split(" = ")
                value = fields[1]
                    
            if ".inputs." in line:
                if "StopActiveLow" in line:
                    self.inputs[1].sense = int(value)

                if "DoorActiveLow" in line:
                    self.inputs[2].sense = int(value)

                if "AirActiveLow" in line:
                    self.inputs[3].sense = int(value)

                if "GreaseActiveLow" in line:
                    self.inputs[4].sense = int(value)

                if "StartActiveLow" in line:
                    self.inputs[5].sense = int(value)

                if "InverterActiveLow" in line:
                    self.inputs[0].sense = int(value)

            # Salidas
            if ".outputs." in line:
                if "ClipActiveLow" in line:
                    # Mirar que salida es cada una
                    self.outputs[0].sense = int(value)

                if "ClampActiveLow" in line:
                    self.outputs[1].sense = int(value)

                if "DrillActiveLow" in line:
                    self.outputs[2].sense = int(value)

                if "spireDelay" in line:
                    self.spireDelay = int(value)

                if "spireEnabled" in line:
                    self.spireEnabled = int(value)

                if "DrillDelay" in line:
                    self.drillDelay = float(value)/10
                
            # System
            if ".system." in line:
                if "ArcSysFactor" in line:
                    self.arcSysFactor = float(value)

                if "LedRef" in line:
                    self.ledRef = int(value)

                if "Mark" in line:
                    self.mark = int(value)

            # Encoder
            if "EncoderTimeout" in line:
                self.encoderTimeout = int(value)
            else:
                if "EncoderErr" in line:
                    self.encoderError = float(value)

            # autogrease
            if "autogreaseMinutes" in line:
                self.autogreaseMinutes = int(value)

            if "autogreaseSeconds" in line:
                self.autogreaseSeconds = int(value)
            
            # Fixtures
            if ".fixture[" in line:
                pass
                
            # Axis
            if "axis[" in line:
                fields = line.split("[")
                nAxis = int(fields[1][0])
                fields = line.split(" = ")[0].split(".")
                param = fields[2]
                #print(line)
                #print("naxis:"+str(nAxis)+"param:"+param+" value:"+str(value))

                if param == "StepsByUnit":
                    self.axis[nAxis].resolution = float(value)

                if param == "Speed":
                    self.axis[nAxis].maxSpeed = int(value)

                if param == "Acceleration":
                    self.axis[nAxis].acceleration = int(value)

                if param == "Linial":
                    self.axis[nAxis].linear = int(value)

                if param == "JogSlowSpeed":
                    self.axis[nAxis].jogSlowSpeed = int(value)

                if param == "JogFastSpeed":
                    self.axis[nAxis].jogFastSpeed = int(value)

                if param == "StepActiveLow":
                    self.axis[nAxis].stepOutput.sense = int(value)

                if param == "DirActiveLow":
                    self.axis[nAxis].dirOutput.sense = int(value)

                if param == "Encoder":
                    self.axis[nAxis].encoder = float(value)
                    
                if param == "HomePosition":
                    self.axis[nAxis].homePos = float(value)

                if param == "HomeSpeed":
                    self.axis[nAxis].homeSpeed = int(value)

                if param == "HomeDir":
                    self.axis[nAxis].homeDir = int(value)

                if param == "HomeActiveLow":
                    self.axis[nAxis].homeSensor.sense = int(value)

                if param == "PulseWidth":
                    self.axis[nAxis].pulseWidth = int(value)

                if param == "DirectionWidth":
                    self.axis[nAxis].dirWidth = int(value)


        #print(config)

    def blocked(self):
        if self.blockSending == False:
            return False
        else:
            if self.blockTimes > 0:
                self.blockTimes -= 1
                return True
            else:
                return False
        
    def blockSend(self):
        self.blockSending = True
        self.blockTimes = 10

    def show_reset(self):
        print("RESET!!")
        import datetime
        ts = datetime.date.today().strftime("%B %d, %Y %H:%M")
        self.reset = True

        fdebug = open("reset.log","a")
        fdebug.write(ts + " reset\n")      
        fdebug.close()
        
        
    def send(self, data):
        if self.port == 0:
            return

        print("Sending:"+data)
        if not self.port.isOpen():
            self.port.open()

        # copdebug
        # depuracion de datos

        l = self.port.readline()
        if "VERTIMAQ CNC" in l:
            show_reset()
            
        #fdebug = open("debug.txt","a")
        while len(l) > 1:
            print("Rem:"+l)
            #fdebug.write("<<"+l)
            l = self.port.readline()
            #self.show_reset();
                
            
        
        #fdebug.close()
   

        #self.port.flushInput()
        #self.port.flushOutput()

        self.port.write(data)
        #time.sleep(1)
        #line = self.port.readline() # Eliminamos el eco
        #line = self.port.readline()

        #fdebug = open("debug.txt","a")
        #fdebug.write(">>"+data)      
        
        line0 = self.port.readline()
        print("Reply:"+line0)
        line = self.port.readline()
        print("Reply:"+line)
        #self.port.close()
        #fdebug.write("<<"+line0)
        #fdebug.write("<<"+line)
        #fdebug.close()

    def isInteger(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False
        
    def close(self):
        if self.port != 0:
            print("Closing port")
            self.port.close()

    def getErrors(self):
        if self.port == 0:
            return

        if not self.port.isOpen():
            self.port.open()

        self.port.flushInput()
        self.port.flushOutput()    
        self.port.write(b"errors\r")
        self.readLine()
        errors = []
        tmps = ""
        while not "Error list end" in tmps:
            tmps = self.readLine()
            errors.append( tmps )

        print(errors)
        
        return errors

    def getInfo(self):
        if self.port == 0:
            return

        if not self.port.isOpen():
            try:
                self.port.open()
            except:
                print("port closed, can't open")

        self.port.flushInput()

        try:
            self.port.write(b"info\r")
        except:
            print("-- error writing info --")
            self.port.close()
            try:
                self.port.open()
            except:
                print("port not found")

            return
        print("info reply")
        line = self.readLine()
        print(line)
        line = self.readLine()
        print(line)

        version = line.split(";")[0]
        machineTime = int(line.split(";")[1])
        machineSeconds = machineTime % 60
        machineTime /= 60
        machineMinutes = machineTime % 60
        machineHours = machineTime / 60
        machineStr = str(machineHours)+"h"+str(machineMinutes)+"m"+str(machineSeconds)+"s"
        return [version, machineStr]

    def getUUID(self):
        if self.port == 0:
            return

        if not self.port.isOpen():
            try:
                self.port.open()
            except:
                print("port closed, can't open")

        self.port.flushInput()

        try:
            self.port.write(b"uuid\r")
        except:
            print("-- error writing info --")
            self.port.close()
            try:
                self.port.open()
            except:
                print("port not found")

            return
        print("info reply")
        line = self.readLine()
        line = self.readLine()
        print(line)

        '''
        fdebug = open("debug.txt","a")
        fdebug.write(">>"+b"uuid\r")
        fdebug.write("<<"+line)
        fdebug.close()
        '''
        
        return line
    
    def readStatus(self):
        if self.port == 0:
            return

        if not self.port.isOpen():
            try:
                self.port.open()
            except:
                print("port closed, can't open")

        self.port.flushInput()
        #self.port.flushOutput()
        try:
            self.port.write(b"status\r")
        except:
            print("-- error writing --")
            self.port.close()
            try:
                self.port.open()
            except:
                print("port not found")
                #self.__init__()
            return
        #line = self.readLine()
        #print("L1:"+line)
        line = self.readLine()
        #print("L1:"+line)
        #self.port.close()
        line2 = self.readLine()
        #print("L2:"+line2)
        #line = self.readLine()

        if "VERTIMAQ CNC" in line or "VERTIMAQ CNC" in line2:
            self.show_reset()

        # copdebug
        fdebug = open("debug.txt","a")
        fdebug.write(">>"+b"status\r")
        fdebug.write("<<"+line)
        fdebug.write("<<"+line2)
        fdebug.close()
        if ";" in line2 and not ";" in line:
            line = line2
        #print(line)
        fields = line.split(";")
        if len(fields) < 6:
            print("******* Status info error ***************")
            print("Fields"+str(fields))
            print("lines:"+line+","+line2)
            return
        
        inputs = fields[0][0:4]
        #print("Inputs0.."+str(inputs))
        try:
            inputSt = int(inputs, 16)
        except ValueError:
            inputSt = 0

        '''    
        if self.isInteger(inputs):
            inputSt = int(inputs, 16)
        else:
            inputSt = 0
        '''
        
        #print("Inputs.."+hex(inputSt))
        cncSt = fields[0][4:6]

        #print(fields)
        currLine = fields[1]
        self.currentExecutionLine = currLine

        # Fijamos la posición de cada eje
        self.axis[0].setPosition( int(fields[2])/100.0 )
        self.axis[1].setPosition( int(fields[3])/100.0 )
        self.axis[2].setPosition( int(fields[4])/100.0 )
        self.axis[3].setPosition( int(fields[5])/100.0 )

        self.expectedPage = int(fields[7])
        
        # Alarmas
        self.alarms = int(fields[6], 16)
        #print("Alarmas:"+str(self.alarms))
        if self.alarms & 0x001:
            self.alarmDoor = 1
        else:
            self.alarmDoor = 0

        if self.alarms & 0x002:
            self.alarmAir = 1
        else:
            self.alarmAir = 0

        if self.alarms & 0x004:
            self.alarmGrease = 1
        else:
            self.alarmGrease = 0

        if self.alarms & 0x008:
            self.alarmStop = 1
        else:
            self.alarmStop = 0

        if self.alarms & 0x010:
            self.alarmLimits = 1
        else:
            self.alarmLimits = 0

        if self.alarms & 0x020:
            self.alarmEncoder = 1
        else:
            self.alarmEncoder = 0

        if self.alarms & 0x040:
            self.alarmParser = 1
        else:
            self.alarmParser = 0

        if self.alarms & 0x080:
            self.alarmExec = 1
        else:
            self.alarmExec = 0

        if self.alarms & 0x100:
            self.alarmInverter = 1
        else:
            self.alarmInverter = 0

        # rev20180102: Leemos el estado del referenciado
        if self.alarms & 0x800:
            self.referenced = True
        else:
            self.referenced = False
            
        # Fijamos los estados de las entradas
        # HOMES
        for i in range(0,4):
            if inputSt & (0x0001 << i):
                self.axis[i].homeSensor.state = 1
            else:
                self.axis[i].homeSensor.state = 0

        # Resto de inputs
        for i in range(0, 6):
            #print("Input "+str(i)+", name: "+self.inputs[i].name+", mask:"+hex(self.inputs[i].mask))
            if inputSt & self.inputs[i].mask:
                self.inputs[i].state = 1
            else:
                self.inputs[i].state = 0

        i = 0
        for out in self.outputs:
            #print("InputSt: "+hex(inputSt))
            if inputSt & out.mask:
                self.outputs[i].state = 1
            else:
                self.outputs[i].state = 0
            i += 1
                

        # status
        self.mode = int(cncSt)
        self.currentExecutionLine = int(currLine)


if __name__ == "__main__":        
    cnc = CNC()
    cnc.readStatus()
    cnc.printStatus()
    #cnc.printStatus()
    #cnc.send(b"start\r")
    #cnc.send(b"addpage 000106d1g1 x100 y100 f1000;g1 x0 y0;\r")
    #cnc.send(b"start\r")
    #cnc.send(b"addpage 0000081eg1 y1000 f10000;g1 z20 F3000;g1 a90\r")
    #cnc.readConfig()
    #cnc.printConfig()
    cnc.getUUID()
    
    #cnc.send(b"start\r")
    #cnc.send(b"addpage 00000ddcM601;G28 Z0;G28 Y0;G28 X0;G28 A0;G01 Y-60 F20000;G01 Z-110;M600;\r")
    
    
    '''
    pages = []
    pages.append(b"addpage 000006d1g1 x100 y100 f1000;g1 x0 y0;\r")
    pages.append(b"addpage 000106d1g1 x100 y100 f1000;g1 x0 y0;\r")
    pages.append(b"addpage 000206d1g1 x100 y100 f1000;g1 x0 y0;\r")
    cnc.send(b"start\r")
    for p in pages:
        cnc.send(p)
        
        rem =cnc.readLine()
        rem2 =cnc.readLine()
        print("Reply:"+rem+","+rem2)
        while not "Ok" in rem2:
            cnc.send(p)
            rem =cnc.readLine()
            rem2 =cnc.readLine()
            print("Reply:"+rem+","+rem2)
    '''
            
    '''
    cnc.send(b"exec m3\r")
    time.sleep(1)
    cnc.send(b"exec g4 p1\r")
    time.sleep(1)
    cnc.send(b"exec m5\r")
    
    cnc.saveConfig("config.axis[0].StepsByUnit", 1.1)
    cnc.saveConfig("config.axis[1].StepsByUnit", 2.2)
    cnc.saveConfig("config.axis[2].StepsByUnit", 3.3)
    '''

    '''
    infile = open("config.txt","r")
    for line in infile:
        fields = line.split(" = ")
        if "." in fields[1]:
            cnc.saveConfig(fields[0], float(fields[1]))
        else:
            if "True" in fields[1]:
                cnc.saveConfig(fields[0], 1)
            else:
                if "False" in fields[1]:
                    cnc.saveConfig(fields[0], 0)
                else:
                    cnc.saveConfig(fields[0], int(fields[1]))

    close(infile)
    '''
    
    cnc.readConfig()
    cnc.printConfig()
    cnc.close()
    
