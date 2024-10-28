# ChefGPT

Welcome to ChefGPT, a Streamlit application designed to help you discover delicious Indian recipes based on the ingredients you have at home and any dietary restrictions you might follow. 

This application uses `st.secrets` for securely managing API keys and other sensitive information.

## Features

- **Ingredient Input**: Enter the ingredients you have (e.g., "rice, cumin, turmeric") and the bot will suggest a complete Indian recipe using those ingredients.
- **Dietary Restrictions**: Select any dietary restrictions you have, and the bot will tailor the recipe accordingly.
- **Recipe Suggestions**: Get step-by-step Indian recipes tailored to the ingredients and dietary restrictions you've provided.
- **Recipe History**: View your previous recipe searches and results for easy reference.
- **Responsive UI**: A user-friendly interface that works well on both desktop and mobile devices.

## How to Use

1. **Enter Ingredients**: Start by typing the ingredients you have in the text area provided.
2. **Select Dietary Restrictions**: Choose any dietary restrictions from the multi-select dropdown.
3. **Get Recipe**: Click the 'Get Recipe' button to submit your ingredients and dietary preferences and receive a recipe suggestion.
4. **Reset**: Use the 'RESET' button to clear your history and start over with new ingredients.

## Installation

To run this application locally, you'll need Python and Streamlit installed. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-repository/chefgpt.git
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run main.py
   ```

## Dependencies

- Streamlit
- LangChain Mistral
- python-dotenv
- os

Ensure you have a `.env` file with your API keys set up as shown in the `.env.example` file. Alternatively, you can use `st.secrets` for managing your API keys as demonstrated in the `main.py` file. Comments in the `main.py` file provide guidance on how to switch between using `.env` files and `st.secrets`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.
