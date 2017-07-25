# connect to my local database using psycopg2
import psycopg2
try:
    con = psycopg2.connect(
        "dbname='recipes' user='seth' host='localhost' password=''"
    )
except:
    print "I am unable to connect to the database"
cur = con.cursor()

class Recipe(object):
    """ A recipe. Attributes: 
        name: The name of the recipe (string)
        ingredientList: A list of tuples (name, quantity, unit)
        cooktime: An integer in minutes
        instructions: a SQL text object. Does this become a string?
        notes: another SQL text object
    """
    def __init__(self, name, ingredientList, cooktime, instructions, notes):
        # Return a recipe (name, ingredientList, cooktime)
        self.name = name
        self.ingredientList = ingredientList
        self.cooktime = cooktime
        self.instructions = instructions
        self.notes = notes

    def modifyAttribute(self,attr, newattr):
        setattr(self, attr, newattr)

    def modifyAttributeInteractive(self,attr):
        print(getattr(self,attr))
        if raw_input('Modify attr? y/n: ') == 'y':
            setattr(self, attr, input('What do you want to change it to? '))
        else:
            print('Exiting modify attempt')

    def addIngredient(self, ingredient):
        # Add an ingredient to ingredientList
        if ingredient in ingredientList:
            raise RuntimeError('You already have this ingredient')
        self.ingredientList = self.ingredientList + ingredient


def rebuildDatabase():
    # Initial attempt was not error catching. TODO
    return(0)


def listRecipes():
    cur.execute("""select id, recipe_name from recipes""")
    results = cur.fetchall()
    for row in results:
        print "    ", row[0], row[1]


def listIngredients(name):
    # arg: recipe name (string)
    cur.execute("""
        select recipe_name, ingredient_name, quantity, unit
        from recipesingredients
        join ingredients on ingredients.id = recipesingredients.ingredient_id
        join recipes on recipes.id = recipesingredients.recipe_id
        where recipe_name = %s
    """, (name,))
    results = cur.fetchall()
    for row in results:
        print "    ", row[0], row[1], row[2], row[3]


def recipeNameToID(name):
    # arg: Recipe Name (string)
    cur.execute("""
        select id from recipes
        where recipe_name= %s;
    """, (name,))
    results = cur.fetchall()
    return results[0][0]


def ingNameToID(name):
    # arg: Ingredient Name (string)
    cur.execute("""
        select id from ingredients
        where ingredient_name=%s;
    """, (name,))
    results = cur.fetchall()
    return results[0][0]


def shoppingListIngredients(shoppingListIds):
    # arg: shoppingListIds (tuple)
    cur.execute("""
        select 
            ingredient_name, 
            sum(quantity) as total_quantity,
            unit
        from recipesingredients
        join ingredients on ingredients.id = recipesingredients.ingredient_id
        join recipes on recipes.id = recipesingredients.recipe_id
        where recipes.id in %s

        group by ingredient_name, unit
        order by ingredient_name;
    """, (shoppingListIds,))
    results = cur.fetchall()
    for row in results:
        print "    ", row[0], row[1], row[2]


def fromDB(name):
    # Conditional can be removed later. Useful to input id for testing.
    if type(name) == str:
        recipe_id = recipeNameToID(name)
    elif type(name) == int:
        recipe_id = name
    else:
        raise RuntimeError('You have the wrong input type')
    cur.execute("""
        select 
            recipe_name, 
            ingredient_name, 
            quantity, 
            unit, 
            cooktime, 
            instructions, 
            notes
        from recipesingredients
        join ingredients on ingredients.id = recipesingredients.ingredient_id
        join recipes on recipes.id = recipesingredients.recipe_id
        where recipe_id = %s
    """, (recipe_id,))
    results = cur.fetchall()
    global row
    ingredientList = list()
    for row in results:
        ingredientList.append((row[1], row[2], row[3],))
    recipe = Recipe(row[0], ingredientList, row[4], row[5], row[6])
    return recipe


def closeDatabaseConnection():
    con.close

def importFromDB():
    recipeList = list()
    for i in range(1,37):
        Recipe = fromDB(i)
        recipeList.append(Recipe)
    return recipeList    
      
recipeList=importFromDB()
