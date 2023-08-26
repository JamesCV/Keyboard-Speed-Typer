def calcSpeedScore(answerLen, duration):
    return (answerLen / duration)*100

def calcBonusScore(mistakeCount):
    if (mistakeCount == 0):
        return 100
    elif (mistakeCount <= 3):
        return 25
    else:
        return 0

def getAccuracyMultiplier(answerLen, mistakeCount):
    return ((answerLen - mistakeCount) / answerLen * 100)/100

def getDifficultyMultiplier(difficulty):
    if (difficulty == "Easy"):
        return 0.50
    elif (difficulty == "Mild"):
        return 1.00
    elif (difficulty == "Difficult"):
        return 1.50
    elif (difficulty == "Extreme"):
        return 2.00

def calculateCoins(speedScore, bonusScore, accuracyMultiplier, difficultyMultiplier):
    return ((speedScore+bonusScore) * difficultyMultiplier)*accuracyMultiplier
