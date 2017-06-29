'''
Created on Jun 26, 2017

@author: Khoa Au
kau@kymetacorp.com
'''



from matplotlib import pyplot as plt
import os
import pandas as pd
from datetime import datetime
import json
from sparmsPkg.s2p_calculations import S2PDataProcessing as DP
import math
import re
import glob
class scError(Exception):
    pass

"""
This callable object is capable of generating firstpass summary and sidelobe summary.
For firstpass. This object expects the 3 different directory paths, BroadSide_dyn, Off_Broadside, and S2P path. Usually from the Optimization 
Best dyn
For sideLobe. This object expect 1 scorecard path. Could be any path from the FF Folder that contains scorecards.
This class generally filters the scorecard in a way that only the row with appropriate json bounds (freq,pol) are captured and appended to the 
dataframe.
"""

class reportGenerator():
    
    
    
    
    def __init__(self,saveFilePath,reportType,sideLobe_csv_path=None,FFBroadSide_csv_path = None,FFOffBroadSide_csv_path=None,s2pFileOpen=None):
        self.antenna_serial_number = ''
        self.antenna_build_number =''
        self.type_of_scan = ''
        #perform basic input validation
        if ((sideLobe_csv_path) == "" or (saveFilePath) == ""):
            print "Warning: either csv path or s2p is missing"
        if reportType == "sidelobe" or reportType == "firstpass":
            pass
        else:
            raise scError("invalid process type")
        
        if FFBroadSide_csv_path is not None:
            self.ff_broadside_path = FFBroadSide_csv_path
            self._getSerialNumber_(FFBroadSide_csv_path)
        else:
            print scError ("Warning: missing firstpass Broadside scorecard path")
        if FFOffBroadSide_csv_path is not None:
            self.ff_offbroadside_path = FFOffBroadSide_csv_path
        else:
            print scError ("Warning: missing firstpass Off Broadside scorecard path")
        if sideLobe_csv_path is not None:
            self.csv_file_path = sideLobe_csv_path
            self._getSerialNumber_(sideLobe_csv_path)
        
        self.s2p_file_path = s2pFileOpen
        self.file_name = ""
        self.process_type = reportType
        self.pattern_freq_rx = 0.0
        self.pattern_lpa_rx = 0
        self.pattern_freq_tx = 0.0
        self.pattern_lpa_tx = 0
       
        self.csv_export_path =saveFilePath
        self.pattern_theta = 0.0
        self.pattern_lpa = 0.0
        with open('freq_cal_dict.txt') as inFile:
            self.freq_dictionary = json.load(inFile)
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.print_time =datetime.now().strftime('%Y%m%d%H%M%S')
        self.csv_frame = pd.DataFrame()#csv dataFrame

    """
    The following methods gernerates appropriate reports
    @def: generateFirstPass method will generate a concatinated dataframe containing frequencies vs gain 
    for offbroadside and broadside across all available frequencies. The filtered angles are LPA90P0T0, LPA0P0T0, and LPA0P0T60.
    Base on these bounds, a new formatted dataframe is produced for more readability 
    """
    def generateFirstPass(self):
        header = ['frequency','Gain_dBi','Pattern_LPA','Pattern_PHI','Pattern_THETA','Frequencies (GZ)','Optimized S21 + cal (dBi) LPA90P0T0','Theoretical Directivity','Directivity_dB']  
        combined_csv = pd.concat([self.process('broadside'),self.process('offbroadside')])
        combined_csv = combined_csv.ix[( (combined_csv['frequency']>13.0 ) &  (combined_csv['Pattern_LPA']==90.0) & (combined_csv['Pattern_PHI']==0.0) & (combined_csv['Pattern_THETA']==0))   | ( (combined_csv['frequency']>13.0 ) & (combined_csv['Pattern_LPA']==0.0) & (combined_csv['Pattern_PHI']==0.0) & (combined_csv['Pattern_THETA']==0.0))  | ( (combined_csv['frequency']>13.0 )& (combined_csv['Pattern_LPA']==90.0) & (combined_csv['Pattern_PHI']==0.0) & (combined_csv['Pattern_THETA']==60.0))   | ( (combined_csv['frequency']>13.0 )& (combined_csv['Pattern_LPA']==0.0) & (combined_csv['Pattern_PHI']==0.0) & (combined_csv['Pattern_THETA']==60.0))  ]
        combined_csv = combined_csv.reset_index(drop = True)
        #reduced_df = df.ix[(df['frequency']==float(self.pattern_freq_tx)) & (df['pol'] == float(self.pattern_lpa_tx))]
        result = pd.concat([combined_csv,self.processS2P()],axis = 1)
        result.to_csv(os.path.join(self.csv_export_path, self.antenna_serial_number +'_'+self.antenna_build_number+"_"+self.type_of_scan+self.print_time+'_FirstpassReport.csv'),columns = header,index = False)
        print "csv successfully generated"
        
        """
        Forget plotting!
        plt.xlabel('frequencies (GZ)')
        plt.plot(result['Frequencies (GZ)'],result['Optimized S21 + cal (dBi) LPA90P0T0'],label= "Optimized S21 + cal (dBi) LPA90P0T0")
        plt.plot(result['Frequencies (GZ)'],result['Theoretical Directivity'],label = 'Theoretical Directivity')
        l0p0t0 = result.ix[(result['Pattern_LPA']==0) & (result['Pattern_PHI']==0) & (result['Pattern_THETA']==0)]
        print l0p0t0['frequency']
        plt.plot(result['Frequencies (GZ)'],l0p0t0['Gain_dBi'],label = 'LPA0P0T)')
        plt.legend(loc="upper right", bbox_to_anchor=[1,1],ncol=1, shadow=True)
        plt.grid()
        """
    def generateSideLobe(self):
        header = ['Pattern_FREQ_RX','Pattern_FREQ_TX','Pattern_LPA','Theta_deg','phi','xpd','Sidelobe_1_dBc','Sidelobe_1_deg','Sidelobe_2_dBc','Sidelobe_2_deg'] 
        self.process('sidelobe')
        #self._plot_()
        self.csv_frame.to_csv(os.path.join(self.csv_export_path,'Score_Card_Summary ' + self.antenna_serial_number + ' ' + '(' + self.antenna_build_number + ')_'+ self.type_of_scan+"_"+self.print_time +'.csv' ),encoding = 'utf-8',columns = header,index = False)
    def parseFreq(self,file):
        return ''.join(re.findall('_f=(.*?)_L', file))
    def processS2P(self):    
        num = 4.5479  #4* math.pow(3.14159,2)*math.pow(0.34, 2)- math.pow(0.02,2) 
        fre = []
        gain_at_freq = []
        directivity = []
        s2p_frame = pd.DataFrame()
        os.chdir(self.s2p_file_path)
        #iterate throught the files that contain the s2p files 
        for file in glob.glob("*.s2p"):
            giga_freq = float(self.parseFreq(file))*1e-9
            fre.append(giga_freq)
            mys2p = DP(os.path.join(self.s2p_file_path,file))
            for key in self.freq_dictionary:
                if key == self.parseFreq(file):
                    value = float(self.freq_dictionary[key]) + float(mys2p.s21_gain_at_frequency(int(self.parseFreq(file)), return_nearest = False)) 
                    gain_at_freq.append(value)
                        
            directivity.append(abs(10*math.log10(num/  math.pow(0.3/giga_freq,2)   )))
                
        s2p_frame.insert(0, column = "Frequencies (GZ)", value = fre)
        s2p_frame.insert(1, column = "Optimized S21 + cal (dBi) LPA90P0T0", value = gain_at_freq)
        s2p_frame.insert(2, column = 'Theoretical Directivity',value = directivity)
        s2p_frame = s2p_frame.ix[s2p_frame['Frequencies (GZ)'] >13.0 ]
        s2p_frame=s2p_frame.reset_index(drop = True)
        return s2p_frame
    def process(self,ffType):
        csv_frame = pd.DataFrame()
        if ffType == 'broadside':
            directory_path = self.ff_broadside_path
            print "processing broadside data"
        elif ffType =='offbroadside':
            directory_path = self.ff_offbroadside_path
            print "processing offbroadside data"
            
        list = []
        if self.process_type == 'sidelobe':
            directory_path = self.csv_file_path
            colHeader = ['Theta_deg','phi','xpd','Sidelobe_1_dBc','Sidelobe_1_deg','Sidelobe_2_dBc','Sidelobe_2_deg','pol','frequency']
        elif self.process_type =='firstpass':
            colHeader = ['frequency','Gain_dBi','pol','Directivity_dB'] #read the appropriate data to save memory
                
        #print colHeader
        
        for file in sorted(os.listdir(directory_path)):
            if self.isScoreCard (file):
                #print file
                df = pd.read_csv(os.path.join(directory_path,file),usecols = colHeader)
                #print df
                #if found a score card, check if it is a Tx scorecard or a Rx score card?
                if ('_Rx_' in file):
                    self.parseRxJson(self.getRxJsonName(file),directory_path)
                    reduced_df = df.ix[(df['frequency']==float(self.pattern_freq_rx)) & (df['pol'] == float(self.pattern_lpa_rx))]
                    reduced_df.insert(0, column = 'Pattern_FREQ_RX', value =self.pattern_freq_rx)
                    reduced_df.insert(0, column = 'Pattern_LPA', value =self.pattern_lpa_rx)
                    reduced_df.insert(0, column = 'Pattern_PHI', value =self.pattern_phi)
                    reduced_df.insert(0, column = 'Pattern_THETA', value =self.pattern_theta)
                    list.append(reduced_df)
                elif ('_Tx_' in file):
                    #logger.info(self.current_time + ' Found a Tx scorecard')
                    if ('_RxRef_' in file): #indication of MiniPostOpt Scan
                        self.parseTxJson(self.getTxJsonNameMiniPostOpt(file),directory_path)
                        
                    else:
                        self.parseTxJson(self.getTxJsonName(file),directory_path)
                        reduced_df = df.ix[(df['frequency']==float(self.pattern_freq_tx)) & (df['pol'] == float(self.pattern_lpa_tx))]
                        reduced_df.insert(0, column = 'Pattern_FREQ_TX', value =self.pattern_freq_tx)
                        reduced_df.insert(0, column = 'Pattern_LPA', value =self.pattern_lpa_tx)
                        reduced_df.insert(0, column = 'Pattern_PHI', value =self.pattern_phi)
                        reduced_df.insert(0, column = 'Pattern_THETA', value =self.pattern_theta)
                        list.append(reduced_df)
        self.csv_frame = pd.concat(list)
        self.csv_frame.sort_values(by =['pol','Pattern_PHI','Pattern_THETA'], ascending = True, inplace = True)
        return self.csv_frame
        
    def isScoreCard (self,file):
        count = 0
        string = 'scorecard'
        return string in file  
    
    def _plot_(self):
        sideLobe1PosTx = []
        sideLobe2PosTx = []
        sideLobe1PosRx = []
        sideLobe2PosRx = []
        
        sideLobe1NegTx = []
        sideLobe2NegTx = []
        sideLobe1NegRx = []
        sideLobe2NegRx = []
        plt.cla()
        
        for index,row in self.csv_frame.iterrows():
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
        
        
    def _getSerialNumber_(self,antenna_path):
        #get a score_card file
        sc_file = ''
        self.type_of_scan = os.path.basename(os.path.normpath(antenna_path))
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
                self.antenna_serial_number = self.antenna_serial_number + c
        start,end = str(antenna_path).split(self.antenna_serial_number)
        dummy = ''
        for d in end:
            if d == ')':
                break
            elif d is not '(' and d is not ' ':
                self.antenna_build_number = self.antenna_build_number + d   
    """
    The parse tx/rx methods below reads the value by key in the corresponding json files and
    save those value into appropriate global variables
    @param tx_name:generated/parsed by the method getTx
    @param rx_name:generated/parsed by the method getRx:  
    """    
    def parseTxJson(self,tx_name,csv_path):
        #reiterate through the folder again to find the appropriate tx jason
        os.chdir(csv_path)
        for file in glob.glob("*.json"):
                #check for tx name
            if tx_name in file:
                    #read that file
                my_data = json.load(open(os.path.join(csv_path,file)))
                    #print 'tx json freqeuncy values: ' + str(my_data['TX']['Pattern_FREQ'])
                self.pattern_freq_tx = my_data['TX']['Pattern_FREQ']
                self.pattern_lpa_tx = my_data['TX']['Pattern_LPA']
                self.pattern_theta = my_data['TX']['Pattern_THETA']
                self.pattern_phi = my_data['TX']['Pattern_PHI']
                    #print str(self.pattern_freq_tx) + ' , ' +str(self.pattern_lpa_tx)
    def parseRxJson(self,rx_name,csv_path):
        os.chdir(csv_path)
        for file in glob.glob("*.json"):
                #check for tx name
            if rx_name in file:
                    #read that file
                my_data = json.load(open(os.path.join(csv_path,file)))
                #print 'tx json freqeuncy values: ' + str(my_data['RX']['Pattern_FREQ'])
                #save the appropriate data 
                self.pattern_freq_rx = my_data['RX']['Pattern_FREQ']
                self.pattern_lpa_rx = my_data['RX']['Pattern_LPA']
                self.pattern_theta = my_data['RX']['Pattern_THETA']
                self.pattern_phi = my_data['RX']['Pattern_PHI']
                    #print str(self.pattern_freq_rx) + ' , ' + str(self.pattern_lpa_rx)

    def getRxJsonName(self,my_scorecard):
        #logger.debug(self.current_time + ' Rx Json Name is:' + my_scorecard.split('_',2)[1])
        return my_scorecard.split('_',2)[1]
    def getTxJsonName(self,my_scorecard):
        #logger.debug(self.current_time + ' Tx Json Name is:' + my_scorecard.split('_',3)[2])
        return my_scorecard.split('_',3)[2]
    def getTxJsonNameMiniPostOpt(self,my_scorecard):
        #logger.debug(self.current_time + ' Tx Minipost Opt Json Name is:' + my_scorecard.split('_',4)[3])
        return my_scorecard.split('_',4)[3]    
    
