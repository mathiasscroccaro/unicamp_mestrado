#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import serial
from pyqtgraph import QtCore, QtGui
import pyqtgraph
from time import sleep


class serialThread(QtCore.QThread):
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.serial = serial.Serial()
        self.sinalRecebeuDado = QtCore.SIGNAL("RecebeuDado")
        
    def __del__(self):
        self.exit(0)
    
    def run(self):
        dados = []
        self.serial.flush()
        while (True):
            dado = self.serial.read(1)
            
            if (dado == '\n'):
                dados = int(''.join(dados))
                self.emit(self.sinalRecebeuDado,dados)
                dados = []
            else:
                dados.append(dado)
    
    def enviarSerial(self,valor):
        self.serial.write(valor)



class Interface(QtGui.QWidget):
    
    def __init__(self):
        super(Interface, self).__init__()
        
        self.iniciaWidgets()
        
    def iniciaWidgets(self):
        
        self.alarme = "0"
        self.atuador = "0"
        
        # Cria os objetos widgets de interação com o usuário
        
        self.labelBaudRate = QtGui.QLabel("Velocidade de conexao:",self)
        self.labelPorta = QtGui.QLabel("Porta de conexao\ncom Arduino:",self)
        self.inputBaudRate = QtGui.QLineEdit("9600",self)
        self.inputPorta = QtGui.QLineEdit("/dev/ttyACM0",self)
        self.grafico = pyqtgraph.PlotWidget(self)
        self.botaoConexao = QtGui.QPushButton("Conectar",self)
        
        self.dadosVisiveis = []
        self.curva = pyqtgraph.PlotCurveItem()
        self.grafico.addItem(self.curva)
        
        self.inputSetPoint = QtGui.QLineEdit("18",self)
        self.inputHisterese = QtGui.QLineEdit("1",self)
        self.inputAlarme = QtGui.QLineEdit("30",self)
        
        self.labelSetPoint = QtGui.QLabel("SetPoint:",self)
        self.labelHisterese = QtGui.QLabel("Histerese:",self)
        self.labelAlarme = QtGui.QLabel("Alarme:",self)
        
        # Cria threads para comunicação serial
        self.serialCom = serialThread()
        
        # Reposiciona os objetos criados na GUI
                
        self.labelBaudRate.move(610,80)
        self.labelPorta.move(610,15)
        self.inputBaudRate.move(610,100)
        self.inputPorta.move(610,50)
        self.botaoConexao.move(610,130)
        self.grafico.move(0,0)
        
        self.inputSetPoint.move(610,210)
        self.inputHisterese.move(610,280)
        self.inputAlarme.move(610,350)
        
        self.labelHisterese.move(610,255)
        self.labelSetPoint.move(610,185)
        self.labelAlarme.move(610,325)
        # Redimensionando os objetos
        
        self.grafico.resize(600,600)
        self.grafico.setXRange(0,100)
        self.grafico.setYRange(15,35)
        
        self.grafico.setBackground(0)
        
        # Conecta sinais dos objetos
        
        self.botaoConexao.clicked.connect(self.conectarSerial)
        #self.inputAlarme.textChanged.connect(self.enviarSerial)
        #self.inputHisterese.textChanged.connect(self.enviarSerial)
        #self.inputSetPoint.textChanged.connect(self.enviarSerial)
        
        # Alterando parâmetros da janela principal 
        
        self.connect(self.serialCom,self.serialCom.sinalRecebeuDado,self.atualizaGrafico)
        
        self.resize(800,600)
        self.setWindowTitle('Leitura da temperatura do Arduino')
        self.show()
        
    def conectarSerial(self):
        
        if (self.botaoConexao.text() == "Conectar"):
              
            self.serialCom.serial.baudrate = int(self.inputBaudRate.text())
            self.serialCom.serial.port = str(self.inputPorta.text())
            self.serialCom.serial.timeout = float(3)
        
            try:
                self.serialCom.serial.open()
                self.serialCom.start()
                self.botaoConexao.setText("Desconectar")
            except:
                print("Erro ao conectar!")
        else:
            self.botaoConexao.setText("Conectar")
            self.serialCom.serial.close()
            self.serialCom.exit()        
    
    
    def atualizaGrafico(self,dado):
                
        dado = (dado/1023.0)*20.0+15
        
        antigo = self.atuador
        
        if (dado > float(self.inputSetPoint.text()) + float(self.inputHisterese.text())):
            self.atuador = "0"
        elif (dado < float(self.inputSetPoint.text()) - float(self.inputHisterese.text())):
            self.atuador = "1"
        else:
            self.atuador = "0"
        
        if (self.atuador is not antigo):
            self.serialCom.enviarSerial(self.alarme + self.atuador)
            
        
        antigo = self.alarme
        
        if (dado > float(self.inputAlarme.text())):
            self.alarme = "1"
            self.grafico.setBackground(0)
        else:
            self.alarme = "0"
            self.grafico.setBackground("default")
        
        if (self.alarme is not antigo):
            self.serialCom.enviarSerial(self.alarme + self.atuador)
        
        self.dadosVisiveis.append(dado)
        if (len(self.dadosVisiveis) == 100):
            del self.dadosVisiveis[0]
        self.curva.setData(self.dadosVisiveis)

        
def main():
    
    
    app = QtGui.QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
