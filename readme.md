# Indian Recipe Bot

Welcome to the Indian Recipe Bot, a Streamlit application designed to help you discover delicious Indian recipes based on the ingredients you have at home.

## Features

- **Ingredient Input**: Enter the ingredients you have (e.g., "rice, cumin, turmeric") and the bot will suggest a complete recipe using those ingredients.
- **Recipe Suggestions**: Get step-by-step recipes tailored to the ingredients you've provided.
- **Recipe History**: View your previous recipe searches and results for easy reference.
- **Responsive UI**: A user-friendly interface that works well on both desktop and mobile devices.

## How to Use

1. **Enter Ingredients**: Start by typing the ingredients you have in the text area provided.
2. **Get Recipe**: Click the 'Get Recipe' button to submit your ingredients and receive a recipe suggestion.
3. **Reset**: Use the 'RESET' button to clear your history and start over with new ingredients.

## Installation

To run this application locally, you'll need Python and Streamlit installed. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-repository/indian-recipe-bot.git
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
- LangChain Cohere
- dotenv
- os

Ensure you have a `.env` file with your `COHERE_API_KEY` set up as shown in the `.env.example` file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.
