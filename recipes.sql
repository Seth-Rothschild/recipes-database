/* Make a recipe list and an ingredients list*/
create table recipes (
  recipe_id serial primary key,
  recipe_name varchar(50) not null unique,
  instructions text,
  cooktime varchar (50)
);

create table ingredients (
  ingredient_id serial primary key,
  ingredient_name varchar(50) not null unique,
  calories integer,
  unit_to_grams integer,
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

create index idx_igrname
  on ingredients (ingredient_name);

create index idx_recname
  on recipes (recipe_name);

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
select recipe_id, recipe_name from recipes;

/* What are the instructions for this meal */
select instructions from recipes
where recipe_name = 'Hard Boiled Eggs'
or recipe_id = 1;

/* What ingredients are in this meal */
select recipe_name, ingredient_name, quantity, units
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where recipe_name = null
or recipes.id = 4;

/* What ingredients are in some collection of meals */
select 
  ingredient_name, 
  sum(quantity) as total_quantity,
  units
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where recipe_name in (null)
or recipes.id in (3,4)
--
group by ingredient_name, units;

/* What recipes use some of these ingredients */
select count(recipes.id) as count, recipe_name
from recipesingredients
join ingredients on ingredients.id = recipesingredients.ingredient_id
join recipes on recipes.id = recipesingredients.recipe_id
-- User input below --
where ingredient_name in ('olive oil', 'lime juice', 'frozen corn', 'egg')
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
where recipe_id in (2,3,4);


/* Other useful functions */

/* Modify column entry
update recipes
set cooktime = 40
where recipe_id=4;
*/

/* Modify column type
alter table ingredients
  rename column cup_to_grams to unit_to_grams;
*/


