from threading import Thread
from reach_rpc import mk_rpc
import time

def main():
    rpc, rpc_callbacks = mk_rpc()
    starting_balance = rpc("/stdlib/parseCurrency", 100)
    player_1 = input("Enter your name player1: ")
    player_2 =input("Enter your name player2: ")
    player_3 = input("Enter your name player3: ")
    acc_p1 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_p2 = rpc("/stdlib/newTestAccount", rpc("/stdlib/parseCurrency", 20))
    acc_p3 = rpc("/stdlib/newTestAccount", rpc("/stdlib/parseCurrency", 50))
    NFT = rpc('/stdlib/launchToken', acc_p1, 'te', 'Te', 1)
    print("The nft generated: %s"%NFT)

    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))
    def get_bal(w,r):
        return rpc('/stdlib/balanceOf', w, r)
    def get_address(s):
        return(rpc("/acc/getAddress", s))


    n1 = NFT['token']['id']
    n2 = rpc("/stdlib/bigNumberToNumber", n1)

    before_p1 = get_balance(acc_p1)
    before_p2 = get_balance(acc_p2)
    before_p3 = get_balance(acc_p3)

    print("%s starting balance is %s algo" %(player_1,before_p1))
    print("%s starting balance is %s algo"%(player_2,before_p2))
    print("%s starting balance is %s algo"%(player_3,before_p3))
    print(" the nft id is %s" %n2)
    bp1nft = get_bal(acc_p1, n1)
    bp2nft = get_bal(acc_p2, n1)
    bp3nft = get_bal(acc_p3, n1)
    print("%s has 1 token"%player_1)
    print("%s has 0 tokens"%player_2)
    print("%s has 0 tokens"%player_3)
    player2_address = get_address(acc_p2)
    player3_address = get_address(acc_p3)

    ctc_p1 = rpc("/acc/contract", acc_p1)

    def User1():
        minPrice = input("what is the amount for whitelist: ")
        
        rpc_callbacks(
            "/backend/User1",
            ctc_p1,
            dict( getnftid =  rpc("/stdlib/bigNumberToNumber",NFT['token']['id']),minPrice = minPrice)
        )
    Usr1 = Thread(target=User1)
    Usr1.start()

    def User2():
        def getbal():
            return before_p2

        def seetok(ids):
            rpc("/acc/tokenAccept",acc_p2,ids)
            print("%s accept token"%player_2)
        ctc_p2 = rpc("/acc/contract", acc_p2, rpc("/ctc/getInfo",ctc_p1))
        rpc_callbacks(
            "/backend/User2",
            ctc_p2,
            dict(see_token = seetok,getbal = getbal)
        )
        rpc("/forget/ctc",ctc_p2)
    Usr2 = Thread(target=User2)
    Usr2.start()

    def User3():
        def getbal():
            return before_p3

        def seetok(ids):
            rpc("/acc/tokenAccept",acc_p3,ids)
            print("%s accept token"%player_3)
        ctc_p3 = rpc("/acc/contract", acc_p3, rpc("/ctc/getInfo",ctc_p1))
        rpc_callbacks(
            "/backend/User3",
            ctc_p3,
            dict(see_token = seetok,getbal = getbal)
        )
        rpc("/forget/ctc",ctc_p3)
    Usr3 = Thread(target=User3)
    Usr3.start()

    Usr1.join()
    Usr2.join()
    Usr3.join()

    p1nft = get_bal(acc_p1, n1)
    p2nft = get_bal(acc_p2, n1)
    p3nft = get_bal(acc_p3, n1)
    if bp1nft == p1nft:
        print("No transfer was made by %s" %player_1)
    else:
        print("%s made transfer to the whitelisted address" %player_1)
    if bp2nft == p2nft:
        print("%s wasn't whitelisted hence recieved 0 tokens" %player_2)
    else:
        print("%s was whitelisted and recieved 1 token\n Address: %s" %(player_2, player2_address ))
    if bp3nft == p3nft:
        print("%s wasn't whitelisted hence 0 tokens" %player_3)
    else:
       print("%s was whitelisted and recieved 1 token\n Address: %s" %(player_3,player3_address ))

    rpc("/forget/acc", acc_p1,acc_p2,acc_p3)
    rpc("/forget/ctc", ctc_p1)
if __name__ == "__main__":
    main()
       

