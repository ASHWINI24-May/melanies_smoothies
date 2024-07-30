# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your custom smoothie!
    """)

name_on_order = st. text_input('Name of Smoothie')
st.write('The name on your smoothie will be:',name_on_order)
from snowflake.snowpark.functions import col
cnx=st.connection("SNOWFLAKE")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
  ingredients_string =''

for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen+ ''

#st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string +"""','"""+name_on_order+"""')"""

#st.write(my_insert_stmt)
#st.stop()


time_to_insert= st.button('Submit Order')

if ingredients_string:
        session.sql(my_insert_stmt).collect()

st.success('Your Smoothie is ordered!', icon="✅")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
