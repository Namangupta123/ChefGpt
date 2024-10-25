import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import Together
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

Together_api = st.secrets["API_KEYS"]["TOGETHER_KEY"]
model_name=st.secrets["MODEL"]["NAME"]
llm = Together(model=model_name, temperature=0.3, together_api_key=Together_api, max_tokens=300)

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

template = """You are an AI culinary assistant specializing in Indian cuisine. Your task is to create a recipe based on the provided ingredients and any dietary restrictions. Follow these steps to ensure the recipe meets the user's needs:

### Inputs
- **Ingredients**: {{ingredients}}
- **Dietary Restrictions**: {{dietary_restrictions}}

### Task
1. **Ingredient Analysis**: Determine if the provided ingredients are vegetarian or non-vegetarian.
2. **Recipe Creation**: Develop an Indian dish using only the provided ingredients. Ensure the recipe adheres to any dietary restrictions specified.
3. **Procedure**: Outline a simple, step-by-step cooking procedure.
4. **Validation**: If a suitable recipe cannot be created with the given ingredients and restrictions, return a message indicating this.

### Example
- **Ingredients**: "chickpeas, tomatoes, onion, garlic, ginger"
- **Dietary Restrictions**: "vegan"

**Output**:
- **Recipe Name**: "Chickpea Masala"
- **Procedure**:
  1. Heat oil in a pan and sauté onions, garlic, and ginger until golden.
  2. Add tomatoes and cook until soft.
  3. Add chickpeas and spices, cook for 10 minutes.
  4. Serve hot with rice or bread.

### Output Format
- **Recipe Name**: [Name of the dish]
- **Procedure**: [Step-by-step instructions]

If unable to create a recipe, respond with: "Unable to create a recipe with the provided ingredients and restrictions."
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
                        if(result==None):
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