if __name__ == "__main__":
    #reportGenerator = reportGenerator(csvFileOpen ="C:\dev\AAE000J170503066 (U7.47R6-11)\RF_DVT_TC1\FF\Scan_Roll_Off_170520",s2pFileOpen = "",saveFilePath = "C:\dev\Test3\ExportTest",reportType="sidelobe")
    #reportGenerator = reportGenerator(csvFileOpen ="C:\dev\AAE000J170503066 (U7.47R6-11)\RF_DVT_TC1\FF\Scan_Roll_Off_170520",s2pFileOpen = "",saveFilePath = "C:\dev\Test3\ExportTest",reportType="sidelobe")
    #reportGenerator.process()
    print 'test'
    #reportGeneratorSL = reportGenerator(sideLobe_csv_path ="C:\dev\AAE000J170503066 (U7.47R6-11)\RF_DVT_TC1\FF\Scan_Roll_Off_170520",s2pFileOpen = "",saveFilePath = "C:\dev\Test3\ExportTest",reportType="sidelobe")
    #reportGeneratorSL.generateSideLobe()
    reportGeneratorFF = reportGenerator(FFOffBroadSide_csv_path="C:\dev\AAE000J170417056 (U7.47R6-01)\FF\RF_First_Pass\Off_Broadside",FFBroadSide_csv_path="C:\dev\AAE000J170417056 (U7.47R6-01)\FF\RF_First_Pass\Broadside_DBW",s2pFileOpen = "C:\dev\AAE000J170417056 (U7.47R6-01)\Opt\dynBW_1_best",saveFilePath = "C:\dev\Test3\ExportTest",reportType="firstpass")
    reportGeneratorFF.generateFirstPass()
    #reportGeneratorFF2 = reportGenerator(csvFileOpen ="K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)\mTCBA-170622-01 (Ku70TFT5.1-X3-C7)\FF\Post_Opt_170622",s2pFileOpen = "K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)\mTCBA-170622-01 (Ku70TFT5.1-X3-C7)\Opt\SO_dynBW_1_best",saveFilePath = "C:\dev\Test3\ExportTest",reportType="firstpass")
    #reportGeneratorFF2.processS2P()
    #reportGeneratorFFC8 = reportGenerator(csvFileOpen ="K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)\mTCBA-170623-01 (Ku70TFT5.1-X3-C8)\FF\Post_Opt_170623",s2pFileOpen = "K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)\mTCBA-170623-01 (Ku70TFT5.1-X3-C8)\Opt\SO_dynBW_1_best",saveFilePath = "C:\dev\Test3\ExportTest",reportType="firstpass")
    #reportGeneratorFFC8.processS2P()
    
    
    
    
    
    
    