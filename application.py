#!usr/bin/python
import sys,time,threading
import Queue

from calibration import Ui_Calibration
from set_controls import Ui_SetControls
from main_page import Ui_MainPage
from monitor_params import Ui_MonitorParams
from comm_params import Ui_CommParams
from interlock_params import Ui_InterlockParams
from intropg import Ui_Intro
from circular_progress import QRoundProgressBar

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QObject, pyqtSignal
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

in_q = Queue.Queue()
out_q = Queue.Queue()

class ModbusComm(ModbusClient):
    def __init__(self):
        self.client = ModbusClient(method = "rtu", port='/dev/ttyAMA0',stopbits = 1, timeout = 0.1, bytesize = 8, parity = 'N', baudrate= 115200)
        self.client.connect()
        self.rt = threading.Thread(target=self.run,args=())
        self.rt.setDaemon(True)
        self.rt.start()

    def run(self):
        while True:
            try:
                if not out_q.empty():
                    self.data = out_q.get()
                self.rs = self.client.write_registers(0,self.data,unit=1)                    
                #print self.rs
            except:
                pass

            try:
                self.rr = self.client.read_holding_registers(0,17,unit=1)
                #print self.rr
                try:
                    in_q.put(self.rr.registers)
                except:
                    pass
            except:
                pass

            self.client.close()
            time.sleep(0.018)
            
