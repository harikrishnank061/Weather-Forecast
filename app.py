import streamlit as st
import requests
import datetime
import cohere

# Streamlit app layout
st.set_page_config(page_title="Weather Forecast App", page_icon="☀️")
st.title("☀️ Weather Forecast App")
st.markdown("Get the current weather, 5-day forecast, and AI-generated weather insights for any city.")

# Input API key and city
api_key = st.text_input("Enter your OpenWeatherMap API Key", type="password")
cohere_api_key = st.text_input("Enter your Cohere API Key", type="password")
city = st.text_input("Enter the City Name")

# Button to fetch weather
if st.button("Get Weather"):
    if api_key and cohere_api_key and city.strip():
        try:
            # Fetch current weather data
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(current_url).json()
            if response.get("cod") == 200:
                temp = response["main"]["temp"]
                desc = response["weather"][0]["description"].capitalize()
                humidity = response["main"]["humidity"]
                wind_speed = response["wind"]["speed"]
                st.success(f"Current weather in {city}:")
                st.write(f"🌡️ Temperature: {temp}°C")
                st.write(f"🌥️ Description: {desc}")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind Speed: {wind_speed} m/s")
                
                # Fetch 5-day forecast
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
                forecast_data = requests.get(forecast_url).json()
                if forecast_data.get("cod") == "200":
                    st.subheader("5-Day Weather Forecast:")
                    forecast_summary = []
                    for forecast in forecast_data["list"][::8]:
                        date = datetime.datetime.fromtimestamp(forecast["dt"]).strftime('%Y-%m-%d')
                        temp = forecast["main"]["temp"]
                        desc = forecast["weather"][0]["description"].capitalize()
                        forecast_summary.append(f"{date}: {temp}°C, {desc}")
                        st.write(f"📅 {date} - {temp}°C, {desc}")
                    
                    # Generate weather insights using Cohere
                    co = cohere.Client(cohere_api_key)
                    insights_prompt = ("Generate a weather forecast summary based on the following data:\n" + "\n".join(forecast_summary))
                    insights_response = co.generate(
                        model="command-xlarge",
                        prompt=insights_prompt,
                        max_tokens=300,
                        temperature=0.7,
                        k=0,
                        p=0.8,
                        frequency_penalty=0.2,
                        presence_penalty=0.2
                    )
                    if insights_response.generations:
                        insights = insights_response.generations[0].text.strip()
                        st.subheader("AI Weather Insights:")
                        st.write(insights)
                    else:
                        st.warning("⚠️ No insights generated. Try again later.")
                else:
                    st.error("⚠️ Error fetching forecast data. Please try again.")
            else:
                st.error(f"⚠️ City '{city}' not found. Please check the spelling.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("⚠️ Please provide both the API keys and city name to get the weather.")

st.markdown("---")
st.caption("Powered by OpenWeatherMap and Cohere | Built with ❤️ using Streamlit")
