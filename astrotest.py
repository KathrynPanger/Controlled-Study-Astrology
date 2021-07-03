#Dependencies
import requests
import json
import pandas as pd
from datetime import date
import csv
import random
from scipy import stats
import time

#Open your log of previous guesses (or begin a new one) using your first name
name=input("What is your first name?")
with open (f"{name}.csv",'a') as allpckts:
    pass

#Define a function to fetch your zodiac sign"
def zodiac_sign(day, month):
    if month == 12:
        astro_sign = 'sagittarius' if (day < 22) else 'capricorn'
    elif month == 1:
        astro_sign = 'capricorn' if (day < 20) else 'aquarius'
    elif month == 2:
        astro_sign = 'aquarius' if (day < 19) else 'pisces'
    elif month == 3:
      astro_sign = 'pisces' if (day < 21) else 'aries'
    elif month == 4:
        astro_sign = 'aries' if (day < 20) else 'taurus'
    elif month == 5:
      astro_sign = 'taurus' if (day < 21) else 'gemini'
    elif month == 6:
        astro_sign = 'gemini' if (day < 21) else 'cancer'
    elif month == 7:
        astro_sign = 'cancer' if (day < 23) else 'leo'
    elif month == 8:
        astro_sign = 'leo' if (day < 23) else 'virgo'
    elif month == 9:
        astro_sign = 'virgo' if (day < 23) else 'libra'
    elif month == 10:
        astro_sign = 'libra' if (day < 23) else 'scorpio'
    elif month == 11:
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
    return(astro_sign)

#collect info to determine your zodiac sign
month=input("Enter the number of your birth month. Do not include leading zeros.")
day=input("Next, enter the number of your birth day. Do not include leading zeros.")

#get your sign
sign=zodiac_sign(int(day),int(month))
print(f"Your zodiac sign is {sign.title()}. If this is correct, continue. If not, please start over and re-enter your information.")
print("In 30 seconds, you will be shown a list of horoscopes. One of these horoscopes is your real horoscope. The others are horoscopes from different astrology signs. Select the one that you think describes your day the best. If you can guess the correct one more often than random chance, horoscopes might just be accurate!\n")
time.sleep(30)

zodiaclist=["sagittarius", "capricorn", "aquarius", "pisces", "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio"]

#Get 4 Wrong Answers
wronglist=[item for item in zodiaclist if item != sign]
fakes=[]
for i in range(4):
    onefake=random.choice(wronglist)
    fakes.append(onefake)
    wronglist.remove(onefake)

#Get a randomly shuffled list of four zodiac signs, one of which is correct
testlist=[]
for item in fakes:
    testlist.append(item)
testlist.append(sign)
random.shuffle(testlist)

#Assign each possible answer to a number
guessdict={}
for i in range(len(testlist)):
    guessdict[i]= testlist[i]

#Get readings from every entry on the testlist, and assign a number to each possible guess
for i in range(5):
    params = (
('sign', testlist[i]),
('day', 'today'),
)

    results=requests.post('https://aztro.sameerkumar.website/', params=params)
    results_json=api_json = results.json()
    print(f"CHOICE NUMBER {i+1}")
    print ("----------------")
    mood=results_json["mood"]
    print(f"MOOD: {mood}")
    reading=results_json["description"]
    print(f"Reading: {reading}")
    print("\n")

#Make your guess!
make_guess=int(input("Type the number of your choice. Which zodiac reading sounds the most accurate to you?"))-1


#Report the results of this guess
if guessdict[make_guess]==sign:
    print ("Congratulations! You were able to identify your real astrology sign today!\n")
else:
    print("Sorry! Today you picked the incorrect astrology sign.\n")

#This is the sign you picked
print(f"Your Real Sign: {sign.title()} ")
your_guess=testlist[make_guess]
print(f"Your Guess: {your_guess.title()}")


#Generate today's datapoint
today = date.today()
correct = guessdict[make_guess]==sign
correct_num = 0
if guessdict[make_guess]==sign:
    correct = 1

datapoint=[today,sign,guessdict[make_guess], correct, correct_num,]


#Record the data for today
with open (f"{name}.csv",'a') as allpckts:
        writer = csv.writer(allpckts)
        writer.writerow(datapoint)



#Examine your results for guesses so far

print("Your guesses so far:")
data=pd.read_csv(f"{name}.csv" , names=["Date","True Sign","Your Guess","You Right?","binary_rightness"])
print(data)

#No cheating! Erase every attempt on the same day except for the first try.
cleandf=pd.DataFrame(columns = ["Date","True Sign","Your Guess","You Right?","binary_rightness"])
uniquedates=data["Date"].unique()
for item in uniquedates:
    firsttry=data[data.Date == item].head(1)
    cleandf=cleandf.append(firsttry)
if len(uniquedates)<len(data):
    print("\nHave you been cheating? There is more than one entry in here for the same date! Not to worry. I'll just ignore those other tries when calculating your results below :) .\n")

#Conduct a t-test for difference of one mean from a set value (20%)
binary_list=[]
for item in cleandf["binary_rightness"]:
    binary_list.append(item)
pvalue=stats.ttest_1samp(binary_list,0.20)[1]
N=len(binary_list)

#Report the results
pvalue=stats.ttest_1samp(binary_list,0.20)[1]
N=len(binary_list)
percent = cleandf["binary_rightness"].mean() *100
result=f"INCONCLUSIVE. Test must be taken on {30 - N} more days.\n"
print(f"You guessed correctly {percent}% of the time. If your guesses were only as good as random chance, you would be right approximately 20% of the time.\n")
print(f"You took this test on {N} different days. For maximally rigorous results, you must take this test on at least 30 different days.\n")
print(f"The probability that your guesses are only as good as random chance is {pvalue}. Note that this vlue will be 'nan' if you only took this test on one day.\n")
if pvalue<0.05:
    if percent>0.25:
        print("So far, your guesses are were more accurate than random chance! Congratulations!")
        if N<30:
            print(f"However, you have only completed this test on {N} days so far. You must complete it at on at least 30 different days for it to be conclusive.\n")
        else: 
            print(f"You have completed this test {N} times so far, which is greater than the minimum of 30 days needed for a rigorous test! Congratulations! You have produced scientific evidence that horoscopes are accurate! I hope that you recorded proof that you followed the directions, because the scientific community will be extatic to learn about this momentus discovery. You will be famous!")
            result = "Reject the Null Hypothesis. Horoscopes might be real!\n"
    else:
        print("Your guesses are significantly different from random chance, but... oops! You guessed worse than random chance would predict! You were less likely to identify the correct horoscope for yourself with the help of these descriptions than you would have been with your eyes closed!\n")
else:
    print("So far, your guesses are not significantly different than random chance. Sorry!\n")
    if N<30:
            print(f"However, you have only completed this test on {N} days so far. You must complete it at on at least 30 different days for it to be conclusive. Keep taking the test! You still have a chance!\n")
    else:
        print("You took this test for at least 30 days, and you were still unable to guess your horoscope better than random chance. Sorry, but the weight of the scientific evidence points to the fact that these horoscopes simply didn't describe your day accurately. Perhaps horoscopes are not real after all.")
        result = "Fail to reject the Null Hypothesis. Horoscopes are probably not real.\n"    

print(f"RESULT: {result}")

