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
    def __init__(self, name = '', ingredientList = [], cooktime = 0, instructions = '', notes = ''):
        # Return a recipe (name, ingredientList, cooktime)
        self.name = name
        self.ingredientList = ingredientList
        self.cooktime = cooktime
        self.instructions = instructions
        self.notes = notes

    def addIngredient(self, ingredient):
        # Add an ingredient to ingredientList
        ingnames = [item[0] for item in self.ingredientList]
        if ingredient[0][0] in ingnames:
            raise RuntimeError('You already have this ingredient')
        else:
            self.ingredientList = self.ingredientList + ingredient
    
    def savetoDB(self, attr):
        # Search to see if there's already a recipe
        # Modify if exists, otherwise insert
        return 0

    def modify(self, attr):
        # An interactive function to modify attributes of a recipe
        # Prints Recipe.attr and asks for a new value
        print getattr(self, attr)
        if attr == 'name':
            Value = str(raw_input('New name: '))
        elif attr == 'ingredientList':
            query = input('Give (ing, quant, unit): ')
            self.addIngredient([query])
            Value = self.ingredientList
        elif attr == 'cooktime':
            Value = input('New cooktime: ')
        elif attr == 'notes':
            Value = str(raw_input('New notes: '))
        elif attr == 'instructions':
            Value = str(raw_input('New instructions: '))
        setattr(self, attr, Value)

    @classmethod
    def fromDB(self, name):
        # Conditional can be removed later. Useful to input id for testing.
        # Given a recipe_name, return a Recipe class element

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
        recipe = Recipe()
        for row in results:
            ingredientList.append((row[1], row[2], row[3],))
        recipe.name = row[0]
        recipe.ingredientList = ingredientList
        recipe.cooktime = row[4]
        recipe.instructions = row[5]
        recipe.notes = row[6]
        return recipe

    @classmethod
    def allfromDB(self):
        # Write all recipes to a list
        cur.execute("""select * from recipes""")
        results = cur.fetchall()
        recipelist = [Recipe.fromDB(row[1]) for row in results]
        return recipelist
        

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

def shopping(recipes):
    # arg: list of recipes
    names = tuple([recipe.name for recipe in recipes])
    cur.execute("""
        select 
            ingredient_name, 
            sum(quantity) as total_quantity,
            unit
        from recipesingredients
        join ingredients on ingredients.id = recipesingredients.ingredient_id
        join recipes on recipes.id = recipesingredients.recipe_id
        where recipes.recipe_name in %s

        group by ingredient_name, unit
        order by ingredient_name;
    """, (names,))
    results = cur.fetchall()
    for row in results:
        print "    ", row[0], row[1], row[2]

def closeDatabaseConnection():
    con.close      