class GuiThread(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            try:
                self.val_in = in_q.get()
                #print "Err"
            except:
                pass

            self.emit(QtCore.SIGNAL('datafrmbus'),self.val_in)
            

class MainWidget(QtGui.QWidget,QtCore.QObject):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.data_from_gui = [None]                                                #Data to the controller
       

    def initWidget(self):
        self.stack = QtGui.QStackedWidget()
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.stack)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
 
        self.stack.setStyleSheet("background-color: rgb(0,139,255);")

        self.intropg = Intropage_Gui()
        self.stack.addWidget(self.intropg)
       
        self.mainpg = MainPage_Gui()
        self.stack.addWidget(self.mainpg)

        self.monitorparams = MonitorParams_Gui()
        self.stack.addWidget(self.monitorparams)

        self.interlockparams = InterlockParams_Gui()
        self.stack.addWidget(self.interlockparams)

        self.setctrls = SetControl_Gui()
        self.stack.addWidget(self.setctrls)

        self.calib = Calib_Gui()
        self.stack.addWidget(self.calib)

        self.commparams = CommParams_Gui()
        self.stack.addWidget(self.commparams)

        self.stack.setCurrentWidget(self.intropg)
        QtCore.QTimer.singleShot(2000,self.run)                                 #Change the value of timer in final application code

        self.GuiThread = GuiThread()
	self.connect(self.GuiThread,QtCore.SIGNAL('datafrmbus'),self.datatodisplay)
	self.GuiThread.start()
        
        self.mainpg.sigMP.connect(self.displayMP)                               #Capturing Signal for Monitor Paramters 
	self.mainpg.sigIP.connect(self.displayIP)                               #Capturing Signal for Interlock Parameters
	self.mainpg.sigSC.connect(self.displaySC)                               #Capturing Singal for Set Controls
	self.mainpg.sigCP.connect(self.displayCP)                               #Capturing Signal for Communication Parameters
	self.mainpg.sigcalib.connect(self.displayCalib)                         #Capturing Signal for Calibration
	self.mainpg.sigexit.connect(QtCore.QCoreApplication.instance().quit)    #Capturing Signal for Exit 
        self.monitorparams.sigbackMP.connect(self.displaymainpg)                #Capturing Signal for Back on MP
        self.interlockparams.sigbackIP.connect(self.displaymainpg)              #Capturing Signal for Back on IP
        self.setctrls.sigbackSC.connect(self.displaymainpg)                     #Capturing Signal for Back on Set Controls
        self.calib.sigbackCalib.connect(self.displaymainpg)                     #Capturing Signal for Back on Calibration
        self.commparams.sigbackCP.connect(self.displaymainpg)                   #Capturing Signal for Save&Exit on Communication Parameters
        
    def run(self):
        self.stack.setCurrentWidget(self.mainpg)                                #Change the current widget to main page      
        self.mainpg.buttonevent()                                               #Calling method of Main Page Widget

    def datatodisplay(self,value):
        self.data_from_gui = []
        self.received_data = value
        print self.received_data
        self.data_to_IP = self.received_data[0:2]
        self.data_to_MP = self.received_data[6:11]
        self.data_to_calib = self.received_data[2:17] 
     
        self.MP_data = self.monitorparams.readData(self.data_to_MP)
        self.interlockparams.readData(self.data_to_IP)
        self.SC_data = self.setctrls.readData()
        if(self.SC_data[15] == 3):
            self.monitorparams.hmipot_IN.setEnabled(True)
            self.monitorparams.dial.setEnabled(True)

        self.calib_data = self.calib.readData(self.data_to_calib)
        self.CP_data = self.commparams.readData() 

        self.data_from_gui.append(1*1000)                                             #Hardcode value for power trip
        self.data_from_gui.append(1*1000)                                             #Hardcode value for voltage trip
        self.data_from_gui.append((self.SC_data[0]/self.calib_data[2])*1000)
        self.data_from_gui.append(1*1000)                                             #HardCode Value for freq trip
        self.data_from_gui.append((self.SC_data[1]/self.calib_data[4])*1000)
        self.data_from_gui.append((self.SC_data[2]/self.calib_data[5])*1000)
        self.data_from_gui.append((self.SC_data[3]/self.calib_data[0])*1000)
        self.data_from_gui.append((self.SC_data[4]/self.calib_data[1])*1000)
        self.data_from_gui.append((self.SC_data[5]/self.calib_data[2])*1000)
        self.data_from_gui.append((self.SC_data[6]/self.calib_data[3])*1000)
        self.data_from_gui.append((self.SC_data[7]/self.calib_data[4])*1000)
        self.data_from_gui.append((self.SC_data[8]/self.calib_data[5])*1000)
        self.data_from_gui.append((self.SC_data[9]/self.calib_data[0])*1000)
        self.data_from_gui.append((self.SC_data[10]/self.calib_data[1])*1000)
        self.data_from_gui.append((self.SC_data[11]/self.calib_data[2])*1000)
        self.data_from_gui.append((self.SC_data[12]/self.calib_data[3])*1000)
        self.data_from_gui.append((self.SC_data[13]/self.calib_data[4])*1000)
        self.data_from_gui.append((self.SC_data[14]/self.calib_data[5])*1000)
        self.data_from_gui.append((self.SC_data[15]*1)+1)
        self.data_from_gui.append((self.SC_data[16]*1)+1)
        if(self.SC_data[16] == 0):
            self.data_from_gui.append((self.MP_data[0]/self.calib_data[0])*1000)
        if(self.SC_data[16] == 1):
            self.data_from_gui.append((self.MP_data[0]/self.calib_data[1])*1000)
        if(self.SC_data[16] == 2):
            self.data_from_gui.append((self.MP_data[0]/self.calib_data[2])*1000)

        self.data_from_gui.append(self.MP_data[1]*1)
        self.data_from_gui.append(self.MP_data[2]*1)
        print self.data_from_gui
        if not out_q.full():
            out_q.put(self.data_from_gui)

    def displaymainpg(self):                                                    #Display Main Page
        self.stack.setCurrentWidget(self.mainpg)
        self.mainpg.buttonevent()

    def displayMP(self):                                                        #Display Monitor Parameters
        self.stack.setCurrentWidget(self.monitorparams)
		
    def displayIP(self):                                                        #Display Interlock Parameters
        self.stack.setCurrentWidget(self.interlockparams)
		
    def displaySC(self):                                                        #Display Set Controls
        self.stack.setCurrentWidget(self.setctrls)
		
    def displayCalib(self):                                                     #Display Calibration
        self.stack.setCurrentWidget(self.calib)
		
    def displayCP(self):                                                        #Display Communication Parameters
        self.stack.setCurrentWidget(self.commparams)
		
    #def displayExit(self):                                                      #Exit from Current Page
    

class Intropage_Gui(QtGui.QWidget,Ui_Intro):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)        

