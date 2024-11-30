import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import time
from state_images import city_images
from api import get_unsplash_image
from functools import lru_cache
import os

st.set_page_config(layout='wide',page_title='USA House Hunt', page_icon='favio.ico')# this should always be at the top of the code for streamlit

st.write("Current Working Directory:", os.getcwd())
st.write("Files in Directory:", os.listdir(os.getcwd()))
st.write("Files in 'data/' Directory:", os.listdir("data/") if os.path.exists("data/") else "No such directory")

def add_header():
    st.markdown("""
        <style>
        .header {
            background-color: rgba(28, 28, 28, 0.9);
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }
        .header-title {
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }
        .header-subtitle {
            font-size: 14px;
            opacity: 0.8;
        }
        </style>
        
        <div class="header">
            <div>
                <h1 class="header-title">USA House Hunt 🏠</h1>
                <p class="header-subtitle">Explore Real Estate Across America</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
def add_linkedin():
    st.sidebar.markdown("""
        <style>
        .linkedin-sidebar {
            position: fixed;
            bottom: 20px;
            left: 20px;
            font-size: 14px;
            z-index: 9999;
            background-color: rgba(28, 28, 28, 0.9);
            padding: 8px 10px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .linkedin-sidebar a {
            color: white;
            text-decoration: none;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .linkedin-sidebar svg {
            fill: white;
        }
        </style>
        <div class="linkedin-sidebar">
            <a href="https://www.linkedin.com/in/vraj-patel-3228ba2a9/" target="_blank">
                <span>LinkedIn: Vraj Patel</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
            </a>
        </div>
    """, unsafe_allow_html=True)


add_header()  # Add header at the top

# Add these right after your imports
@st.cache_data
def load_data():
    df = pd.read_csv('data/cleaned_housing_data.csv')
    # Clean price data once at load time
    if df['price (USD)'].dtype == object:
        df['price (USD)'] = df['price (USD)'].str.replace('$', '').str.replace(',', '').astype(float)
    return df

@st.cache_data
def load_coordinates():
    return pd.read_csv('data/coordinates.csv')

@st.cache_data
def load_zipcode_data():
    return pd.read_csv('data/zipdf.csv')

# I have cleaned the primary data and than saved it to cleaned_housing_data.csv, and then continued from here for streamlit.
df = load_data()
coords = load_coordinates()
zipcode_df = load_zipcode_data()


def add_key_insights():
    st.subheader("📊 Market Highlights")
    cols = st.columns(3)
    with cols[0]:
        st.info("🏠 Most Active Market: California")
    with cols[1]:
        st.info("📈 Fastest Growing: Texas")
    with cols[2]:
        st.info("💰 Best Value: Mississippi")

def load_overall_dashboard():
    st.title('Overall Details')
    avg_house_price = '$410,000'
    median_house_price = '$385,000'
    avg_lot_area = '0.25-0.35 acres'
    avg_sq_ft = '2,200-2,500 Sq Ft'

    add_key_insights()

    st.map(coords,zoom = 3.5)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Average House Price', avg_house_price)
    with col2:
        st.metric('Median House Price', median_house_price)
    with col3:
        st.metric('Average Lot Area', avg_lot_area)
    with col4:
        st.metric('Average House Area', avg_sq_ft)


    # Data with all U.S. states and their average housing prices
    housing_data = pd.DataFrame({
        'State': [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ],
        'Avg_Housing_Price': [
            175000, 310000, 330000, 145000, 800000, 540000, 380000, 290000, 350000, 285000,
            850000, 375000, 270000, 190000, 180000, 170000, 185000, 210000, 325000, 410000,
            550000, 225000, 310000, 155000, 205000, 420000, 180000, 395000, 450000, 480000,
            270000, 700000, 290000, 245000, 250000, 175000, 450000, 300000, 385000, 280000,
            250000, 310000, 300000, 475000, 320000, 380000, 520000, 155000, 240000, 410000
        ],
        'Cost_of_Living_Index': [
            89, 121, 104, 86, 151, 116, 125, 110, 103, 95,
            191, 100, 95, 90, 88, 89, 92, 96, 114, 124,
            132, 92, 99, 86, 91, 106, 92, 113, 118, 126,
            97, 142, 95, 98, 90, 88, 117, 101, 117, 95,
            98, 94, 92, 113, 110, 112, 125, 84, 94, 108
        ]
    })

    # Heatmap
    st.markdown("## 🏡 Housing Prices Across States")
    fig = px.choropleth(
        housing_data,
        locations="State",
        locationmode="USA-states",
        color="Avg_Housing_Price",
        color_continuous_scale="Blues",  # Add a color scale
        hover_name="State",
        hover_data=["Avg_Housing_Price", "Cost_of_Living_Index"],
        scope="usa"
    )
    st.plotly_chart(fig)


    # A few states with unique insights
    insight_options = [
        "California has the highest average house price at $800,000.",
        "Mississippi is the most affordable state, with an average house price of $145,000.",
        "Hawaii has the most expensive cost of living index in the U.S.",
        "Texas has the fastest-growing housing market in recent years.",
        "New York is known for luxury apartments, with an average price of $700,000."
    ]

    # CSS for floating transparent row
    st.markdown(
        """
        <style>
        .floating-tip {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 14px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            text-align: center;
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Dynamic insight updates
    placeholder = st.empty()
    insight_index = int(time.time() / 15) % len(insight_options)  # Changes every 15 seconds
    placeholder.markdown(
        f"""
        <div class="floating-tip">
            {insight_options[insight_index]}
        </div>
        """,
        unsafe_allow_html=True
    )


def display_city_image(state):
    # Convert state name to lowercase and replace spaces with hyphens
    state_key = state.lower().replace(" ", "-")
    
    # Check if the state has an image
    if state_key in city_images:
        st.image(city_images[state_key], use_container_width=True, caption=f"Welcome to {state}")
    else:
        st.write(f"No image available for {state}")



def find_state_details(state):
    st.title(state)

    display_city_image(state)

    state_data = df[df['state'] == state]
    if len(state_data) == 0:
        st.error(f"No data available for {state}")
        return
    
    st.header(f'Top 10 Most Expensive Houses in {state}')

    # Ensure 'price (USD)' is numeric
    if df['price (USD)'].dtype == object:  # Check if column is a string
        df['price (USD)'] = df['price (USD)'].replace({',': '', r'\$': ''}, regex=True).astype(float)

    # Filter and sort for the top 10 most expensive houses
    top_exp_house = df[df['state'] == state].sort_values(by='price (USD)', ascending=False).head(10)

    # Create a copy and add price in millions
    formatted_houses = top_exp_house.copy()
    formatted_houses['price_in_Million'] = formatted_houses['price (USD)'] / 1_000_000

    # Display specific columns with price in millions
    selected_columns = ['price_in_Million', 'status', 'bed', 'bath', 'acre_lot', 'city', 'state', 'zip_code', 'house_size_sq_ft', 'prev_sold_date']
    st.dataframe(formatted_houses[selected_columns])



   # Section 2: Top 10 Cities by Average House Price
    st.header(f'Average House Prices in {state}')

    # Filter data for the selected state
    state_data = df[df['state'] == state]

    # Calculate the average price by city
    avg_price_data = state_data.groupby(['city']).mean(numeric_only=True).reset_index()
    avg_price_data.rename(columns={'price (USD)': 'average_price'}, inplace=True)

    # Sort by average price and get the top 10 cities
    top_10_cities = avg_price_data.sort_values(by='average_price', ascending=False).head(10)

    # Filter the original dataset to include only rows from the top 10 cities
    top_10_data = state_data[state_data['city'].isin(top_10_cities['city'])].copy()

    # Add the average price for each city as a new column
    top_10_data['average_price'] = top_10_data['city'].map(top_10_cities.set_index('city')['average_price'])
    top_10_data['average_price_M'] = top_10_data['average_price'] / 1_000_000

    final_top_10 = top_10_data.head(10)  # Ensures only the top 10 rows are displayed
    selected_columns = ['average_price_M', 'status', 'bed', 'bath', 'acre_lot', 'city', 'state', 'zip_code', 'house_size_sq_ft', 'prev_sold_date']
    st.dataframe(final_top_10[selected_columns])

    # Additional Insight: Overall Average House Price in the State
    overall_average = avg_price_data['average_price'].mean()
    st.subheader(f"Overall Average House Price in {state}: ${overall_average:,.2f}")




def display_city_map(city, state):
    # Filter data for the selected city
    try:
        city_data = zipcode_df[(zipcode_df['city'] == city) & (zipcode_df['state'] == state)]
        
        # Display population metric
        st.metric(label=f"Population of {city}", 
                value=f"{int(city_data['population'].iloc[0]):,}")
        
        # Create a dataframe for the map with required columns
        map_data = city_data[['lat', 'lng']].rename(columns={'lng': 'lon'})
        
        # Display the map
        st.map(map_data, zoom=7)
    except Exception as e:
        st.error(f"Not enough information on {city}")


def show_highest_property_details(city):
    # Get the highest-priced property in the city
        try:
            highest_property = df[df['city'] == city].sort_values('price (USD)', ascending=False).iloc[0]
            
            # Section title with a styled container
            st.subheader("🏡 Highest Valued Property Details")
            st.markdown("""
                <div style="background-color: #2C3E50; padding: 20px; border-radius: 10px; margin: 10px; border: 2px solid #ECF0F1;">
                    <h3 style="color: #ECF0F1; text-align: center;">Highest Valued Property Details</h3>
                    <p style="color: #F1C40F; font-size: 20px; font-weight: bold;">Price: ${:,.2f}</p>
                    <p style="color: #BDC3C7; font-size: 18px;">Bedrooms: {}</p>
                    <p style="color: #BDC3C7; font-size: 18px;">Bathrooms: {}</p>
                    <p style="color: #BDC3C7; font-size: 18px;">Square Feet: {:,.0f}</p>
                    <p style="color: #BDC3C7; font-size: 18px;">Lot Size: {:.2f} acres</p>
                    <p style="color: #BDC3C7; font-size: 18px;">Status: {}</p>
                </div>
            """.format(
                highest_property['price (USD)'],
                int(highest_property['bed']),
                int(highest_property['bath']),
                highest_property['house_size_sq_ft'],
                highest_property['acre_lot'],
                highest_property['status']
            ), unsafe_allow_html=True)
        
        except IndexError:
            st.error(f"No properties found in {city}.")
        except Exception as e:
            st.error(f"Not enough information available")

def show_best_deals(city):
    city_data = df[df['city'] == city]
    total_properties = len(city_data)
    
    if total_properties == 0:
        st.warning(f"No properties found in {city}")
        return
    
    # Take minimum between total properties and 5
    n_samples = min(5, total_properties)
    best_deal_data = city_data.sample(n=n_samples)
    
    st.subheader(f"Featured Properties in {city}")
    if total_properties < 5:
        st.info(f"Showing all {total_properties} available properties in {city}")
    else:
        st.info(f"Showing {n_samples} random properties out of {total_properties} available")
        
    st.dataframe(best_deal_data[['price (USD)', 'house_size_sq_ft', 'bed', 'bath', 'acre_lot']])

# Put this OUTSIDE and BEFORE the find_city_detail function
@lru_cache(maxsize=100)
def get_cached_unsplash_image(city):
    try:
        return get_unsplash_image(city)
    except Exception as e:
        st.warning(f"Could not load image for {city}: {str(e)}")
        return None

# Then your find_city_detail function stays as is, but uses the cached function
def find_city_detail(city, state):
    st.title(city)
    given_state = state
    
    try:
        image_url = get_cached_unsplash_image(city)
        
        if image_url:
            st.image(image_url, use_container_width=True, caption=f"Welcome to {city}")
        else:
            # Try to get state image as fallback
            state_key = state.lower().replace(" ", "-")
            if state_key in city_images:
                st.image(city_images[state_key], use_container_width=True, 
                        caption=f"Welcome to {city}, {state}")
                
    except Exception as e:
        # Try state image as fallback here too
        try:
            state_key = state.lower().replace(" ", "-")
            if state_key in city_images:
                st.image(city_images[state_key], use_container_width=True, 
                        caption=f"Welcome to {city}, {state}")
            else:
                st.image('nature_default.jpg', 
                        caption=f"Welcome to {city}, {state}")
        except:
            st.error("Could not load any images for this location")

    # Calculate the metrics
    # Total Properties
    total_properties = len(df)

    # Median Price (first ensure price is numeric)
# Filter data for the selected city first
    city_data = df[df['city'] == city].copy()  # Create a copy to avoid warnings
    total_properties = len(city_data)

    if total_properties > 0:  # Only calculate if there are properties in the city
        # Clean and convert price data
        if city_data['price (USD)'].dtype == object:
                city_data['price (USD)'] = city_data['price (USD)'].str.replace('$', '').str.replace(',', '').astype(float)

        
        # Calculate metrics for the specific city
        median_price = city_data['price (USD)'].median()
        
        # Calculate price per sqft for the specific city
        city_data['price_per_sqft'] = city_data['price (USD)'] / city_data['house_size_sq_ft']
        avg_price_per_sqft = city_data['price_per_sqft'].mean()        

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label=f"Total Properties in {city}", value=f"{total_properties:,}")
        
        with col2:
            st.metric(label=f"Median Price in {city}", value=f"${median_price:,.2f}")
        
        with col3:
            st.metric(label=f"Avg Price per Sq Ft in {city}", value=f"${avg_price_per_sqft:,.2f}")
    else:
        st.write(f"No properties found in {city}")
    # calling the upper function below.
    show_highest_property_details(city)


    show_best_deals(city)


    city_data = df[df['city'] == city]
    st.write(f"{city} Property Details")  # Add this to check if filtering works
    st.dataframe(city_data)


    # Price Distribution Chart
    st.subheader("Price Distribution")
    fig = px.histogram(city_data, x='price (USD)', title=f'Price Distribution in {city}')
    st.plotly_chart(fig)

    # Property Size vs Price Scatter Plot
    st.subheader("Property Size vs Price")
    fig = px.scatter(city_data, x='house_size_sq_ft', y='price (USD)', 
                    title=f'Property Size vs Price in {city}')
    st.plotly_chart(fig)

    st.subheader("Property Statistics")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Avg Bedrooms", f"{city_data['bed'].mean():.1f}")
    with col5:
        st.metric("Avg Bathrooms", f"{city_data['bath'].mean():.1f}")
    with col6:
        st.metric("Avg Lot Size", f"{city_data['acre_lot'].mean():.2f} acres")

        # Price trends over time 
    try:
        if 'prev_sold_date' in city_data.columns:
            st.subheader("Price Trends")
            price_trend = city_data.groupby('prev_sold_date')['price (USD)'].mean()
            st.line_chart(price_trend)
    except Exception as e:
        st.error(f"Not enough information on: {state}")


    display_city_map(city,given_state)


def main():
    # Then update your main navigation code to include these:
    st.sidebar.title('Locate Property Details')
    option = st.sidebar.selectbox('Select One',['Overall', 'State','City'])


    if option == 'Overall':
        load_overall_dashboard()
    elif option == 'State':
        # State-level selection
        selected_state = st.sidebar.selectbox('Select State', sorted(df['state'].unique().tolist()))

        # Store the state of btn1 (Find State Details)
        if st.sidebar.button('Find State Details'):
            st.session_state['state_selected'] = selected_state

        # Check if a state is selected
        if 'state_selected' in st.session_state:
            find_state_details(st.session_state['state_selected'])

            # Filter cities for the selected state
            cities_in_state = df[df['state'] == st.session_state['state_selected']]['city'].unique().tolist()

            # Dropdown to select a city within the state
            selected_city = st.selectbox('Select City in State', sorted(cities_in_state), key="city_selector")

            # Store the state of btn2 (Find City Details)
            if st.button('Find City Details'):
                st.session_state['city_selected'] = selected_city

            # Check if a city is selected and call the city details function
            if 'city_selected' in st.session_state:
                find_city_detail(st.session_state['city_selected'], selected_state)
    else:
        # Dropdown to select a city
        selected_city = st.sidebar.selectbox('Select City', sorted(df['city'].unique().tolist()))

        # Button to fetch details
        btn3 = st.sidebar.button('Find Details')

        if btn3:
            # Get the state corresponding to the selected city
            state_for_city = df[df['city'] == selected_city]['state'].iloc[0]
            
            # Pass both city and state to the function
            find_city_detail(selected_city, state_for_city)


    add_linkedin()

if __name__ == "__main__":
    main() 