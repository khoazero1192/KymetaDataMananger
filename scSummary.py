"""
Author: Khoa Au

kau@kymetacorp.com
5/27/2016
"""
import numpy
import pandas as pd
import logging
import os
import tkinter as tk
import tkFileDialog as tkFile
import json
from datetime import datetime
from LoggingUtil import XStream,QtHandler
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QFileDialog, QMessageBox, QVBoxLayout, QRect
from __builtin__ import file
from fileinput import filename
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from numpy import empty
import wx
import sys
import re
import math
#sys.path.append('C:\dev\sparms')
from sparmsPkg.s2p_calculations import S2PDataProcessing as DP
from OrionUtilPkg.common_gui import MultiFileSelect,TxRxFilePairing
from cmath import log10
from _ast import Num

logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):
    _CSV_FILE_PATH_ = ''
    _FILE_NAME = ''
    _ANTENNA_SERIAL_NUMBER = ''
    _ANTENNA_BUILD_NUMBER =''
    _PATTERN_FREQ_RX = 0.0
    _PATTERN_LPA_RX = 0
    _PATTERN_FREQ_TX = 0.0
    _PATTERN_LPA_TX = 0
    _TYPE_OF_SCAN = ''
    _CSV_EXPORT_PATH_ =""
    _S2P_FILE_TAB_3_ = ""
    _CSV_FILE_TAB_3 = ""
    freq_dictionary = {'10000000000':'23.36','10100000000':'23.35','10200000000':'23.45','10300000000':'23.58','10400000000':'23.56','10500000000':'23.58','10600000000':'23.72','10700000000':'23.74',
                       '10800000000':'23.69','10090000000':'23.80','11000000000':'23.93','11100000000':'23.89','11200000000':'23.89','11300000000':'24.01','11400000000':'24.06','11500000000':'24.03','11600000000':'24.07',
                       '11700000000':'24.16','11800000000':'24.19','11900000000':'24.21','12000000000':'24.25','12100000000':'24.30','12200000000':'24.33','12300000000':'24.35','12400000000':'24.38','12500000000':'24.43',
                       '12600000000':'24.46','12700000000':'24.44','12800000000':'24.47','12900000000':'24.56','13000000000':'24.57','13100000000':'24.56','13200000000':'24.62','13300000000':'24.67','13400000000':'24.64',
                       '13500000000':'24.65','13600000000':'24.73','13700000000':'24.74','13800000000':'24.71','13900000000':'24.79','14000000000':'24.85','14100000000':'24.80','14200000000':'24.80','14300000000':'24.89',
                       '14400000000':'24.86','14500000000':'24.81','14600000000':'24.89','14700000000':'24.93','14800000000':'24.82','14900000000':'24.83','15000000000':'24.98'}
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_time =datetime.now()
    frame = pd.DataFrame()
    
    
    def setupUi(self, Form):
        
        app = wx.App(False)
        w, h = wx.GetDisplaySize()
        print w,h
        
        
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(w-20, h-60)
        
        
        self.popupWin = QtGui.QMessageBox(Form)
        self.popupWin.setWindowTitle('Warning')
        self.popupWin.setStandardButtons(QMessageBox.Ok)
        
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(30, 30, w-120, h-120))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.formLayoutWidget = QtGui.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 8, 411, 331))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        
        
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.pushButton = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.pushButton_2)
        
        self.label = QtGui.QTextEdit(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setDisabled(True)
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label)
        self.label_2 = QtGui.QTextEdit(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setDisabled(True)
        
        
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_2)
        self.verticalLayoutWidget = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(450, 10, 701, 651))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.pushButton_3 = QtGui.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 400, 161, 101))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        
        
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 50, w-200, h-250))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
             
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self._console = QtGui.QTextBrowser()        
        # maplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.tab_2)
        
        
        #tab 2 section for table of sidelobes data
        
        
        
        self.verticalLayout.addWidget(self._console)
        #self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self._console)
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )
        
       
        self.verticalLayout_2.addWidget(self.canvas)
        
        """
        TAB 3 First Pass data processing
        """
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_3,_fromUtf8("First Pass"))
        
        self.formLayoutWidgetTab3 = QtGui.QWidget(self.tab_3)
        self.formLayoutWidgetTab3.setGeometry(QtCore.QRect(20, 8, 411, 331))
        self.formLayoutWidgetTab3.setObjectName(_fromUtf8("formLayoutWidgetTab3"))
        
        self.formLayoutTab3 = QtGui.QFormLayout(self.formLayoutWidgetTab3)
        self.formLayoutTab3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayoutTab3.setMargin(0)
        self.formLayoutTab3.setObjectName(_fromUtf8("formLayoutTab3"))
        
        self.s2pfileTab3 = QtGui.QTextEdit()
        self.formLayoutTab3.setWidget(0, QtGui.QFormLayout.FieldRole, self.s2pfileTab3)
        self.s2pfileTab3Label = QtGui.QLabel()
        self.s2pfileTab3Label.setText("S2P directory")
        self.formLayoutTab3.setWidget(0,QtGui.QFormLayout.LabelRole,self.s2pfileTab3Label)
        
        self.csvfileTab3 = QtGui.QTextEdit()
        self.formLayoutTab3.setWidget(1,QtGui.QFormLayout.FieldRole,self.csvfileTab3)
        self.csvfileTab3Label = QtGui.QLabel()
        self.csvfileTab3Label.setText('Scorecard directory')
        self.formLayoutTab3.setWidget(1,QtGui.QFormLayout.LabelRole,self.csvfileTab3Label)
        
        self.processButtonTab3 = QtGui.QPushButton(self.tab_3)
        self.processButtonTab3.setGeometry(QtCore.QRect(20,400,150,120))
        self.processButtonTab3.setText('Process')
        
        
        
        QtCore.QObject.connect(self.processButtonTab3,QtCore.SIGNAL(_fromUtf8("clicked()")),self._processTab3_)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL(_fromUtf8("clicked()")),self._open_csv_)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL(_fromUtf8("clicked()")),self._saveFile_)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL(_fromUtf8("clicked()")),self._process)
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Score Card Summary", None))
        self.pushButton.setText(_translate("Form", "Open Directory", None))
        self.pushButton_2.setText(_translate("Form", "Export Directory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Side Lobe", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Side Lobe Plot", None))
        self.pushButton_3.setText(_translate("Form", "Process", None))
      
    def parseFreq(self,file):
        return ''.join(re.findall('_f=(.*?)_L90', file))
        
    
    
    def _process_S2P_tab3(self):
        #read the lineedit to grab the s2p path
        num = 4.5479  #4* math.pow(3.14159,2)*math.pow(0.34, 2)- math.pow(0.02,2) 
        self.s2pfileTab3.setText('C:\dev\AAE000J170417056 (U7.47R6-01)\Opt\dynBW_1_best')
        self._S2P_FILE_TAB_3_ = str(self.s2pfileTab3.toPlainText())
        
        fre = []
        gain_at_freq = []
        directivity = []
        frame = pd.DataFrame()
        #iterate throught the files that contain the s2p files 
        for file in sorted(os.listdir(self._S2P_FILE_TAB_3_)):
            if self.smartPick(file) == '.s2p':
                #read that s2p file
                #print file
                #print os.path.join(self._S2P_FILE_TAB_3_,file)
                #print self.parseFreq(file)
                giga_freq = float(self.parseFreq(file))*1e-9
                fre.append(giga_freq)
                mys2p = DP(os.path.join(self._S2P_FILE_TAB_3_,file))
                #gain_at_freq.append(mys2p.s21_gain_at_frequency(int(self.parseFreq(file)), return_nearest = False))
                for key in self.freq_dictionary:
                    if key == self.parseFreq(file):
                        value = float(self.freq_dictionary[key]) + float(mys2p.s21_gain_at_frequency(int(self.parseFreq(file)), return_nearest = False)) 
                        gain_at_freq.append(value)
                #parse the frequency at that file
                #calculate the directivity
                
                #print num 
                #print math.pow(0.3/giga_freq,2)
                
                
                directivity.append(abs(10*log10(num/math.pow(0.3/giga_freq,2))))
        frame.insert(0, column = "Frequencies (GZ)", value = fre)
        frame.insert(1, column = "Optimized S21 + cal (dBi) LPA90P0T0", value = gain_at_freq)
        frame.insert(2, column = 'Theoretical Directivity',value = directivity)
        frame.to_csv('test.csv')
        print frame
        
    def _process_CSV_tab3(self):
        self.csvfileTab3.setText('K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)\AAE000J170417056 (U7.47R6-01)\FF\RF_First_Pass\Broadside_DBW')
        self._CSV_FILE_TAB_3 = str(self.csvfileTab3.toPlainText())
        print self._CSV_FILE_TAB_3
        #grabs the gain and append it to the appropriate jsons
        
        
        
    def _processTab3_(self):
        self._process_S2P_tab3()
        self._process_CSV_tab3()        
    """
    This method determines whether a csv file is a scorecard 
    """  
    
    #if processType = 1 then its sidelobe processing. If processType = 2 then it is firstpass
    def _processtab1(self):
            self._process(self._CSV_FILE_PATH_, self._CSV_EXPORT_PATH_, processType = 1)
            
            
            
    
    def _process(self,openPath,exportPath,processType = None):
        plt.cla()
        if openPath == '' or exportPath == '':
            self.popupWin.setText('Please indicate scorecard directory OR export directory')
            self.popupWin.show()
            return
        else:
            
            list = []
            
        #grabs the first file, populates it with anntenas serial number
        #process the files in the directory, first check if a file is a csv
        for file in sorted(os.listdir(openPath)):
            if (self.isScoreCard(file)):
                logger.info(self.current_time + ' Reading csv file')
                colHeader = ['Theta_deg','phi','xpd','Sidelobe_1_dBc','Sidelobe_1_deg','Sidelobe_2_dBc','Sidelobe_2_deg','pol','frequency']
                
                df = pd.read_csv(os.path.join(openPath,file),usecols = colHeader)
                #print df
                #if found a score card, check if it is a Tx scorecard or a Rx score card?
                if ('_Rx_' in file):
                    logger.info(self.current_time + ' Found an RX ScoreCard')
                    #print 'Rx score card :' + self.getRxJsonName(file)
                    #give me the name of the tx json
                    #perform parsing on the Rx json to get Pattern_FREQ and LPA
                    self.parseRxJson(self.getRxJsonName(file))
                    logger.info(self.current_time + ' Parse the Rx Json')
                    #iterate back to the file read to find the header that contains the appropriate bounds
                    for index, row in df.iterrows():
                        if row['frequency'] == float(self._PATTERN_FREQ_RX) and row['pol'] == float(self._PATTERN_LPA_RX):
                            outputFrame = pd.DataFrame(row)
                            transposeFrame = outputFrame.T
                            transposeFrame.insert(0, column = 'Pattern_FREQ_RX', value =self._PATTERN_FREQ_RX)
                            transposeFrame.insert(0, column = 'Pattern_LPA_RX', value =self._PATTERN_LPA_RX)
                            list.append(transposeFrame)
                            #slice here
                    
                    #a = numpy.where(df ['pol'] == self._PATTERN_LPA_RX) [0]
                    #b = numpy.where (df['frequency'] == float(self._PATTERN_FREQ_RX)) [0]
                    #c= (set(a)&set(b))
                    #for item in c:
                    #    print item
                    #    print df.iloc[item]
                        
                        
                    #print df.iloc(c)
                    
                    #print (numpy.where((df['frequency'] == float(self._PATTERN_FREQ_RX)) and df['pol'] == self._PATTERN_LPA_RX) [0])
                     
                    df.insert(0, column = 'Pattern_FREQ_RX', value =self._PATTERN_FREQ_RX)
                    df.insert(0, column = 'Pattern_LPA_RX', value =self._PATTERN_LPA_RX)
                elif ('_Tx_' in file):
                    logger.info(self.current_time + ' Found a Tx scorecard')
                    if ('_RxRef_' in file): #indication of MiniPostOpt Scan
                        logger.info(self.current_time + ' FoundMiniPostOpt Tx json')
                        #print self.getTxJsonNameMiniPostOpt(file)
                        self.parseTxJson(self.getTxJsonNameMiniPostOpt(file))
                        
                        #insert TX parameters
                        #df.insert(0, column = 'Pattern_FREQ_TX', value =self._PATTERN_FREQ_TX)
                        #df.insert(0, column = 'Pattern_LPA_TX', value =self._PATTERN_LPA_TX)
                    else:#other wise this is a first pass
                        #print 'went here'
                        #print 'Tx score card :' + self.getTxJsonName(file)
                        logger.info(self.current_time + ' Found regular Txjson')
                        self.parseTxJson(self.getTxJsonName(file))
                        #insert TX parameters
                        #df.insert(0, column = 'Pattern_FREQ_TX', value =self._PATTERN_FREQ_TX)
                        #df.insert(0, column = 'Pattern_LPA_TX', value =self._PATTERN_LPA_TX)
                        #print " "
                    for index, row in df.iterrows():
                        if row['frequency'] == float(self._PATTERN_FREQ_TX) and row['pol'] == float(self._PATTERN_LPA_TX):
                            outputFrame = pd.DataFrame(row)
                            transposeFrame = outputFrame.T
                            transposeFrame.insert(0, column = 'Pattern_FREQ_TX', value =self._PATTERN_FREQ_TX)
                            transposeFrame.insert(0, column = 'Pattern_LPA_TX', value =self._PATTERN_LPA_TX)
                            list.append(transposeFrame)
          
                #list.append(df)
                #print file
        #print list    
            #else:
                #logger.debug('folder does not contain scorecard file')
                #return
        self.frame = pd.concat(list)
        self._plot_()
        
        
        #frame.sort_index(axis =1,inplace = True)
        #uncomment this to add a collumn of antenna serial number
        self.frame.insert(0, column = 'SERIAL NUMBER', value=self._ANTENNA_SERIAL_NUMBER)
        self._TYPE_OF_SCAN = os.path.basename(os.path.normpath(openPath))
        #print frame
        header = ['Pattern_FREQ_RX','Pattern_FREQ_TX','Pattern_LPA_RX','Pattern_LPA_TX','Theta_deg','phi','xpd','Sidelobe_1_dBc','Sidelobe_1_deg','Sidelobe_2_dBc','Sidelobe_2_deg'] 
        
        try:
            self.frame.to_csv(os.path.join(self._CSV_EXPORT_PATH_,'Score_Card_Summary ' + self._ANTENNA_SERIAL_NUMBER + ' ' + '(' + self._ANTENNA_BUILD_NUMBER + ')_'+ self._TYPE_OF_SCAN  +'.csv' ),encoding = 'utf-8',columns = header,index = False)
        except:
            self.popupWin.setText(" PLEASE CLOSE THE CURRENT CSV FILE AND TRY AGAIN ")
            self.popupWin.show()
            logger.error('Cannot Write CSV')
            return
        
        
        logger.info(self.current_time + ' Written a CSV file')
        logger.info('data plotted succesfully')
    
    
    def _plot3_(self):# ignore positive or negative polarity
        
        sideLobe1 = []
        sideLobe2 = []
        
        for index,row in self.frame.iterrows():
            sideLobe1.append(row['Sidelobe_1_dBc'])
            sideLobe2.append(row['Sidelobe_2_dBc'])
            
        
        plt.xlabel('Samples')
        plt.ylabel('gain (dB)')
        plt.title('Positive Sidelobes')
        plt.plot(sideLobe1,label = 'SideLobe1')
        plt.plot(sideLobe2,label = 'SideLobe2')
        plt.legend(loc="upper left", bbox_to_anchor=[1, 1],ncol=1, shadow=True)
        
        self.canvas.draw()
        
    
    def _plot2_(self):# plot for sidelobe 1 and 2 in. two for positive degrees and 2 for negative degrees
        plt.close()
        sideLobe1Pos = []
        sideLobe2Pos = []
        
        sideLobe1Neg = []
        sideLobe2Neg = []
        
        for index, row in self.frame.iterrows():
            if row['Sidelobe_1_deg'] > 0:
                sideLobe1Pos.append(row['Sidelobe_1_dBc'])
            elif row['Sidelobe_2_deg'] > 0:
                sideLobe2Pos.append(row['Sidelobe_2_dBc'])
            
        for index2,row2 in self.frame.iterrows():
            if row2['Sidelobe_1_deg'] < 0:
                sideLobe1Neg.append(row2['Sidelobe_1_dBc'])
            elif row2['Sidelobe_2_deg'] < 0:
                sideLobe2Neg.append(row2['Sidelobe_2_dBc'])    
                    
             
             
        plt.subplot(2,1,1)
        plt.xlabel('Samples')
        plt.ylabel('gain (dB)')
        plt.title('Positive Sidelobes')
        plt.plot(sideLobe1Pos,label = 'SideLobe1')
        plt.plot(sideLobe2Pos,label = 'SideLobe2')
        plt.legend(loc="upper left", bbox_to_anchor=[1, 1],ncol=1, shadow=True)  
        plt.subplot(2,1,2)
        plt.xlabel('Samples')
        plt.ylabel('gain (dB)')
        plt.title('Negative Sidelobes')
        plt.plot(sideLobe1Neg,label = 'SideLobe1')
        plt.plot(sideLobe2Neg,label = 'SideLobe2')
        plt.legend(loc="upper left", bbox_to_anchor=[1, 1],ncol=1, shadow=True)  
        #self.canvas.draw()
        plt.show()
    def _plot_(self):
        print 'hello??????????????????????????'
        sideLobe1PosTx = []
        sideLobe2PosTx = []
        sideLobe1PosRx = []
        sideLobe2PosRx = []
        
        sideLobe1NegTx = []
        sideLobe2NegTx = []
        sideLobe1NegRx = []
        sideLobe2NegRx = []
       
        
        for index,row in self.frame.iterrows():
            if float(row['frequency'])>13.0: #this is data for TX
                if float(row['Sidelobe_1_deg']) > 0:
                    sideLobe1PosTx.append(row['Sidelobe_1_dBc']) # sideLobe1 Positive Tx
                if float(row['Sidelobe_2_deg'])> 0:
                    sideLobe2PosTx.append(row['Sidelobe_2_dBc']) # sideLobe2 Positive Tx
                if float(row['Sidelobe_1_deg']) < 0:
                    sideLobe1NegTx.append(row['Sidelobe_1_dBc']) # sideLobe1 Negative Tx
                if float(row['Sidelobe_2_deg'])< 0:
                    sideLobe2NegTx.append(row['Sidelobe_2_dBc']) # sideLobe2 Negative Tx
                
                
                
                
            elif float(row['frequency'] < 13.0): #this is data for RX
                pass
        
        
        
        
        
        print sideLobe1PosTx
        print sideLobe2PosTx
        print sideLobe1NegTx
        print sideLobe2NegTx
       
        plt.subplot(2,1,1) 
        plt.xlabel('Samples')
        plt.ylabel('gain (dB)')
        plt.title('Positive Sidelobes')
        plt.plot(sideLobe1PosTx,label = 'SL1Tx')
        plt.plot(sideLobe2PosTx,label = 'SL2Tx')
        plt.plot(sideLobe1PosRx,label = 'SL1Rx')
        plt.plot(sideLobe2PosRx,label = 'SL2Rx')
        plt.legend(loc="upper left", bbox_to_anchor=[1, 1],ncol=1, shadow=True)
        plt.subplot(2,1,2)
    
        plt.title('Negative Sidelobes')
        plt.plot(sideLobe1NegRx,label = 'SL1RX')
        plt.plot(sideLobe2NegRx,label = 'SL2RX')
        plt.plot(sideLobe1NegTx,label = 'SL1Tx')
        plt.plot(sideLobe2NegTx,label = 'SL2Tx')
        plt.legend(loc="upper left", bbox_to_anchor=[1, 1],ncol=1, shadow=True)
        self.canvas.draw()
    def _saveFile_(self):
        root = tk.Tk()
        root.withdraw()
        self._CSV_EXPORT_PATH_ = 'C:/dev/Test3/ExportTest'
        #self._CSV_EXPORT_PATH_ = tkFile.askdirectory()
        if self._CSV_EXPORT_PATH_ == '':
            self.popupWin.setText("please select a Path")
            self.popupWin.show()
            return
       
        logger.info(self.current_time + ' Csv file folder path: ' + self._CSV_EXPORT_PATH_)
        self.label_2.setText(self._CSV_EXPORT_PATH_)
    
    def _getSerialNumber_(self,antenna_path):
        #get a score_card file
        sc_file = ''
        for file in os.listdir(antenna_path):
            if self.isScoreCard(file):
                #print file
                sc_file = file # save this file
                break # exit the loop soon as the first score card file is found
            
        #print sc_file
        for c in sc_file:
            if c == '_':
                break# break as soon as the first _ is seen
            else:
                self._ANTENNA_SERIAL_NUMBER = self._ANTENNA_SERIAL_NUMBER + c
        
        #print self._ANTENNA_BUILD_NUMBER
        #print self._ANTENNA_SERIAL_NUMBER 
        #try to get antenna build number
        start,end = str(antenna_path).split(self._ANTENNA_SERIAL_NUMBER)
        dummy = ''
        for d in end:
            if d == ')':
                break
            elif d is not '(' and d is not ' ':
                self._ANTENNA_BUILD_NUMBER = self._ANTENNA_BUILD_NUMBER + d
        #print end
        #print self._ANTENNA_BUILD_NUMBER
        #print 'Completed'
        
    def getJsonInfo(self):
        pass  
    def isScoreCard (self,file):
        count = 0
        string = 'scorecard'
        return string in file  
        
    def isJason(self,file):
        if self.smartPick(file) == '.json':
            return True
        
    def parseTxJson(self,tx_name):
        #reiterate through the folder again to find the appropriate tx jason
        for file in os.listdir(self._CSV_FILE_PATH_):
            if self.isJason(file):
                #check for tx name
                if tx_name in file:
                    #read that file
                    my_data = json.load(open(os.path.join(self._CSV_FILE_PATH_,file)))
                    #print 'tx json freqeuncy values: ' + str(my_data['TX']['Pattern_FREQ'])
                    self._PATTERN_FREQ_TX = my_data['TX']['Pattern_FREQ']
                    self._PATTERN_LPA_TX = my_data['TX']['Pattern_LPA']
                    #print str(self._PATTERN_FREQ_TX) + ' , ' +str(self._PATTERN_LPA_TX)
                    
                                
    def parseRxJson(self,rx_name):
        for file in os.listdir(self._CSV_FILE_PATH_):
            if self.isJason(file):
                #check for tx name
                if rx_name in file:
                    #read that file
                    my_data = json.load(open(os.path.join(self._CSV_FILE_PATH_,file)))
                    #print 'tx json freqeuncy values: ' + str(my_data['RX']['Pattern_FREQ'])
                    #save the appropriate data 
                    self._PATTERN_FREQ_RX = my_data['RX']['Pattern_FREQ']
                    self._PATTERN_LPA_RX = my_data['RX']['Pattern_LPA']
                    #print str(self._PATTERN_FREQ_RX) + ' , ' + str(self._PATTERN_LPA_RX)
             
                    
    #get rx and tx jsons names from the scorecard file, these methods depends heavily on the naming convention
    #chaning the naming convention will cause this method to malfunction
    def getRxJsonName(self,my_scorecard):
        logger.debug(self.current_time + ' Rx Json Name is:' + my_scorecard.split('_',2)[1])
        return my_scorecard.split('_',2)[1]
        
    def getTxJsonName(self,my_scorecard):
        logger.debug(self.current_time + ' Tx Json Name is:' + my_scorecard.split('_',3)[2])
        return my_scorecard.split('_',3)[2]
    def getTxJsonNameMiniPostOpt(self,my_scorecard):
        logger.debug(self.current_time + ' Tx Minipost Opt Json Name is:' + my_scorecard.split('_',4)[3])
        return my_scorecard.split('_',4)[3]
   
    
    def smartPick(self,aFile):
        head,extendsion = os.path.splitext(aFile)
        return extendsion

    def _open_csv_(self):
        #initialize the file path to avoid error when user clicked on open button multiple times
        #logger.info(self.current_time+ ' Reinitializing instance variables ')
        self._CSV_FILE_PATH_ = ''
        self._ANTENNA_SERIAL_NUMBER = ''
        self._ANTENNA_BUILD_NUMBER =''
        root = tk.Tk()
        root.withdraw()
        #self._CSV_FILE_PATH_ = tkFile.askdirectory()
        self._CSV_FILE_PATH_ = 'C:\dev\AAE000J170503066 (U7.47R6-11)\RF_DVT_TC1\FF\DynBW_170522'
        if self._CSV_FILE_PATH_== '':
            self.popupWin.setText("please select a Path")
            self.popupWin.show()
            return
        
        #self._CSV_FILE_PATH_ = 'C:\dev\AAE000J170503066 (U7.47R6-11)'
        try:
            self._getSerialNumber_(self._CSV_FILE_PATH_)
            self.label.setText(self._CSV_FILE_PATH_)
        except:
            self.popupWin.setText('Invalid Directory, Please select a Directory with scorecard files')
            self.popupWin.show()
            logger.error(self.current_time + ' Can not find scorecard files')
            return
        logger.info('Opened a directory')
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

