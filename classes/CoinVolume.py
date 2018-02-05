import requests
import time, datetime

class CoinVolume(object):

    def __init__(self, name=None):

        self.name = name
        self.lastId = 0
        self.initalPrice = 0
        self.initialSellVol = 0
        self.initialBuyVol = 0
        self.currentVol = 0

        self.soldVolume = 0
        self.soldPrice = 0
        self.soldBtcVol = 0
        self.soldPerc = 0
        self.soldPercIncrease = 0
        self.soldVolIncrease = 0

        self.boughtVolume = 0
        self.boughtPrice = 0
        self.boughtBtcVol = 0
        self.boughtPerc = 0
        self.boughtPercIncrease = 0
        self.boughtVolIncrease = 0

    def initializeVars(self):
        orders = self.getOrderBook()

        self.soldPrice = orders[0]['Price']
        self.boughtPrice = orders[0]['Price']
        self.lastId = orders[0]['Id']
        for order in orders:
            if order['OrderType'] == 'BUY':
                self.boughtVolume += order['Quantity']
                self.boughtBtcVol += order['Total']

            else:
                self.soldVolume += order['Quantity']
                self.soldBtcVol += order['Total']

        self.initialSellVol = self.soldVolume
        self.initialBuyVol = self.boughtVolume

    def getOrderBook(self):
        print('Getting Order Book from: ' + self.name)
        return requests.get('https://bittrex.com/api/v1.1/public/getmarkethistory?market=' + self.name).json()['result']
        

    def calculateVolume(self):
    
        orders = self.getOrderBook()
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S')
        
        print('Request time: ' + str(st) + '\n')

        _sellVol = self.soldVolume
        _buyVol = self.boughtVolume
        _lastId = orders[0]['Id']
        for order in orders:
            if int(order['Id']) <= self.lastId:
                break
            if order['OrderType'] == 'BUY':
                self.boughtVolume += order['Quantity']
                self.boughtBtcVol += order['Total']
                print('New buy order completed: ' + str(order['Quantity']) + ' ' + self.name)

            else:
                self.soldVolume += order['Quantity']
                self.soldBtcVol += order['Total']
                print('New sell order completed: ' + str(order['Quantity']) + ' ' + self.name)

        self.lastId = _lastId

        #Calculate perc and vol increased since last request
        self.soldPerc, self.soldVolIncrease = self.calculateIncrease(self.soldVolume, _sellVol)
        self.boughtPerc, self.boughtVolIncrease = self.calculateIncrease(self.boughtVolume, _buyVol)

        self.soldPercIncrease, _ = self.calculateIncrease(self.soldVolume, self.initialSellVol)
        self.boughtPercIncrease, _ = self.calculateIncrease(self.boughtVolume, self.initialBuyVol)


    def calculateIncrease(self, newValue, oldValue):
        _increase = newValue - oldValue
        return (_increase / oldValue) * 100, _increase 


    def printLog(self):
        print('############################ {} ##########################################'.format(self.name))
        print('          Volume  ||   Change  || Volume Change || Acumulated Change')
        print('sold:     {0:.2f}'.format(self.soldVolume) + '   ||  ' +str(round(self.soldPerc, 2)) +'%    ||  ' +str(round(self.soldVolIncrease, 2)) +'         ||  ' +str(round(self.soldPercIncrease, 2)) + '%')
        print('Bought:   {0:.2f}'.format(self.boughtVolume) + '   ||  ' +str(round(self.boughtPerc, 2)) +'%     ||  ' +str(round(self.boughtVolIncrease, 2)) +'         ||  ' +str(round(self.boughtPercIncrease, 2)) + '%')

        print('############################  END  ##########################################')
        