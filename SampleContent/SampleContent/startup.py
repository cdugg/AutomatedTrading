def accountSetup(which):
    accountBroker = 0
    while accountBroker not in ['1', '2', '3', '4']:
        accountBroker = input(f"""Please enter the corresponding number to the {which} Brokerage account:
        1. Ameritrade
        2. Interactive Brokers
        3. ETrade
        4. Charles Schwab\n""")
        if accountBroker not in ['1', '2', '3', '4']:
            print("Please select a valid option")
    if accountBroker == "1":
        ameritradeSetup()
    if accountBroker == "2":
        ibkrSetup()

def ameritradeSetup():
    input("To setup your Ameritrade trading app you will need to start by visiting developer.tdameritrade.com and registering an account.")
    input("Once registered go to My Apps and create a new app. Give the app whatever name and description you want. Make the callback url http://localhost. For Order Limit this program will use 60.")
    input("While we will likely never go above 20 as we are attempting to buy with sell brackets enabled we don't want to limit our ability to close positions if necessary.")
    input("Now so that we have the data retained here please go back to My Apps and open your new app once it has been approved.")
    apiKey = input("You should see in the Keys section a 'Consumer Key' copy and paste that here.\n")
    callback = input("Please enter the callback url you entered for the app here.\n")
    order_limit = input("Please enter the order limit set for your application.\n")
    app_name = input("Please enter your app name.\n")
    user = input("Please enter your ameritrade username.\n")
    password = input("Please enter your ameritrade password.\n")
    user_dev = input("Please enter your development.tdameritrade.com email.\n")
    pass_dev = input("Please enter your development.tdameritrade.com password.\n")

def ibkrSetup():
    pass

def main():
    input("""We are going to set up some stuff. Test prompts will appear and if they request input please enter ansers as requested. Otherwise press enter to continue.""")
    input("""The following will be a set of details about the mechanics of this trading system. Please read them to understand how things work.""")
    print("""Please note we will only allow the app to trade with money that exceeds $25,000, so if you have $25,001 for example we will only be trading with $1.""")
    input("""This is to protect accounts from going negative and requiring funding to follow PDT laws.""")
    input("""Additionally if an account ever falls below $25,000 you will be notified and we will not trade with either account until the funds between both are redistributed.""")
    print("""When trading we will only use the overflow equaling the minimum of the two accounts. IE if account A has $27,000 and account B has $30,000 we will only trade with $2,000 on each account.""")
    input("""Because of this we recommend redistributing the money between accounts weekly. Finding the right timing and amounts will take some getting used to.""")
    input("""If at any time you would like to go over this information again find the README file in the current folder to check again.""")
    input("""Hello and welcome to the automated trading app. I can see this is your first time using this so we will need to ask a few questions to set things up first.""")
    input("""First we will need to know the two brokerages you will be using here.""")

    accountSetup("first")
    accountSetup("second")

if __name__ == "__main__":
    main()