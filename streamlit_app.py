# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your custom smoothie!
    """)

name_on_order = st. text_input('Name of Smoothie')
st.write('The name on your smoothie will be:',name_on_order)
#establish Snowflake connection
cnx=st.connection("snowflake")
session = cnx.session()

#Fetch data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the Loc function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

ingredients_string =''

if ingredients_list:
   ingredients_string = ',  '.join(ingredients_list)

if Fruit_chosen == ':'

   for fruit_chosen in ingredients_list:
    search_on= pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen,'SEARCH_ON'].iloc[0]
st.write('The search value for', fruit_chosen,'is', search_on, '.')
st.subheader(fruit_chosen + 'Nutrition information')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

#st.write(ingredients_string)

my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name on order) values ('{ingredients_string}','{name_on_order}')"""

#st.write(my_insert_stmt)
#st.stop()

time_to_insert= st.button('Submit Order')

if ingredients_string:
        session.sql(my_insert_stmt).collect()

st.success('Your Smoothie is ordered!', icon="✅")



