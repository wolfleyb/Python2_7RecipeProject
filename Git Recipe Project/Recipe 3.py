# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:02:32 2015

@author: Ben
"""
from __future__ import division
import numpy as np
import pickle
import json
def var_str(variable):
    variable = str(variable)


TheBook = list()

ing_data = {}
with open('ingdictionary.txt','r') as inf:
    ing_data = json.loads(inf.read())
#Ing_Data = #whatever Dallas sends me
        
class Recipe(object):
    """A collection of Recipes used to create a callorie count. Recipes have the 
    following properties:
    
    Attributes:
        name: String representing the recipe's name
        ing_count: number of ingredients
        ingredient: The main ingredient
    """
    
    def __init__(self, nameP, ing_countP, ingsP):
        """Return a recipe name that's name is "name" and ingredients are
        ingredient and ing_count"""
        self.name = nameP
        self.ing_count = ing_countP  
        self.ings = ingsP
      


#ingredient database, used to count calories        
class Ingredients(object):
    """Ingredient Database including Ingredient, number of calories per measure.
    This data will be used to count calories, which is the whole purpose of this
    program."""
    
    def __init__(self, ingredient, calorie, measure):
        
        self.ingredient = ingredient
        self.cal = calorie
        self.measure = measure #calorie per this unit of measure


#input units and calories per unit.

def unit_conv (unit, calories):
    if unit == ('tsp') :
        new_amount = (1 / 48) * calories #+('calories/cup')
    elif unit == ('tbsp') :
        new_amount = (1 / 16) * calories #+ ('calories/cup')
    elif unit == ('oz') :
        new_amount = (1 / 8) * calories #+ ('calories/cup')
    elif unit ==('cup') :
        new_amount = calories #+ ('calories/cup')

    return new_amount

#Function for testing if a variable is an integer
def num_test_int(var):
    try:
        var = int(var)
    except ValueError:
        print("Invalid Input: Numbers Only, Restart Program")
        quit()
#Function for testing if a variable is a float        
def num_test_float(var):
    try:
        var = float(var)
    except ValueError:
        print("Invalid Input: Numbers Only, Restart Program")
        quit()


#Function for adding ingredient data to database
def ing_data_add():
    
    #input new ingredient data
    new_ing = input("Name of Ingredient: ")
    cal_ing = input('Calories per cup: ')
    cost_ing = input('Cost per cup: ')
    
    #new dictionary entry
    ing_data[new_ing]={}
    ing_data[new_ing]["calories"] = cal_ing
    ing_data[new_ing]["price"] = cost_ing
    
    with open('ingdictionary.txt', 'w') as inf:
        inf.write(json.dumps(ing_data))

#What do I want to do. I want a function that will call a specific recipe, \
#through that recipe's ingredients, open that specific ingredients file
#call on its calorie count, add that calorie count to a variable, and return
#that variable
#converts units to calories per cup.    

def calorie_count():
    TheBook = pickle.load(open("save.p", "rb"))
    calcount = 0
    costcount = 0
    
       
    meal_number = input("How Many Items: ")

    #search and combine both databases to count calories and cost
    for i in range(meal_number):
        rec_name = input("Name of Recipe " + str(i+1) + ": ")
        rec_name = rec_name.title()
        
        TheBook = pickle.load( open("save.p", "rb"))
        
        for recipe in TheBook:
            if recipe.name == rec_name:
                for ingredient in recipe.ings:
 
                    calcount = calcount + float(recipe.ings[ingredient]["amount"]) * float(ing_data[ingredient]['calories'])
                    costcount = costcount + float(recipe.ings[ingredient]["amount"]) * float(ing_data[ingredient]['price'])
                            
    return calcount, costcount
    
                    
    return calcount

def add_ingredient(): #Function used to add ingredients to database
       
    #Add ingredient name
    ingredient_name = input('Ingredient name: ')
    ingredient_name.title()
    
    #Add ingredient unit
    print('Unit of measure:')
    print('     1---cups')
    print('     2---tsp')
    print('     3---tbsp')
    print('     4---oz')

    
    measure = input('Input: ')
    num_test_int(measure)
    
   
    #Add calorie count
    amount = input('Amount of ingredient per unit entered: ')
    num_test_float(amount)
    amount = float(amount)    
    
    
    if measure == 1:
        unit = 'cups'
    elif measure == 2:
        unit = 'tsp'
        amount = unit_conv(unit, amount)
    elif measure == 3:
        unit = 'tbsp'
        amount = unit_conv(unit, amount)
    elif measure == 4:
        unit = 'oz'
        amount = unit_conv(unit, amount)
    else:
        print('Invalid Entry: Restart Prgram')
        quit()
        
        
        unit = 'cups'
    
    
    y = (ingredient_name, unit, amount)
    return y

def add_recipe(): #Function used to add a new recipe
    recipe_name = input('Recipe name: ')
    ing_num = input('Number of Ingredients: ')
    ings = {}
    
    for i in range(ing_num):
        ing_add = add_ingredient()
        print(ing_add)
        ings[ing_add[0]] = {"unit":ing_add[1], "amount":ing_add[2]}
        
        
    
    x = Recipe(recipe_name, ing_num, ings)
    return x
    

    
#Function to Print Recipes    
def Print_Recipe(x):
    TheBook = pickle.load( open("save.p", "rb"))
    print (TheBook[x].name)
    print (TheBook[x].ing_count)
    print (TheBook[x].ings)
    print ("____________________")
    
    
# Initialize counter    
t = 0

while t !=6: # The main menu page
    print ("What would you like to do?")
    print ("1---Add a Recipe")
    print ("2---View Recipes")
    print ("3---Delete Recipe")
    print ("4---Count Calories and Cost")
    print ("5---Add Ingredient Data")
    print ("6---Quit")
    t = input("Input: ")
    
    #Add A Recipe  
    if t == 1:
        R = add_recipe()
        TheBook.append(R);
        print (R.name, R.ing_count, R.ings)
    #Save to file        
        for i in range(len(TheBook)):    
            pickle.dump(TheBook,open("save.p", "wb"))
        

    #View Recipe Book            
    elif t == 2:
        TheBook = pickle.load(open("save.p", "rb"))
        for i in range(len(TheBook)):
            Print_Recipe(i)
            print ("____________________")
    
    #Edit Recipes        
    elif t == 3:
        
        #Load Recipes
        TheBook = pickle.load(open("save.p", "rb"))    
        
        #input desired recipe to change
        del_recipe = input("Name of Recipe to Delete: ")
        del_recipe = del_recipe.title()
        
        #Search TheBook for Recipe name
        for recipe in TheBook:
            
            if recipe == del_recipe:
                TheBook = pickle.load(open("save.p", "rb"))
                TheBook = [x for x in TheBook if x.name != del_recipe]
                pickle.dump(TheBook,open("save.p", "wb"))

     #Calorie and Cost counting option                   
    elif t == 4:
        Output = calorie_count()
        print("________________________________________")
        print("________________________________________")
        print("Amount of Calories for Today: " + str(Output[0]))
        print("Cost of Ingredients: $" + "%.2f" % Output[1])
        print("________________________________________")
        print("________________________________________")
        print(" ")


        #Add Ingredients to ingredient database
    elif t == 5:
        ing_data_add()
                
                    
        
                
                
