/* We define the commands to rebuild the database from CSV */
/* This can be ported into a python script wholesale */
drop table recipesingredients;
drop table recipes, ingredients;

/* Make a recipe table */
/* cols: id, recipe_name, instructions, cooktime, notes */
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

/* Make an ingredients table */
/* cols: id, ingredient_name, store_unit, price */
create table ingredients (
  id serial primary key,
  ingredient_name varchar(50) not null unique,
  store_unit varchar(50),
  price real
);

copy ingredients(ingredient_name, store_unit, price,id)
from '/Users/Seth/Desktop/Repositories/recipe-database/ingredients.csv'
delimiter ',' csv header;

/* Make a junction table */
/* cols: recipe_id, ingredients_id, quantity, unit*/
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

/* In script, include error handling here */

create index idx_igrname
  on ingredients (ingredient_name);

create index idx_recname
  on recipes (recipe_name);

/* End of recreate database */

/*-----------------------*/
/* Example code snippets */
/*-----------------------*/

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
  unit_to_grams,
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
select id, recipe_name from recipes;

/* What are the instructions for this meal */
select instructions from recipes
where recipe_id = 21;

/* What ingredients are in this meal */
select recipe_name, ingredient_name, quantity, unit
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where recipe_name = null
or recipes.id in (26);

/* What ingredients are in some collection of meals */
select 
  ingredient_name, 
  sum(quantity) as total_quantity,
  unit
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where recipe_name in (null)
or recipes.id in (36,37,4,11)
--
group by ingredient_name, unit
order by ingredient_name;

/* What recipes use some of these ingredients */
select count(recipes.id) as count, recipe_name
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where ingredient_name in ('lime juice', 'cilantro')
--
group by recipe_name
order by count desc;

/* What is the est cost of shopping for those ingredients */
select sum(price) as total_price from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where recipe_id in (1,2,3,4);

/* How much time will I spend cooking this week? */
select sum(cooktime) as cooktime from recipes
where id in (2,3,4);


/* Other useful functions */

/* Modify column entry
update recipes
set instructions = 'ATK pg. 72'
where id=3;
*/

/* Modify column type
alter table ingredients
  rename column cup_to_grams to unit_to_grams;
*/