class MainPage_Gui(QtGui.QWidget,QtCore.QObject,Ui_MainPage):
    
    sigMP = QtCore.pyqtSignal()					                #PyQt Signal for Monitor Params
    sigIP = QtCore.pyqtSignal()					                #PyQt Signal for Interlock Params
    sigSC = QtCore.pyqtSignal()					                #PyQt Signal for Set Controls
    sigCP = QtCore.pyqtSignal()					                #PyQt Signal for Communication Parameters
    sigcalib = QtCore.pyqtSignal()				                #PyQt Siganl for Calibration
    sigexit = QtCore.pyqtSignal()				                #PyQt Signal for Exit

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)
        #palette = self.palette()
        #role = self.backgroundRole()
        #palette.setColor(role, QtGui.QColor('green'))
        #self.setPalette(palette)
        self.setStyleSheet("background-color:white;")
    
    def buttonevent(self):
        self.btn_monitorParams.clicked.connect(self.clickedMP)		        #Calling method for Monitor Parameter button press
        self.btn_interlockParams.clicked.connect(self.clickedIP)	        #Calling method for Interlock Parameter button press
        self.btn_setControls.clicked.connect(self.clickedSC)		        #Calling method for Set Controls button press
        self.btn_commParams.clicked.connect(self.clickedCP)		        #Calling method for Communication Parameter button press
        self.btn_calibration.clicked.connect(self.clickedCalib)		        #Calling method for Calibration button press
        self.btn_exit.clicked.connect(self.clickedExit)			        #Calling method for Exit button press

    def clickedMP(self):						        #Monitor Params
        #print "called MP"
        self.sigMP.emit()						        #Emitting Signal for Button press
        
    def clickedIP(self):						        #Interlock Params
        #print "Called IP"
        self.sigIP.emit()						        #Emitting Signal for Button press

    def clickedSC(self):						        #Set Controls
        #print "Called SC"
        self.sigSC.emit()						        #Emitting Signal for Button press

    def clickedCP(self):						        #Communication Parameters
        #print "Called CP"
        self.sigCP.emit()						        #Emitting Signal for Button press

    def clickedCalib(self):						        #Calibration
        #print "Called Calib"
        self.sigcalib.emit() 					                #Emitting Signal for Button press

    def clickedExit(self):						        #Exit
        #print "Called Exit"
        self.sigexit.emit()                                                     #Emitting Signal for Button press
        
