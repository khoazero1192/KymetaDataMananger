# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportGen.ui'
#
# Created: Mon Jun 26 11:53:53 2017
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import wx
from LoggingUtil import XStream,QtHandler
import logging
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from datetime import datetime
import math
#import scProcessor.reportGenerator
import scProcessor
import matplotlib.pyplot as plt
from scProcessor import reportGenerator

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
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        #print_time =datetime.now()
    csv_file_path = ''
    def setupUi(self, Form):
        app = wx.App(False)
        w, h = wx.GetDisplaySize()
        print w,h
        
        
        self.popupWin = QtGui.QMessageBox(Form)
        self.popupWin.setWindowTitle('Warning')

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(w-50,h-50)
        self.tab2 = QtGui.QTabWidget(Form)
        self.tab2.setGeometry(QtCore.QRect(20, 20, w-100,h-120))
        self.tab2.setObjectName(_fromUtf8("tab2"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, h/8, w/4.5,h/10))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.SaveDirButt = QtGui.QPushButton(self.verticalLayoutWidget)
        self.SaveDirButt.setObjectName(_fromUtf8("SaveDirButt"))
        self.verticalLayout.addWidget(self.SaveDirButt)
        self.SaveDirTE = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.SaveDirTE.setObjectName(_fromUtf8("SaveDirTE"))
        self.verticalLayout.addWidget(self.SaveDirTE)
        self.formLayoutWidget = QtGui.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10,h/4,w/4.5,h/5))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        
        self.SidelobeDirButt = QtGui.QPushButton(self.formLayoutWidget)
        self.SidelobeDirButt.setObjectName(_fromUtf8("SidelobeDirButt"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.SidelobeDirButt)
        self.FirstpassS2PButt = QtGui.QPushButton(self.formLayoutWidget)
        self.FirstpassS2PButt.setObjectName(_fromUtf8("FirstpassS2PButt"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.FirstpassS2PButt)
        self.FirstpassBroadsideButt = QtGui.QPushButton(self.formLayoutWidget)
        self.FirstpassBroadsideButt.setObjectName(_fromUtf8("FirstpassBroadsideButt"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.FirstpassBroadsideButt)
        self.SideLobeTE = QtGui.QTextEdit(self.formLayoutWidget)
        self.SideLobeTE.setObjectName(_fromUtf8("SideLobeTE"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.SideLobeTE)
        self.FirstpassS2PTE = QtGui.QTextEdit(self.formLayoutWidget)
        self.FirstpassS2PTE.setObjectName(_fromUtf8("FirstpassS2PTE"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.FirstpassS2PTE)
        self.FirstpassSCVTE = QtGui.QTextEdit(self.formLayoutWidget)
        self.FirstpassSCVTE.setObjectName(_fromUtf8("FirstpassSCVTE"))
        self.FirstpassOffBroadsideButt = QtGui.QPushButton(self.formLayoutWidget)
        self.FirstpassOffBroadsideTE = QtGui.QTextEdit(self.formLayoutWidget)
        self.formLayout.setWidget(3,QtGui.QFormLayout.LabelRole,self.FirstpassOffBroadsideButt)
        self.formLayout.setWidget(3,QtGui.QFormLayout.FieldRole,self.FirstpassOffBroadsideTE)
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.FirstpassSCVTE)
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, h/2, w/4.5, h/5))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.processFFButt = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.processFFButt.setObjectName(_fromUtf8("processFFButt"))
        self.horizontalLayout.addWidget(self.processFFButt)
        self.ProcessSidelobeButt = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ProcessSidelobeButt.setObjectName(_fromUtf8("ProcessSidelobeButt"))
        self.horizontalLayout.addWidget(self.ProcessSidelobeButt)
        
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(479, 20, w/2, h/1.5))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
    
        """
        Default the mode to firstpass mode
        """
        self.ffCheckBox = QtGui.QRadioButton()
        self.ffCheckBox.setText('First Pass')
        self.ffCheckBox.setChecked(1)
        self.ProcessSidelobeButt.setDisabled(1)
        self.SidelobeDirButt.setDisabled(1)
        self.SideLobeTE.setDisabled(1)
        
        
        self.slCheckBox = QtGui.QRadioButton()
        self.slCheckBox.setText('Side Lobe')
        
        self.ffCheckBox.toggled.connect(self.checkFF)
        self.ffCheckBox.toggled.connect(self.checkSL)
        
        self.checkButtonLayoutWidget = QtGui.QWidget(self.tab)
        self.checkButtonLayoutWidget.setGeometry(QtCore.QRect(20,0,w/5,100))
        
        self.checkButtonLayout = QtGui.QHBoxLayout(self.checkButtonLayoutWidget)
        self.checkButtonLayout.addWidget(self.ffCheckBox)
        self.checkButtonLayout.addWidget(self.slCheckBox)
        
        self._console = QtGui.QTextBrowser()   
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText ) 
        self.verticalLayout_2.addWidget(self._console)
        
        logger.info("First Pass Mode generated")
        
        self.tab2.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tab2.addTab(self.tab_2, _fromUtf8(""))
        
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20,60, w-200, h-250))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.tab_2)
        
        
        #tab 2 section for table of sidelobes data
        self.verticalLayout_3.addWidget(self.canvas)
        self.retranslateUi(Form)
        self.tab2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        QtCore.QObject.connect(self.SaveDirButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.openDir)
        QtCore.QObject.connect(self.SidelobeDirButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.openSidelobeDir)
        QtCore.QObject.connect(self.FirstpassBroadsideButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.openFirstpass_broadside)
        QtCore.QObject.connect(self.FirstpassS2PButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.openFirstpassS2P)
        QtCore.QObject.connect(self.processFFButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.processFirstpass)
        QtCore.QObject.connect(self.ProcessSidelobeButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.processSideLobe)
        QtCore.QObject.connect(self.FirstpassOffBroadsideButt,QtCore.SIGNAL(_fromUtf8("clicked()")),self.openFirstpass_offbroadside)
        
        
    
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Report Generator", None))
        self.SaveDirButt.setText(_translate("Form", "Save Directory", None))
        self.SidelobeDirButt.setText(_translate("Form", "Sidelobe Dir", None))
        self.FirstpassS2PButt.setText(_translate("Form", "Firstpass s2p", None))
        self.FirstpassBroadsideButt.setText(_translate("Form", "Firstpass Broadside", None))
        self.FirstpassOffBroadsideButt.setText(_translate("Form", 'Firstpass OffBroad', None))
        self.processFFButt.setText(_translate("Form", "Process First Pass", None))
        self.ProcessSidelobeButt.setText(_translate("Form", "Process Sidelobe", None))
        self.tab2.setTabText(self.tab2.indexOf(self.tab), _translate("Form", "Core", None))
        self.tab2.setTabText(self.tab2.indexOf(self.tab_2), _translate("Form", "Plotting", None))
    def checkFF(self):
        if self.ffCheckBox.isChecked():
            logger.info("First Pass Generator Selected")
            self.processFFButt.setEnabled(1)
            self.ProcessSidelobeButt.setDisabled(1)
            self.SidelobeDirButt.setDisabled(1)
            self.SideLobeTE.setDisabled(1)
            self.FirstpassBroadsideButt.setDisabled(0)
            self.FirstpassS2PButt.setDisabled(0)
            self.FirstpassS2PTE.setDisabled(0)
            self.FirstpassSCVTE.setDisabled(0)
            self.FirstpassOffBroadsideButt.setDisabled(0)
            self.FirstpassOffBroadsideTE.setDisabled(0)
        
    def checkSL(self):
        if self.slCheckBox.isChecked():
            logger.info("Side Lobe generator Selected")
            self.processFFButt.setDisabled(1)
            self.ProcessSidelobeButt.setEnabled(1)
            self.SidelobeDirButt.setDisabled(0)
            self.SideLobeTE.setDisabled(0)
            self.FirstpassBroadsideButt.setDisabled(1)
            self.FirstpassS2PButt.setDisabled(1)
            self.FirstpassS2PTE.setDisabled(1)
            self.FirstpassSCVTE.setDisabled(1)
            self.FirstpassOffBroadsideButt.setDisabled(1)
            self.FirstpassOffBroadsideTE.setDisabled(1)
    
    def openDir(self):
        
        self.SaveDirTE.setText('C:\dev\Test3\ExportTest')
        #self.csv_file_path = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory", "C:\\"))
        #self.SaveDirTE.setText(self.csv_file_path)
        logger.info(self.current_time + 'opened a a directory')
        
    def openSidelobeDir(self):
        self.SideLobeTE.setText('C:\dev\AAE000J170503066 (U7.47R6-11)\RF_DVT_TC1\FF\Scan_Roll_Off_170520')
        #self.csv_file_path = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.SideLobeTE.setText(self.csv_file_path)
        logger.info('opened a sidelobe directory')
        
    def openFirstpass_broadside(self):
        self.FirstpassSCVTE.setText('C:\dev\AAE000J170417056 (U7.47R6-01)\FF\RF_First_Pass\Broadside_DBW')
        #self.csv_file_path = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory"))
        #self.FirstpassSCVTE.setText(self.csv_file_path)
        logger.info('opened a firstpass broadside folder')
    def openFirstpassS2P(self):
        self.FirstpassS2PTE.setText('C:\dev\AAE000J170417056 (U7.47R6-01)\Opt\dynBW_1_best')
        #self.csv_file_path = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory"))
        #self.FirstpassS2PTE.setText(self.csv_file_path)
        logger.info('opeend a firstpass s2p directory')
    def openFirstpass_offbroadside(self):
        self.FirstpassOffBroadsideTE.setText('C:\dev\AAE000J170417056 (U7.47R6-01)\FF\RF_First_Pass\Off_Broadside')
        #self.csv_file_path = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory"))
        #self.FirstpassOffBroadsideTE.setText(self.csv_file_path)
        logger.info('opened a firstpass offbroadside foler')
    def processFirstpass(self):
        if ( (str(self.FirstpassS2PTE.toPlainText()) == "")) :
            self.popupWin.setText(" Please indicate Offbroadside, Broadside and S2P directory")
            self.popupWin.show()
            return
        #print self.FirstpassOffBroadsideTE.toPlainText()
        reportGeneratorFF = scProcessor.reportGenerator(FFOffBroadSide_csv_path=str(self.FirstpassOffBroadsideTE.toPlainText()),FFBroadSide_csv_path=str( self.FirstpassSCVTE.toPlainText()) ,s2pFileOpen = str(self.FirstpassS2PTE.toPlainText()),saveFilePath = str(self.SaveDirTE.toPlainText()),reportType="firstpass")
        reportGeneratorFF.generateFirstPass()
        self.canvas.draw()
        logger.info('report generated succesfully')
        logger.info('Report saved in :' + str(self.SaveDirTE.toPlainText()))
    def processSideLobe(self):    
        logger.info('ready to process side Lobe data')
        print self.SideLobeTE.toPlainText()
        #if (str(self.SideLobeTE.toPlainText() == "")):
            #self.popupWin.setText(("Please indicate Side Lobe directory"))
            #self.popupWin.show()
            #return
        reportGeneratorSL = scProcessor.reportGenerator(sideLobe_csv_path =str(self.SideLobeTE.toPlainText()),saveFilePath = str(self.SaveDirTE.toPlainText()),reportType="sidelobe")
        reportGeneratorSL.generateSideLobe()
        reportGeneratorSL._plot_()
        self.canvas.draw()
        logger.info('report generated succesfully')
        logger.info('report saved in:'+ str(self.SaveDirTE.toPlainText()))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

