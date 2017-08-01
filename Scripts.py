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

    
    def savetoDB(self):
        # Search to see if there's already a recipe
        # Modify if exists, otherwise insert
        cur.execute(""" select id, recipe_name from recipes """)
        reciperesults = cur.fetchall()
        database_recipes = [row[1] for row in reciperesults]

        cur.execute(""" select id, ingredient_name from ingredients """)
        ingredientresults = cur.fetchall()
        database_ingredients = [row[1] for row in ingredientresults]
        localingredients = [item[0] for item in self.ingredientList]

        # Step 1: if recipe exists ask to modify. If not, insert into database.
        # Also, flag that there might be existing recipeingredients
        if self.name in database_recipes:
            marker = 1
            query1 = raw_input('Recipe exists, modify? (y,n): ')
            if query1 != 'y':
                raise RuntimeError('Recipe not modified')
            cur.execute(
                """ 
                update recipes set
                (cooktime, instructions, notes) =
                (%s, %s, %s) where recipe_name = %s;""", 
                (self.cooktime, self.instructions, self.notes, self.name))
            con.commit()
        else:
            marker = 0
            print 'recipe does not exist'
            newRecId = len(database_recipes)+1
            cur.execute(
                """insert into recipes 
                (id, recipe_name, cooktime, instructions, notes) 
                values (%s, %s, %s, %s, %s);""", 
                (newRecId, self.name, self.cooktime, self.instructions, self.notes))
            con.commit()

        # Step 2: for every ingredient, check that it's in the ingredients table and update
        counter = len(ingredientresults)
        for ingredient in localingredients:
            if ingredient not in database_ingredients:
                print ingredient
                query2 = raw_input('does not exist, add to db? (y,n): ')
                if query2 != 'y':
                    raise RuntimeError('Recipe not added to DB')
                counter += 1
                cur.execute("""insert into ingredients (id, ingredient_name) values (%s, %s);""", (counter, ingredient))
                database_ingredients.append(ingredient)
                con.commit()
                print 'Ingredient added to database!'

        # Step 3: Wipe existing recipeingredients if nontrivial and build new ones
        if marker == 1:
            query3 = raw_input('Wiping potential recipesingredients, proceed? (y,n): ')
            if query1 != 'y':
                raise RuntimeError('Recipe ingredients unmodified')
        cur.execute(
            """delete from recipesingredients
            where recipe_id = %s""",
            (recipeNameToID(self.name),))
        for ingredient in self.ingredientList:
            cur.execute(
                """insert into recipesingredients
                (recipe_id, ingredient_id, quantity, unit)
                values (%s, %s, %s, %s);""",
            (recipeNameToID(self.name), ingNameToID(ingredient[0]), ingredient[1], ingredient[2]))

        con.commit()
        print "Database Updated!"

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

