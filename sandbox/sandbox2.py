# sandbox2.py
# Sandbox for testing various client functions
from ib.clientportal import ClientPortal
from threading import Thread
import time


class MyClassA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print('A')
            time.sleep(1)


class MyClassB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print('B')
            time.sleep(1)


def main():
    ibc = ClientPortal()

    # resp = ClientPortal.clientrequest_authentication_status()
    # resp = ClientPortal.clientrequest_brokerage_accounts()
    # resp = ClientPortal.clientrequest_reauthenticate()
    #print(resp.statusCode)
    #print(resp.json)
    print("===== STARTING THREADS =====")

    #MyClassA()
    #MyClassB()
    print('=== main ====')
    time.sleep(30)
    ibc.watchdog_timeout = 3
    time.sleep(30)
    ibc.watchdog_timeout = 0
    time.sleep(30)
    print("==== MAIN DONE ====")


if __name__ == '__main__':
    main()