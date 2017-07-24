# connect to my local database using psycopg2
import psycopg2
try:
  conn = psycopg2.connect("dbname='recipes' user='seth' host='localhost' password=''")
except:
  print "I am unable to connect to the database"

cur = conn.cursor()

# define a "Recipe" object
class Recipe(object):
  # A recipe. Attributes: 
  #   name: The name of the recipe (string)
  #   ingredientList: A list of tuples (name, quantity, unit)
  #   cooktime: An integer in minutes
    
  def __init__(self, name, ingredientList, cooktime):
    # Return a recipe (name, ingredientList, cooktime)
    self.name = name
    self.ingredientList = ingredientList
    self.cooktime = cooktime
   
  def addIngredient(self, ingredient):
    # Add an ingredient to ingredientList
    if ingredient in ingredientList:
      raise RuntimeError('You already have this ingredient')
    self.ingredientList = self.ingredientList + ingredient


def rebuildDatabase():
  cur.execute("""
    drop table recipesingredients;
    drop table recipes, ingredients;

    create table recipes (
          id serial primary key,
      recipe_name varchar(50) not null unique,
      instructions text,
      cooktime integer,
      notes text
    );
    
    copy recipes(recipe_name, instructions, cooktime, notes)
    from '/Users/Seth/Desktop/Repositories/recipe-database/recipes.csv'
    delimiter ',' csv header;
    
    create table ingredients (
      id serial primary key,
      ingredient_name varchar(50) not null unique,
      store_unit varchar(50),
      price real
    );
    
    copy ingredients(ingredient_name, store_unit, price,id)
    from '/Users/Seth/Desktop/Repositories/recipe-database/ingredients.csv'
    delimiter ',' csv header;
    
    create table recipesingredients (
      recipe_id int not null,
      ingredient_id int not null,
      quantity real,
      unit varchar(50),
      constraint key_recipesingredients primary key (
        recipe_id,
        ingredient_id
      ),
      foreign key (recipe_id) references recipes (id),
      foreign key (ingredient_id) references ingredients (id)
    );
    
    copy recipesingredients(recipe_id, ingredient_id, quantity, unit)
    from '/Users/Seth/Desktop/Repositories/recipe-database/recipesingredients.csv'
    delimiter ',' csv header;
  """)

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
  """,(name,))
  results = cur.fetchall()
  return results[0][0]

def ingNameToID(name):
  # arg: Ingredient Name (string)
  cur.execute("""
    select id from ingredients
    where ingredient_name=%s;
  """,(name,))
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

def fromDB(name_or_id):
  if type(name_or_id) == str:
    name_or_id=recipeNameToID(name_or_id)
  else:
    name_or_id=name_or_id
  cur.execute("""
    select recipe_name, ingredient_name, quantity, unit, cooktime
    from recipesingredients
    join ingredients on ingredients.id = recipesingredients.ingredient_id
    join recipes on recipes.id = recipesingredients.recipe_id
    where recipe_id = %s
  """, (name_or_id,))
  results = cur.fetchall()
  ingredientList=list()
  for row in results:
    ingredientList.append((row[1],row[2],row[3],))
  recipe=Recipe(row[0],ingredientList, row[4])
  return recipe.ingredientList
