## Nigerian Foods API

### Api for some nigerian foods and thier nutritional information

Foods are classfied into 9 categories

*   rice_based
*   soups_and_stews
*   bean_based
*   meat_based
*   yam_based
*   cassava_based
*   snacks
*   beverages
*   others

### Endpoints

#### api/foods/\<foodname\>

Get a json response of the specified food  
example:  

<pre> { foodname: 
    { category: foodcategory, 
      img_url: link to image of food,
      nutritonal_information: 
    {'calories': value , carbs: value, protein: value, fat: value, sodium: value, sugar: value}
    }
}</pre>

URL:  https://nigerianfoods.herokuapp.com/api/foods/jollof_rice  
HTTP method: GET  

#### api/foods

Get a json response of every food in the database  
URL: https://nigerianfoods.herokuapp.com/api/foods
HTTP method: GET  

#### api/food_category/\<categoryname\>

Get a json response of a list of all the foods that belong to a particular category  
URL: https://nigerianfoods.herokuapp.com/api/food_category/rice_based
HTTP method: GET