class MonitorParams_Gui(QtGui.QWidget,Ui_MonitorParams,QtCore.QObject):
    
    sigbackMP = QtCore.pyqtSignal()                                             #PyQt Signal for back button 

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)
        self.listMP = [0,0,0]
        self.heaton = [0]
        self.heatoff = [0]
        self.dialval = [0]
        self.spinval = [0]
        self.btn_bck.clicked.connect(self.btnclicked)
         
        #self.bar = QRoundProgressBar()
        #self.bar.setFixedSize(650,650)
        #self.bar.setDonutThicknessRatio(0.65)
        #self.bar.setDecimals(1)
        #self.bar.setFormat('%p %')
        #self.bar.setNullPosition(-90)
        #self.bar.setBarStyle(QRoundProgressBar.StyleDonut)
        #self.bar.setDataColors([(0.,QtGui.QColor.fromRgb(0,150,0)),\
        #    (0.5,QtGui.QColor.fromRgb(230,230,0)),\
        #    (1.,QtGui.QColor.fromRgb(160,0,0))])
        #self.bar.setRange(0,100)
        #self.bar.setValue((str(str('25')+str('V'))))
        #self.verticalLayout_11.addWidget(self.bar)
        
        #self.bar_rt = QRoundProgressBar()
        #self.bar_rt.setFixedSize(650,650)
        #self.bar_rt.setDonutThicknessRatio(0.65)
        #self.bar_rt.setDecimals(1)
        #self.bar_rt.setFormat('%p ')
        #self.bar_rt.setNullPosition(-90)
        #self.bar_rt.setBarStyle(QRoundProgressBar.StyleDonut)
        #self.bar_rt.setDataColors([(0.,QtGui.QColor.fromRgb(0,150,0)),\
        #    (0.5,QtGui.QColor.fromRgb(230,230,0)),\
        #    (1.,QtGui.QColor.fromRgb(160,0,0))])
        #self.bar_rt.setRange(0,800)
        #self.verticalLayout_7.addWidget(self.bar_rt)
        
        #self.bar_lb = QRoundProgressBar()
        #self.bar_lb.setFixedSize(650,650)
        #self.bar_lb.setDonutThicknessRatio(0.65)
        #self.bar_lb.setDecimals(1)
        #self.bar_lb.setFormat('%p ')
        #self.bar_lb.setNullPosition(-90)
        #self.bar_lb.setBarStyle(QRoundProgressBar.StyleDonut)
        #self.bar_lb.setDataColors([(0.,QtGui.QColor.fromRgb(0,150,0)),\
        #    (0.5,QtGui.QColor.fromRgb(230,230,0)),\
        #    (1.,QtGui.QColor.fromRgb(160,0,0))])
        #self.bar_lb.setRange(0,11)
        #self.verticalLayout_4.addWidget(self.bar_lb)

        #self.bar_rb = QRoundProgressBar()
        #self.bar_rb.setFixedSize(650,650)
        #self.bar_rb.setDonutThicknessRatio(0.65)
        #self.bar_rb.setDecimals(1)
        #self.bar_rb.setFormat('%p ')
        #self.bar_rb.setNullPosition(-90)
        #self.bar_rb.setBarStyle(QRoundProgressBar.StyleDonut)
        #self.bar_rb.setDataColors([(0.,QtGui.QColor.fromRgb(0,150,0)),\
        #        (0.5,QtGui.QColor.fromRgb(230,230,0)),\
        #        (1.,QtGui.QColor.fromRgb(160,0,0))])
        #self.bar_rb.setRange(0,11)
        #self.verticalLayout_6.addWidget(self.bar_rb)


    def readData(self,value):                                                   #Read/Write data to/from the page
        self.dial.setEnabled(False)
        self.hmipot_IN.setEnabled(False)
        self.val = value
        #print value
        self.opvolt = value[0]
        #print self.opvolt
        self.inv = value[1]
        #print self.inv
        self.capv = value[2]
        #print self.capv
        self.freq = value[4]
        #print self.freq
        self.listMP = []
        self.hmipot_IN.valueChanged.connect(self.spinbox_value_changed)
        self.dial.valueChanged.connect(self.dial_value_changed)
        self.btn_heatON.clicked.connect(self.setheaton)
        #self.bar.setValue(self.capv)
        #self.bar_rt.setValue(self.opvolt)
        #self.bar_lb.setValue(self.freq)
        #self.bar_rb.setValue(self.inv)
        self.btn_heatOFF.clicked.connect(self.setheatoff)
        self.capV_out.setText(str(self.capv)+str('V'))
        self.opV_out.setText(str(self.opvolt)+str('V'))
        self.invC_out.setText(str(self.inv)+str('A'))
        self.freq_out.setText(str(self.freq)+str('KHz'))
        self.listMP.append(self.spinval[0])
        self.listMP.append(self.heatoff[0])
        self.listMP.append(self.heaton[0])
        return self.listMP 

    def setheaton(self):
        self.heaton.insert(0,1)
        self.heatoff.insert(0,0)
         
    def setheatoff(self):
        self.heatoff.insert(0,1)
        self.heaton.insert(0,0)

    def spinbox_value_changed(self,value):
        self.dial.setValue(value)
        self.spinval.insert(0,value)
        
    def dial_value_changed(self,value):
        self.hmipot_IN.setValue(value)
        self.spinval.insert(0,value)

    def btnclicked(self):
        self.sigbackMP.emit()
	

