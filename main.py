import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import Together
from dotenv import load_dotenv
import os

load_dotenv()

Together_api = st.secrets["API_KEYS"]["TOGETHER_API_KEY"]
model_name=st.secrets["model"]["NAME"]
llm = Together(model=model_name, temperature=0.3, together_api_key=Together_api, max_tokens=300)

ui_translations = {
    'en': {
        'title': 'ChefGPT',
        'ingredients_label': 'Enter your ingredients (e.g., "rice, cumin, turmeric"):',
        'diet_label': 'Select any dietary restrictions (optional):',
        'button_label': 'Get Recipe',
        'reset_label': 'RESET',
        'error_message': 'Please provide some ingredients!',
        'success_message': 'Here’s your recipe based on your ingredients:',
        'previous_suggestions': 'Previous recipes:',
    }
}

dietary_restrictions = ['Low-carb', 'Low-fat', 'Gluten-free', 'Vegan', 'Vegetarian', 'High Protein']

template = """
Based on the ingredients provided and any dietary restrictions, 
suggest an recipe which have indian taste basically indian dish. 
Stick to only those ingredients provided by the user.
Decide whether the ingredients contain any non-veg or veg option and return the result accordingly.
If any dietary restrictions are provided, ensure the recipe adheres to them.
Provide a simple, step-wise procedure in brief.
If not able to find one return appropriate message.

Ingredients: {ingredients}
Dietary restrictions: {diet}
Recipe:
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Suggest an Indian recipe based on the user's available ingredients and dietary restrictions with a full procedure."),
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

    # Dietary restriction selection
    selected_diet = st.multiselect(lang['diet_label'], dietary_restrictions)

    if st.session_state['recipe_history']:
        st.subheader(lang['previous_suggestions'])
        for idx, entry in enumerate(st.session_state['recipe_history'], 1):
            st.write(f"{idx}. {entry['ingredients']} ({', '.join(entry['diet']) if entry['diet'] else 'No restrictions'})")
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
                            "ingredients": ingredients_input,
                            "diet": ', '.join(selected_diet) if selected_diet else 'No restrictions'
                        }

                        response = (
                            prompt
                            | llm.bind(stop=["\nRecipe:"])
                            | StrOutputParser()
                        )
                        result = response.invoke(input_data)

                        st.session_state['recipe_history'].append({
                            "ingredients": ingredients_input,
                            "diet": selected_diet,
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
