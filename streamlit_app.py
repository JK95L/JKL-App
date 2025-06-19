import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.title("✌️ My new app")
st.write(
    "This is the app of Jannis Kliwert."
)
# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_data():
    """Grab data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/Out of stock.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';')

    # Convert years from string to integers
    df['Quantity'] = pd.to_numeric(df['Quantity'])
    df['ID'] = pd.to_numeric(df['ID'])
    # Convert German date format (DD.MM.YYYY) to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    # Extract calendar week
    df['Calendar_Week'] = df['Date'].dt.isocalendar().week

    return df

df = get_data()
#print(df)

# Add some spacing
''
''

min_value = df['Calendar_Week'].min()
max_value = df['Calendar_Week'].max()

from_week, to_week = st.slider(
    'Which weeks are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

products = df['Name'].unique()

if not len(products):
    st.warning("Select at least one country")

selected_products = st.multiselect(
    'Which products would you like to view?',
    products,
    ['Chocolate Cake', 'Vanilla Shake', 'Cookies', 'Ice Cream'])

''
''
''
''
''

# Filter the data
filtered_df = df[
    (df['Name'].isin(selected_products))
    & (df['Calendar_Week'] <= to_week)
    & (from_week <= df['Calendar_Week'])
]

st.header('Failed quantity over time', divider='gray')

''

st.bar_chart(
    filtered_df,
    x='Calendar_Week',
    y='Quantity',
    color='Name',
)

''
''