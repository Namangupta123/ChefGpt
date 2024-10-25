import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI
# from dotenv import load_dotenv
import os

# load_dotenv()
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_ENDPOINT"]=os.getenv("LANGSMITH_ENDPOINT")
# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGSMITH_API")
# os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
# Together_api = os.getenv("TOGETHER_KEY")
# model_name= os.getenv("NAME")

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_ENDPOINT"]=st.secrets["LANGSMITH"]["LANGSMITH_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"]=st.secrets["API_KEYS"]["LANGSMITH_API"]
os.environ["LANGCHAIN_PROJECT"]=st.secrets["LANGSMITH"]["LANGSMITH_PROJECT"]

Mistral_api = st.secrets["API_KEYS"]["MISTRAL_KEY"]
model_name=st.secrets["MODEL"]["NAME"]
llm = ChatMistralAI(model=model_name, temperature=0.7, mistral_api_key=Mistral_api, max_tokens=10000)

ui_translations = {
    'en': {
        'title': 'ChefGPT',
        'ingredients_label': 'Enter your ingredients (e.g., "rice, cumin, turmeric"):',
        'diet_label': 'Select any dietary restrictions (optional):',
        'button_label': 'Get Recipe',
        'reset_label': 'RESET',
        'error_message': 'Please provide some ingredients!',
        'error_response':'Sorry not able to answer this time !!',
        'success_message': 'Here’s your recipe based on your ingredients:',
        'previous_suggestions': 'Previous recipes:',
    }
}

dietary_restrictions = ['Low-carb', 'Low-fat', 'Gluten-free', 'Vegan', 'Vegetarian', 'High Protein']

template = """Suggest an Indian recipe based on the user's available ingredients and dietary restrictions with a full procedure.

Human: You are an AI culinary assistant specializing in Indian cuisine. Your task is to create a recipe based on the provided ingredients and dietary restrictions. Follow these steps to ensure the recipe meets the user's needs:

1. **Identify Ingredients**: Determine whether the provided ingredients are vegetarian or non-vegetarian.

2. **Check Dietary Restrictions**: Ensure the recipe adheres to any dietary restrictions specified by the user.

3. **Create Recipe**: Develop a recipe that has an Indian taste, using only the ingredients provided. If necessary, suggest minor substitutions to enhance the dish while respecting dietary restrictions.

4. **Provide Instructions**: Offer a simple, step-by-step procedure for preparing the dish. Keep the instructions brief and easy to follow.

5. **Handle Edge Cases**: If you cannot create a suitable recipe with the given ingredients and restrictions, return a message indicating that a recipe could not be found.

### Input Variables

- **Ingredients**: {ingredients}

- **Dietary Restrictions**: {diet}

### Example

- **Ingredients**: "chickpeas, tomatoes, spinach, cumin, garlic"

- **Dietary Restrictions**: "vegan"

- **Recipe**: "Chickpea Spinach Curry"

  - **Instructions**:

    1. Heat oil in a pan and add cumin seeds.

    2. Add chopped garlic and sauté until golden.

    3. Add tomatoes and cook until soft.

    4. Stir in chickpeas and spinach, cook for 5 minutes.

    5. Season with salt and serve hot.

If you cannot find a suitable recipe, respond with: "Unfortunately, a recipe could not be created with the provided ingredients and dietary restrictions."
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
                        if(result==""):
                            st.error(lang['error_response'])
                            return

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