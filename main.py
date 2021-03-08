#!/usr/bin/env python

import sys
import time
import datetime
from datetime import date
from shops import shops_dic
today_date = date.today()
now = datetime.datetime.utcnow().strftime("%H:%M:%S")

dic = {}

print("Hello and welcome this is Money Manager to help\nyou keep on track with you spending!\n") 
name = input("Please enter your full name: ")
f_name = name.split()[0].capitalize()

print("Thank you", f_name)
salary = input("\nCould you please enter your yearly salary: ")
def check_sal(salary):
    try:
        salary = int(salary)
    except ValueError:
        s = input("That is not a valid salary, please enter: ")
        salary = s
check_sal(salary)

file_name = input("\nThank you, could you enter the file name your expenses are in: ")
print("\nWe are now importing your spending data please wait a moment.....\n")
time.sleep(1.5)
with open(file_name, "r") as f:#opens up the users expenses##
    lines = f.readlines()
    i = 0
    while i < len(lines):
        lines1 = lines[i].strip().split()
        prices = (lines1[-1].split("."))
        if len(prices[-1]) < 2:
            lines1[-1] = ".".join(prices) + "0"         #####this turns all numbers into a float#####
        if " ".join(lines1[0:-1]) not in dic:               ######## Unhasable type list for dictionary, converting to string ##############
            dic[" ".join(lines1[0:-1])] = float(lines1[-1])
        elif " ".join(lines1[0]) in dic:                    ######## Unhasable type list for dictionary, converting to string ##############
            dic[" ".join(lines1[0:-1])] = float(dic[lines1[0:-1]]) + float(lines1[-1])
        i = i + 1
        
grocerys = {}
cafes = {}
pubs = {}
takeaways = {}
travel = {}
restaurants = {}
for shop in dic.keys():
    if shop.lower() in shops_dic["grocerys"]:   ###shops_dic is the dictionary we have imported from shops.py which is our mini database of shops
        grocerys[shop.lower()] = dic[shop]           #this checks which category the shops by in by checking the keys of shops_dic, when it has found the same one
    elif shop.lower() in shops_dic["cafes"]:
        cafes[shop.lower()] = dic[shop]
    elif shop.lower() in shops_dic["travel"]:
        travel[shop.lower()] = dic[shop]
    elif shop.lower() in shops_dic["takeaways"]:
        takeaways[shop.lower()] = dic[shop]
    elif shop.lower() in shops_dic["pubs"]:
        pubs[shop.lower()] = dic[shop]
    elif shop.lower() in shops_dic["restaurants"]:
        restaurants[shop.lower()] = dic[shop]
list_dict = [grocerys, cafes, pubs, takeaways, travel, restaurants]
list_dict2 = ["Grocerys", "Cafes", "Pubs", "Takeaways", "Travel", "Restaurants"]

def calc_largest(price_list):
    max_no = price_list[0]
    for c in price_list:
        if c > max_no:
            max_no = c
    return max_no
x = calc_largest(dic.values())

def dic_lookup(price_list, max_no):   
    for shop, price in price_list:
        if price == max_no:
            return shop.capitalize()

def total_shop(list1): ### calculates the total cost of that days expenses ####
    total = 0
    for c in list1:
        total = total + float(c)
    return total

def salary_compare(salary):
    salary = int(salary) / 365 ###find out users daily payment
    x = total_shop(dic.values()) / salary
    if x < 1:
        print("You are under budget today {}! Well done\n".format(f_name)) ##if the user has spent less than they have earned, a number <1 will be outputted hence being under budget and this will be outputted
    elif x > 1:
        print("{} you went over budget today, be careful!\n".format(f_name)) # the opposite applies to this elif statement, they will have spent more than they earned that day

def calcx(x, y): ####this function calculates the percentage 
    time.sleep(.15)
    answer = float(x) / float(y) * 100
    answer = "{:.1f}".format(answer) #this formats the number to just one decimal place I learnt this from the website pythonforbeginners.com
    return answer


def percentage_spending():
    i = 0 ###this function provides the input for calcx and is in a loop so it only needs to be called once
    while i < len(list_dict):
        print(calcx(sum(list_dict[i].values()), total_shop(dic.values())) + "% was spent on " + list_dict2[i] + "\n")
        i = i + 1



def write_to_file():
    f = open("money_manager.txt", "a")
    f.write(str(f_name) + "'" + "s" + " " + "Expenditure on: \n") 
    f.write(str(today_date) + " at " + str(now) + "\n")
    f.write("Your daily expenses added up to: " + str(total_shop(dic.values())) + "\n")
    f.write("Your most expensive shop was: " + str(dic_lookup(dic.items(), x)) + " " + "which cost a total of " + str(calc_largest(dic)) + "\n\n")
    f.write(str(calcx(sum(list_dict[0].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[0]+ "\n")
    f.write(str(calcx(sum(list_dict[1].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[1]+ "\n")
    f.write(str(calcx(sum(list_dict[2].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[2]+ "\n")
    f.write(str(calcx(sum(list_dict[3].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[3]+ "\n")
    f.write(str(calcx(sum(list_dict[4].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[4]+ "\n")
    f.write(str(calcx(sum(list_dict[5].values()), total_shop(dic.values()))) + "% was spent on " + list_dict2[5]+ "\n\n")
    f.close()

percentage_spending()
write_to_file()
salary_compare(salary)
print("Your daily expenses added up to: {}\n".format(total_shop(dic.values())))
print("Your most expensive shop was: {} which cost a total of {}\n".format(dic_lookup(dic.items(), x), calc_largest(dic)))
print("All your spending data will be backed up into a file called money_manager.txt\nThank you and goodbye")