class InterlockParams_Gui(QtGui.QWidget,Ui_InterlockParams,QtCore.QObject):

    sigbackIP = QtCore.pyqtSignal()     

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)
        self.btn_bck.clicked.connect(self.btnclicked)
        self.btn_rst.clicked.connect(self.rstclicked)

    def readData(self,value):
        self.index1 = value[0]
        self.index2 = value[1]

        self.doorSwitch_OUT.setText("Door Switch Healthy")
        if self.index1 & 0x0001:
            self.doorSwitch_OUT.setStyleSheet("background-color:rgb(255,255,255);color: green")
        else:
            self.doorSwitch_OUT.setStyleSheet("background-color:rgb(255,255,255);color: red")
        
        self.psuWater_OUT.setText("PSU Water Pressure Healthy")
        if self.index1 & 0x0002:
            self.psuWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color: green")
        else:
            self.psuWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color: red")

        self.inletWater_OUT.setText("Inlet Water Temp. Healthy")
        if self.index1 & 0x0004:
            self.inletWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.inletWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.heatsinkWater_OUT.setText("Heatsink Water Temp. Healthy")
        if self.index1 & 0x0008:
            self.heatsinkWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.heatsinkWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.coilWater_OUT.setText("Coil Water Temp. Healthy")
        if self.index1 & 0x0010:
            self.coilWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.coilWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
        
        self.outletWater_OUT.setText("Outlet Water Temp. Healthy")
        if self.index1 & 0x0020:
            self.outletWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.outletWater_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
        
        self.coolingTower_OUT.setText("Cooling Tower Fault Healthy")
        if self.index1 & 0x0040:
            self.coolingTower_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.coolingTower_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        if self.index1 & 0x0080:
            self.emergency_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
            self.emergency_OUT.setText("Emergency OFF")
        else:
            self.emergency_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red") 
            self.emergency_OUT.setText("Emergency ON") 
        
        if self.index1 & 0x0100:
            self.dmPump_OUT_2.setStyleSheet("background-color:rgb(255,255,255);color:green")
            self.dmPump_OUT_2.setText("DM Pump ON")
        else:
            self.dmPump_OUT_2.setStyleSheet("background-color:rgb(255,255,255);color:red")
            self.dmPump_OUT_2.setText("DM Pump OFF")
        
        self.dmPump_OUT.setText("DM Pump Trip Fault Healthy")
        if self.index1 & 0x0200:
            self.dmPump_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.dmPump_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.airPress_OUT.setText("Air Pressure Healthy")
        if self.index1 & 0x0400:
            self.airPress_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.airPress_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        self.aux2_OUT.setText("AUX-2 Healthy")
        if self.index1 & 0x0800:
            self.aux2_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.aux2_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        if self.index1 & 0x1000:
            self.heaton = True
        else:
            self.heaton = False

        if self.index1 & 0x2000:
            self.heatoff = True
        else:
            self.heatff = False
            
        if self.index1 & 0x4000:
            self.rst = True
        else:
            self.rst = False
          
        self.aux1_OUT.setText("AUX-1 Healthy")
        if self.index1 & 0x8000:
            self.aux1_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.aux1_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        self.dcFault_OUT.setText("DC Fault Healthy")
        if self.index2 & 0x0001:
            self.dcFault_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.dcFault_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
        
        self.capTrip_OUT.setText("Capacitor Trip")
        if self.index2 & 0x0002:
            self.capTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.capTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
  
        self.capVolt_OUT.setText("Capacitor Volt Limit Healthy")
        if self.index2 & 0x0004:
            self.capVolt_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.capVolt_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        self.phaseLimit_OUT.setText("Phase Limit Healthy")
        if self.index2 & 0x0008:
            self.phaseLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.phaseLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        self.phaseTrip_OUT.setText("Phase Trip")
        if self.index2 & 0x0010:
            self.phaseTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.phaseTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.currLimit_OUT.setText("Current Limit Healthy")
        if self.index2 & 0x0020:
            self.currLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.currLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.currTrip_OUT.setText("Current Trip")
        if self.index2 & 0x0040:
            self.currTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.currTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.pwrLimit_OUT.setText("Power Limit Healthy")
        if self.index2 & 0x0080:
            self.pwrLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.pwrLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
        
        self.pwrTrip_OUT.setText("Power Trip")
        if self.index2 & 0x0100:
            self.pwrTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.pwrTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.freqLimit_OUT.setText("Frequency Limit Healthy")
        if self.index2 & 0x0200:
            self.freqLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.freqLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.freqTrip_OUT.setText("Frequency Trip")
        if self.index2 & 0x0400:
            self.freqTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.freqTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

        self.voltLimit_OUT.setText("Voltage Limit Healthy")
        if self.index2 & 0x0800:
            self.voltLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.voltLimit_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")
            
        self.voltTrip_OUT.setText("Voltage Trip")
        if self.index2 & 0x1000:
            self.voltTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:green")
        else:
            self.voltTrip_OUT.setStyleSheet("background-color:rgb(255,255,255);color:red")

    def rstclicked(self):
        self.reset = 1

    def btnclicked(self):
        self.sigbackIP.emit()

