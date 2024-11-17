# Streamlit App
st.title("AI Agent Dashboard")

# File upload for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
google_sheet_url = st.text_input("Enter Google Sheet URL")

# Load and display data based on user input
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded CSV File:")
    st.dataframe(data)

elif google_sheet_url:
    credentials = authenticate_google_sheets()
    data = load_google_sheet(google_sheet_url, credentials)
    if not data.empty:
        st.write("Preview of Google Sheet Data:")
        st.dataframe(data)
    else:
        st.error("No data found in the provided Google Sheet.")

# Display column selection if data is loaded
if 'data' in locals() and not data.empty:
    column_to_search = st.selectbox("Select the primary column for information retrieval", data.columns, key="column_selection")
    st.write(f"You selected the column: {column_to_search}")
    
    # Query input for custom prompt
    query_template = st.text_input(
        "Enter a custom query (use '{entity}' as a placeholder for each entity)",
        value="Retrieve information about {entity}"
    )
    
    # Instructions for the user
    st.markdown("""
    **Instructions:**
    - Use `{entity}` in your query where you want the entity name to appear.
    - Example: "What is the population of {entity} in 2021?"
    - The application will replace `{entity}` with each value from the selected column.
    """)

    if st.button("Start Search"):
        if column_to_search not in data.columns:
            st.error("Please select a valid column for information retrieval.")
        else:
            # Get unique values from the selected column
            entities = data[column_to_search].dropna().unique()  # Process all entities
            st.write(f"Searching for information on entities in column '{column_to_search}'...")

            search_results = []

            for entity in entities:
                # Construct the query and fetch web results
                query = query_template.replace("{entity}", str(entity))
                web_results = search_serpapi(query)

                # Use the first snippet for processing
                if web_results and isinstance(web_results, list) and "snippet" in web_results[0]:
                    snippet = web_results[0]["snippet"]
                    # Construct a dynamic prompt for Groq API
                    prompt = (
                        f"Using the following text, provide a concise answer to the question: '{query}'.\n\n"
                        f"Text: {snippet}"
                    )
                    parsed_result = extract_information_with_groq(prompt)
                    # Check if the Groq API returned a useful result
                    if is_valid_groq_result(parsed_result):
                        # Add results to the list only if the parsed_result is valid
                        search_results.append({
                            "Entity": entity,
                            "Query": query,
                            "Groq Result": parsed_result,
                        })
                    else:
                        # Skip entities with unhelpful Groq API responses
                        continue
                else:
                    # Skip entities with insufficient data from web search
                    continue

            if search_results:
                # Display results
                result_df = pd.DataFrame(search_results)
                # Optionally, comment out the following two lines if you don't want to display the DataFrame
                st.write("### Final Results (Processed by Groq API)")
                st.dataframe(result_df)

                # Provide option to download the results as a CSV file
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name='ai_agent_dashboard_results.csv',
                    mime='text/csv',
                )
            else:
                st.warning("No valid results were obtained for any entities.")
