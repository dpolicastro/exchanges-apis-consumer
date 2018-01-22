import numpy as np
import requests
from twisted.internet import task
from twisted.internet import reactor
import time, datetime
print('script working')

last = 1
ordersAdded = []
selledVolume = { 'value' : 1, 'last' : 0, 'initialVol' : 1, 'btcVol' : 1}
boughtVolume = { 'value' : 1, 'last' : 0, 'initialVol' : 1, 'btcVol' : 1}

def orderHasBeenAdded(id):
    global ordersAdded
    for orderAdded in ordersAdded:
        if orderAdded == id:
            return True
    return False

def calculateVolume(result):
    
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S')
    
    print('Request time: ' + str(st) + '\n')
    global boughtVolume, selledVolume, ordersAdded

    _sellVol = selledVolume['value']
    _buyVol = boughtVolume['value']

    for order in result:
        if not orderHasBeenAdded(order['Id']):
            if order['OrderType'] == 'BUY':
                boughtVolume['value'] += order['Quantity']
                boughtVolume['last'] = order['Price']
                boughtVolume['btcVol'] += order['Total']

                print('New buy order: ' + str(order['Quantity']))

            else:
                selledVolume['value'] += order['Quantity']
                selledVolume['last'] = order['Price']
                selledVolume['btcVol'] += order['Total']

                print('New sell order: ' + str(order['Quantity']))

            ordersAdded.append(order['Id'])
    
    increase = selledVolume['value'] - _sellVol
    selledVolume['percentDiff'] = (increase / _sellVol) * 100
    selledVolume['volDiff'] = increase

    increase = boughtVolume['value'] - _buyVol
    boughtVolume['percentDiff'] = (increase / _buyVol) * 100
    boughtVolume['volDiff'] = increase


markets = ['BTC-QTUM']
def requestMarketHistory(market):
    print('Market: ' + market)
    r = requests.get('https://bittrex.com/api/v1.1/public/getmarkethistory?market=' + market)
    result = r.json()['result'];
    #print('Result length: '+ str(len(result)))
    calculateVolume(result)
    
    global selledVolume, boughtVolume
    print('\nSelled Volume: ' + str(round(selledVolume['value'], 2)) + 
    ' || BTC Vol: '+ str(round(selledVolume['btcVol'], 2)) + 
    ' || Last: '+ str(selledVolume['last']) + 
    ' || Diff: '+str(round(selledVolume['percentDiff'], 2)) + 
    '% || Vol Diff: '+str(round(selledVolume['volDiff'], 2)))
    
    print('Bought Volume: ' + str(round(boughtVolume['value'], 2)) + 
    ' || BTC Vol: '+ str(round(boughtVolume['btcVol'], 2)) + 
    ' || Last: '+ str(boughtVolume['last']) + 
    ' || Diff: '+str(round(boughtVolume['percentDiff'], 2)) + 
    '% || Vol Diff: '+str(round(boughtVolume['volDiff'], 2)))

    print('#############################################################################')

    increase = selledVolume['value'] - selledVolume['initialVol']
    print('PODER DE COMPRA - SELLED # Value Diff: ' + str(round(increase / selledVolume['initialVol'] * 100, 2 )))

    increase = boughtVolume['value'] - boughtVolume['initialVol']
    print('PODER DE VENDA - BOUGHT # Value Diff: ' + str(round(increase / boughtVolume['initialVol'] * 100, 2 )))
    time.sleep(15)

def getInitialData():
    global selledVolume, boughtVolume
    selledVolume['initialVol'] = selledVolume['value']
    boughtVolume['initialVol'] = boughtVolume['value']

requestMarketHistory(markets[0])
getInitialData()    




while True:
    requestMarketHistory(markets[0])    