class SetControl_Gui(QtGui.QWidget,Ui_SetControls,QtCore.QObject):
    
    sigbackSC = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)
        self.btn_bck.clicked.connect(self.btnclicked)
        self.listSC = []

    def readData(self):
        self.max_pwr_IN.valueChanged.connect(self.val_maxpwr)
        self.min_pwr_IN.valueChanged.connect(self.val_minpwr)
        self.max_voltage_IN.valueChanged.connect(self.val_maxvolt)
        self.min_voltage_IN.valueChanged.connect(self.val_minvolt)
        self.max_current_IN.valueChanged.connect(self.val_maxcurrent)
        self.min_current_IN.valueChanged.connect(self.val_mincurrent)
        self.currentTrip_IN.valueChanged.connect(self.val_currentTrip)
        self.max_capV_IN.valueChanged.connect(self.val_maxcapv)
        self.min_capV_IN.valueChanged.connect(self.val_mincapv)
        self.capVTrip_IN.valueChanged.connect(self.val_capvtrip)
        self.max_freq_IN.valueChanged.connect(self.val_maxfreq)
        self.min_freq_IN.valueChanged.connect(self.val_minfreq)
        self.high_Q_IN.valueChanged.connect(self.val_highQ)
        self.low_Q_IN.valueChanged.connect(self.val_lowQ)
        self.QTrip_IN.valueChanged.connect(self.val_Qtrip)
        self.ctrl_IN.currentIndexChanged.connect(self.val_ctrlmode)
        self.feedback_IN.currentIndexChanged.connect(self.val_feedbackmode)

        self.listSC = [0]
        
        self.listSC.append(self.currentTrip_IN.value())
        self.listSC.append(self.QTrip_IN.value())
        self.listSC.append(self.capVTrip_IN.value())
        self.listSC.append(self.max_pwr_IN.value())
        self.listSC.append(self.max_voltage_IN.value())
        self.listSC.append(self.max_current_IN.value())
        self.listSC.append(self.max_freq_IN.value())
        self.listSC.append(self.high_Q_IN.value())
        self.listSC.append(self.max_capV_IN.value())
        self.listSC.append(self.min_pwr_IN.value())
        self.listSC.append(self.min_voltage_IN.value())
        self.listSC.append(self.min_current_IN.value())
        self.listSC.append(self.min_freq_IN.value())
        self.listSC.append(self.low_Q_IN.value())
        self.listSC.append(self.min_capV_IN.value())
        self.listSC.append(self.ctrl_IN.currentIndex())
        self.listSC.append(self.feedback_IN.currentIndex())
        return self.listSC[1:18]
        
    def val_maxpwr(self,value):
        self.max_pwr_IN.setValue(value)
        self.maxpwr = value

    def val_minpwr(self,value):
        self.min_pwr_IN.setValue(value)
        self.minpwr = value

    def val_maxvolt(self,value):
        self.max_voltage_IN.setValue(value)
        self.maxvolt = value
	
    def val_minvolt(self,value):
        self.min_voltage_IN.setValue(value)
        self.minvolt = value
	
    def val_maxcurrent(self,value):
        self.max_current_IN.setValue(value)
        self.maxcurrent = value
	
    def val_mincurrent(self,value):
        self.min_current_IN.setValue(value)
        self.mincurrent = value

    def val_currentTrip(self,value):
        self.currentTrip_IN.setValue(value)
        self.currentTrip = value
	
    def val_maxcapv(self,value):
        self.max_capV_IN.setValue(value)
        self.maxcapv = value
		
    def val_mincapv(self,value):
        self.min_capV_IN.setValue(value)
        self.mincapv = value

    def val_capvtrip(self,value):
        self.capVTrip_IN.setValue(value)
        self.capvtrip = value
		
    def val_maxfreq(self,value):
        self.max_freq_IN.setValue(value)
        self.maxfreq = value
		
    def val_minfreq(self,value):
        self.min_freq_IN.setValue(value)
        self.minfreq = value
		
    def val_highQ(self,value):
        self.high_Q_IN.setValue(value)
        self.highQ = value
		
    def val_lowQ(self,value):
        self.low_Q_IN.setValue(value)
        self.lowQ = value

    def val_Qtrip(self,value):
        self.QTrip_IN.setValue(value)
        self.qtrip = value

    def val_ctrlmode(self,value):
        self.ctrlidx = value

    def val_feedbackmode(self,value):
        self.fbidx = value
		
    def btnclicked(self):
        self.sigbackSC.emit()

    
