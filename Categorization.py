# FILE PROCESSING

import pandas as pd

###do stuff to make me able to use my bank statement
f1 = 'bank.csv' #the file where my bank statement lives
statement = pd.read_csv(f1,header=None) #read my bank statement file and call it "statement"
bank = [] #create my blank array of expenses
for index, description in enumerate(statement[0]): #for each row in my file (create an index)
    expense = round(statement[1][index],0)
    if statement[1][index] < 0:
        bank.append([description, expense*-1])#append the description and the value to bank. * value by -1
    else:
        bank.append([description, expense]) #do same except * value by -1
###do stuff to make me able to use my categories list
f2 = "Categories.csv" #the file where my list of categories lives
catList = pd.read_csv(f2,header=None,keep_default_na=False) #read my list of categories and call it "catList"
mint = {} #create my blank associative array of categories and keywords


#creates mint
for column in catList:
    key = catList[column][0]
    values = catList[column]
    mint[key] = values

#removes the first value in dictionary (since that is the key in dictionary.) Also removes blank entries
for category in mint:
    del mint[category][0]
    blankspaces = 0
    for vendor in mint[category]:
        if vendor == "":
            blankspaces += 1
    while blankspaces > 0:
        del mint[category][len(mint[category])]
        blankspaces -= 1

# Categorization Function
import locale
locale.setlocale( locale.LC_ALL, '' )


def categorize(bank):
    spending = {}
    spending['Unknown'] = 0
    for expense in bank: ###for each bank entry ([item, cost])###
        description = expense[0] #call the thing that I bought, "description"
        value = expense[1] #call the ammount I paid for it, "value"
        foundMatch = False #initalize whether i find a match in my loop to false
        for cat in mint: ###while i'm at each bank entry, go through each cat in mint###
            categoryName=cat #set cat to something cleaner
            categoryVendors = mint[cat] #set the values of each corresponding key to something clear
            for vendor in categoryVendors: ###while i'm at each bank entry and going through each cat in mint, loop through vendors
                if "".join(vendor.lower().split()) in "".join(description.lower().split()): #if that vendor is somewhere in my description
                    foundMatch = True
                    if cat in spending: #and if that category is already in my spending array
                        spending[cat]+=value#add to that category in spending, the cost of the purchase
                    else: #if it's found in the description, but it's not in our list yet
                        spending[cat]=value #then add the cat as a key and it's inital value as that first cost
        if foundMatch == False: #if after all that I still haven't found a match for some things
            spending['Unknown'] += value #add value to the unknown bucket
            
    print("Total spend categorized:", round((1-(spending['Unknown'] / sum(spending.values())))*100,0),"%")
    return spending 
categorize(bank)
