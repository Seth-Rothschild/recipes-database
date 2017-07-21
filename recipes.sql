/* Make a recipe list and an ingredients list*/
create table recipes (
  recipe_id serial primary key,
  recipe_name varchar(50) not null,
  instructions text,
  cooktime varchar (50)
);

create table ingredients (
  ingredient_id serial primary key,
  ingredient_name varchar(50) not null,
  calories integer,
  cup_to_grams integer,
  price real
);

/* To resolve the n-m relation, need a junction table*/
/* For now, I want it to have names to make it readable and quantities*/
create table recipesingredients (
  recipe_id int not null,
  ingredient_id int not null,
  quantity real,
  units varchar(50),
  constraint key_recipesingredients primary key (
    recipe_id,
    ingredient_id
  ),
  foreign key (recipe_id) references recipes (recipe_id),
  foreign key (ingredient_id) references ingredients (ingredient_id)
);

/* Example add recipe
insert into recipes (
  recipe_name,
  instructions,
  cooktime
)
values (
  'Macaroni and Cheese',
  null,
  '20 minutes'
);
*/

/* Example add ingredient
insert into ingredients (
  ingredient_name,
  calories,
  cup_to_grams,
  price
)
values (
  'smoked gouda',
  '40',
  null,
  null
);
*/

/* Example add recipeingredient
insert into recipesingredients (
  recipe_id,
  ingredient_id,
  quantity,
  units
)
values (
  1,
  1,
  113,
  'grams'
);
*/


/*Queries*/
/* What are all of my recipes? */
select recipe_id, recipe_name from recipes;

/* What are the instructions for this meal */
select instructions from recipes
where recipe_name = 'Hard Boiled Eggs'
or recipe_id = 1;

/* What ingredients are in this meal */
select recipe_name, ingredient_name, quantity, units
from recipesingredients
join ingredients on ingredients.ingredient_id = recipesingredients.ingredient_id
join recipes on recipes.recipe_id = recipesingredients.recipe_id
-- User input below --
where recipe_name = null
or recipes.recipe_id = 3;

/* What ingredients are in some collection of meals */
select 
  ingredient_name, 
  sum(quantity) as total_quantity,
  units
from recipesingredients
join ingredients on ingredients.ingredient_id = recipesingredients.ingredient_id
join recipes on recipes.recipe_id = recipesingredients.recipe_id
-- User input below --
-- First meal --
where recipe_name = null
or recipes.recipe_id = 4
-- Second meal --
or recipe_name = null
or recipes.recipe_id = 3
-- Third meal --
or recipe_name = null
or recipes.recipe_id = null
--
group by ingredient_name, units;


/* What is the est cost of shopping for those ingredients */

/* What recipes use some of these ingredients */
select recipes.recipe_id, recipe_name
from recipesingredients
join ingredients on ingredients.ingredient_id = recipesingredients.ingredient_id
join recipes on recipes.recipe_id = recipesingredients.recipe_id
-- User input below --
where ingredient_name = 'egg'
or ingredient_name = 'smoked gouda';

/* What recipes use some of these ingredients, sorted by which use more */

/* How much time will I spend cooking this week? */



