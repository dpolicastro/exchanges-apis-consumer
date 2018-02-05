from classes.CoinVolume import CoinVolume
import time
print(__name__)
print('Starting Script...')

def main(coins):

    for coin in coins:
        coin.initializeVars()
    while True:
        for coin in coins:
            coin.calculateVolume()
            coin.printLog()
        time.sleep(15) 


main([
    CoinVolume('BTC-XVG'), 
    CoinVolume('BTC-ETH')
    ])