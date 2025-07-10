import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Flight Info Search", layout="centered")
st.title("✈️ Flight Information Lookup")

with st.form("flight_form"):
    departure = st.text_input("Departure Airport Code (IATA)", "DXB").upper()
    arrival = st.text_input("Arrival Airport Code (IATA)", "LHR").upper()
    limit = st.slider("Number of flights to retrieve (max 5)", min_value=1, max_value=5, value=3)
    submitted = st.form_submit_button("Get Flights")

if submitted:
    with st.spinner("Searching for flights..."):
        try:
            response = requests.post(
                "http://localhost:8000/flights",
                json={"departure": departure, "arrival": arrival, "limit": limit}
            )
            data = response.json().get("flights", [])
            
            # Check for error in result
            if isinstance(data, list) and "error" in data[0]:
                st.warning(data[0]["error"])
            elif isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                st.success(f"Showing {len(df)} flights from {departure} to {arrival}:")
                st.dataframe(df)
            else:
                st.warning("No flights found.")
        except Exception as e:
            st.error(f"API error: {e}")
