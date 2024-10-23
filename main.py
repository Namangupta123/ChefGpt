import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
import os

load_dotenv()

cohere_api = st.secrets["API_KEYS"]["COHERE_API_KEY"]
cohere_llm = ChatCohere(model="command", temperature=0.3, cohere_api_key=cohere_api)

ui_translations = {
    'en': {
        'title': 'ChefGPT',
        'ingredients_label': 'Enter your ingredients (e.g., "rice, cumin, turmeric"):',
        'button_label': 'Get Recipe',
        'reset_label': 'RESET',
        'error_message': 'Please provide some ingredients!',
        'success_message': 'Here’s your recipe based on your ingredients:',
        'previous_suggestions': 'Previous recipes:',
    }
}

template = """
Based on the ingredients provided, suggest an Indian recipe limited to those ingredients only with step-wise and easy procedure.

Ingredients: {ingredients}
Recipe:
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Suggest an Indian recipe based on the user's available ingredients with full procedure."),
        ("human", template),
    ]
)

def init_session_state():
    if 'recipe_history' not in st.session_state:
        st.session_state['recipe_history'] = []

def main():
    init_session_state()

    lang = ui_translations['en']

    st.set_page_config(page_title=lang['title'], layout="wide")

    st.title(lang['title'])

    ingredients_input = st.text_area(lang['ingredients_label'], key="ingredients", placeholder="E.g., 'rice, cumin, turmeric'")

    if st.session_state['recipe_history']:
        st.subheader(lang['previous_suggestions'])
        for idx, entry in enumerate(st.session_state['recipe_history'], 1):
            st.write(f"{idx}. {entry['ingredients']}")
            st.code(entry['recipe'], language='markdown')

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button(lang['button_label']):
            if not ingredients_input:
                st.error(lang['error_message'])
            else:
                with st.spinner("Fetching a recipe..."):
                    try:
                        input_data = {
                            "ingredients": ingredients_input
                        }

                        response = (
                            prompt
                            | cohere_llm.bind(stop=["\nRecipe:"])
                            | StrOutputParser()
                        )
                        result = response.invoke(input_data)

                        st.session_state['recipe_history'].append({
                            "ingredients": ingredients_input,
                            "recipe": result
                        })

                        st.success(lang['success_message'])
                        st.code(result, language='markdown')

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.error(f"Details: {str(e)}")

    with col2:
        if st.button(lang['reset_label']):
            try:
                st.session_state['recipe_history'].clear()
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while resetting: {e}")

if __name__ == "__main__":
    main()
