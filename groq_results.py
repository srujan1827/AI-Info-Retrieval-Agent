def extract_information_with_groq(prompt):
    """
    Use the Groq SDK to extract structured information from the text.
    """
    client = Groq(api_key=" ")  # Replace with your Groq API key

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-groq-8b-8192-tool-use-preview",  # Use a valid model ID
            max_tokens=50,  # Limit the response length
            temperature=0.0,  # For deterministic output
        )
        # Extract and return the response content
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error in Groq SDK: {e}"

def is_valid_groq_result(result):
    """
    Determine if the Groq API result is valid and contains useful information.
    """
    # Define phrases that indicate unhelpful responses
    unhelpful_phrases = [
        "No valid results from web search.",
        "I couldn't find",
        "I'm sorry",
        "No information",
        "Error",
        "No relevant data",
        "not available",
        "cannot find",
        "No data",
        "unavailable"
    ]
    # Check if the result contains any unhelpful phrases
    for phrase in unhelpful_phrases:
        if phrase.lower() in result.lower():
            return False
    # Check if the result is empty or whitespace
    if not result.strip():
        return False
    return True