class Calib_Gui(QtGui.QWidget,Ui_Calibration,QtCore.QObject):

    sigbackCalib = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)	
        self.btn_bck.clicked.connect(self.btnclicked)
        self.listCalib = []

    def readData(self,value):
        self.listCalib = []
        self.op_mf_IN.valueChanged.connect(self.val_opMF)
        self.inv_mf_IN.valueChanged.connect(self.val_invMF)
        self.prim_mf_IN.valueChanged.connect(self.val_primMF)
        self.trans_mf_IN.valueChanged.connect(self.val_transMF)
        self.cap_mf_IN.valueChanged.connect(self.val_capMF)
        self.pll_mf_IN.valueChanged.connect(self.val_pllMF)
        self.freq_mf_IN.valueChanged.connect(self.val_freqMF)
        self.local_mf_IN.valueChanged.connect(self.val_localMF)
        self.remote_mf_IN.valueChanged.connect(self.val_remoteMF)
        self.plc_mf_IN.valueChanged.connect(self.val_plcMF)
        self.mA1_mf_IN.valueChanged.connect(self.val_ma1MF)
        self.mA2_mf_IN.valueChanged.connect(self.val_ma2MF)
        self.mA3_mf_IN.valueChanged.connect(self.val_ma3MF)
        self.mA4_mf_IN.valueChanged.connect(self.val_ma4MF)
        self.pwr_mf_IN.valueChanged.connect(self.val_pwrMF)
    
        self.listCalib.append(self.pwr_mf_IN.value())
        self.listCalib.append(self.prim_mf_IN.value())
        self.listCalib.append(self.inv_mf_IN.value())
        self.listCalib.append(self.freq_mf_IN.value())
        self.listCalib.append(self.pll_mf_IN.value())
        self.listCalib.append(self.cap_mf_IN.value())

        self.actual_data = value
        #print self.actual_data
        self.op_mf_Actual.setNum(self.actual_data[4])
        self.inv_mf_Actual_2.setNum(self.actual_data[5])
        self.prim_mf_Actual.setNum(self.actual_data[3])
        self.trans_mf_Actual.setNum(self.actual_data[2])
        self.cap_mf_Actual.setNum(self.actual_data[6])
        self.pll_mf_Actual.setNum(self.actual_data[7])
        self.freq_mf_Actual.setNum(self.actual_data[8])
        self.local_mf_Actual.setNum(self.actual_data[1])
        self.remote_mf_Actual.setNum(self.actual_data[0])
        self.plc_mf_Actual.setNum(self.actual_data[13])
        self.mA1_mf_Actual.setNum(self.actual_data[9])
        self.mA2_mf_Actual.setNum(self.actual_data[10])
        self.mA3_mf_Actual.setNum(self.actual_data[11])
        self.mA4_mf_Actual.setNum(self.actual_data[12])
        self.pwr_mf_Actual.setNum(self.actual_data[14])

        self.op_mf_Calib.setNum(self.op_mf_IN.value() * self.actual_data[4])

        self.inv_mf_Calib_2.setNum(self.inv_mf_IN.value() * self.actual_data[5])
        
        self.prim_mf_Calib.setNum(self.prim_mf_IN.value() * self.actual_data[3])
        
        self.trans_mf_Calib.setNum(self.trans_mf_IN.value() * self.actual_data[2])

        self.cap_mf_Calib.setNum(self.cap_mf_IN.value() * self.actual_data[6])
        
        self.pll_mf_Calib.setNum(self.pll_mf_IN.value() * self.actual_data[7])

        self.freq_mf_Calib.setNum(self.freq_mf_IN.value() * self.actual_data[8])
        
        self.local_mf_Calib.setNum(self.local_mf_IN.value() * self.actual_data[1])
        
        self.remote_mf_Calib.setNum(self.remote_mf_IN.value() * self.actual_data[0])
        
        self.plc_mf_Calib.setNum(self.plc_mf_IN.value() * self.actual_data[13])
        
        self.mA1_mf_Calib.setNum(self.mA1_mf_IN.value() * self.actual_data[9])
        
        self.mA2_mf_Calib.setNum(self.mA2_mf_IN.value() * self.actual_data[10])
        
        self.mA3_mf_Calib.setNum(self.mA3_mf_IN.value() * self.actual_data[11])
        
        self.mA4_mf_Calib.setNum(self.mA4_mf_IN.value() * self.actual_data[12])
        
        self.pwr_mf_Calib.setNum(self.pwr_mf_IN.value() * self.actual_data[14])

        return self.listCalib

    def val_opMF(self,value):
	self.op_mf_Calib.setNum(value * 1)					#replace number with the data passed in to function
	
    def val_invMF(self,value):
	self.inv_mf_Calib_2.setNum(value * 1)
		
    def val_primMF(self,value):
	self.prim_mf_Calib.setNum(value * 1)
	
    def val_transMF(self,value):
	self.trans_mf_Calib.setNum(value * 1)
		
    def val_capMF(self,value):
	self.cap_mf_Calib.setNum(value * 1)
		
    def val_pllMF(self,value):
	self.pll_mf_Calib.setNum(value * 1)
		
    def val_freqMF(self,value):
	self.freq_mf_Calib.setNum(value * 1)
	
    def val_localMF(self,value):
	self.local_mf_Calib.setNum(value * 1)
		
    def val_remoteMF(self,value):
	self.remote_mf_Calib.setNum(value * 1)
	
    def val_plcMF(self,value):
	self.plc_mf_Calib.setNum(value * 1)
		
    def val_ma1MF(self,value):
	self.mA1_mf_Calib.setNum(value * 1)
		
    def val_ma2MF(self,value):
	self.mA2_mf_Calib.setNum(value * 1)
		
    def val_ma3MF(self,value):
	self.mA3_mf_Calib.setNum(value * 1)
		
    def val_ma4MF(self,value):
	self.mA4_mf_Calib.setNum(value * 1)
		
    def val_pwrMF(self,value):
	self.pwr_mf_Calib.setNum(value * 1) 

    def btnclicked(self):
        self.sigbackCalib.emit()

