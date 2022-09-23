# Importing the joblib module to help load the support vector classifier model
import joblib

def main():
    while True:
        startOrQuit = str(input("Press 's' to start a prediction or 'q' to quit: ")).lower()
        if startOrQuit == 'q':
            quit()
        elif startOrQuit == 's':
            allyTeamDmg = 0
            enemyTeamDmg = 0
            while True:
                try:
                    allyTeamDmg = int(input("Enter ally team damage: "))
                    enemyTeamDmg = int(input("Enter enemy team damage: "))
                    break
                except:
                    print("Invalid")
            # Loading the SVC model and predicting using input values
            svcModel = joblib.load('LoL Team Damage Win Predicter.joblib')
            predictions = svcModel.predict([[allyTeamDmg, enemyTeamDmg]])[0]
            if predictions == 0:
                print("Loss")
            elif predictions == 1:
                print("Win")
        else:
            print("Invalid")
                    
if __name__ == '__main__':
    main()