class CommParams_Gui(QtGui.QWidget,Ui_CommParams,QtCore.QObject):

    sigbackCP = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        QtCore.QObject.__init__(self)
        self.setupUi(self)
        self.btn_bck.clicked.connect(self.btnclicked)
        self.listCP = [0]

    def readData(self):
        self.listCP = []
	self.visa_rsrc_IN.currentIndexChanged.connect(self.val_visarsrc)
	self.baud_IN.currentIndexChanged.connect(self.val_baud)
	self.flowCtrl_IN.currentIndexChanged.connect(self.val_flowctrl)
	self.parity_IN.currentIndexChanged.connect(self.val_parity)
	self.timeout_IN.valueChanged.connect(self.val_timeout)
	self.mode_IN.currentIndexChanged.connect(self.val_mode)
	self.slaveAddr_IN.valueChanged.connect(self.val_slaveAddr)
	self.access_IN.currentIndexChanged.connect(self.val_access)
	self.length_IN.valueChanged.connect(self.val_length)
	self.readQty_IN.valueChanged.connect(self.val_readqty)
        
        self.listCP.append(self.visa_rsrc_IN.currentIndex())
        self.listCP.append(self.baud_IN.currentIndex())
        self.listCP.append(self.flowCtrl_IN.currentIndex())
        self.listCP.append(self.parity_IN.currentIndex())
        self.listCP.append(self.timeout_IN.value())
        self.listCP.append(self.mode_IN.currentIndex())
        self.listCP.append(self.slaveAddr_IN.value())
        self.listCP.append(self.access_IN.currentIndex())
        self.listCP.append(self.length_IN.value())
        self.listCP.append(self.readQty_IN.value())
        return self.listCP


    def val_visarsrc(self,value):
	self.visarsrc = value
	
    def val_baud(self,value):
	self.baudrate = value
		
    def val_flowctrl(self,value):
	self.flowctrl = value
	
    def val_parity(self,value):
	self.parity = value
	
    def val_timeout(self,value):
	self.timeout = value
		
    def val_mode(self,value):
	self.mode = value
		
    def val_slaveAddr(self,value):
	self.slaveaddress = value
		
    def val_access(self,value):
	self.access = value
	
    def val_length(self,value):
	self.length = value
		
    def val_readqty(self,value):
	self.readQty = value
		
    def btnclicked(self):
        self.sigbackCP.emit()


def main():
    app = QtGui.QApplication(sys.argv)
    bus = ModbusComm()
    scr_res = app.desktop().screenGeometry()
    wid,hei = scr_res.width(),scr_res.height()
    w = MainWidget()
    w.initWidget()
    #w.setFixedSize(wid,hei+2)
    w.show()
    app.exec_()

if __name__ == '__main__':
    main()
