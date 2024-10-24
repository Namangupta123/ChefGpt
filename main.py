import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import Together
import os
# from dotenv import load_dotenv

# load_dotenv()
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_ENDPOINT"]=os.getenv("LANGSMITH_ENDPOINT")
# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGSMITH_API")
# os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
# Together_api = os.getenv("TOGETHER_KEY")
# model_name= os.getenv("NAME")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGSMITH"]["LANGSMITH_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["API_KEYS"]["LANGSMITH_API"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGSMITH"]["LANGSMITH_PROJECT"]

Together_api = st.secrets["API_KEYS"]["TOGETHER_KEY"]
model_name = st.secrets["MODEL"]["NAME"]
llm = Together(model=model_name, temperature=0.3, together_api_key=Together_api, max_tokens=300)

ui_translations = {
    'en': {
        'title': 'ChefGPT',
        'diet_label': 'Select any dietary restrictions (optional):',
        'reset_label': 'RESET',
        'error_message': 'Please provide some ingredients!',
        'success_message': 'Here’s your recipe based on your ingredients:',
        'previous_suggestions': 'Previous recipes:',
    }
}

dietary_restrictions = ['Low-carb', 'Low-fat', 'Gluten-free', 'Vegan', 'Vegetarian', 'High Protein']

template = """You are an AI culinary assistant specializing in Indian cuisine. Your task is to create a recipe based on the provided ingredients and dietary restrictions. Follow these steps to ensure the recipe meets the user's needs:

1. **Identify Ingredients**: Determine whether the provided ingredients are vegetarian or non-vegetarian.
2. **Check Dietary Restrictions**: Ensure the recipe adheres to any dietary restrictions specified by the user.
3. **Create Recipe**: Develop a recipe that has an Indian taste, using only the ingredients provided. If necessary, suggest minor substitutions to enhance the dish while respecting dietary restrictions.
4. **Provide Instructions**: Offer a simple, step-by-step procedure for preparing the dish. Keep the instructions brief and easy to follow.
5. **Handle Edge Cases**: If you cannot create a suitable recipe with the given ingredients and restrictions, return a message indicating that a recipe could not be found.

### Input Variables
- **Ingredients**: {{ingredients}}
- **Dietary Restrictions**: {{diet}}

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
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

def main():
    init_session_state()

    lang = ui_translations['en']

    st.set_page_config(page_title=lang['title'], layout="wide")

    st.title(lang['title'])

    if st.session_state['messages']:
        for msg in st.session_state['messages']:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])


    if diet_message := st.chat_input("Enter your ingredients (e.g., 'rice, cumin, turmeric')"):
        st.session_state['messages'].append({"role": "user", "content": diet_message})
        
        selected_diet = st.multiselect(lang['diet_label'], dietary_restrictions)
        
        with st.spinner("Fetching a recipe..."):
            try:
                input_data = {
                    "ingredients": diet_message,
                    "diet": ', '.join(selected_diet) if selected_diet else 'No restrictions'
                }

                response = (
                    prompt
                    | llm.bind(stop=["\nRecipe:"])
                    | StrOutputParser()
                )
                result = response.invoke(input_data)

                assistant_message = f"**Recipe:**\n{result}"
                st.session_state['messages'].append({"role": "assistant", "content": assistant_message})

                st.session_state['recipe_history'].append({
                    "ingredients": diet_message,
                    "diet": selected_diet,
                    "recipe": result
                })

                with st.chat_message("assistant"):
                    st.markdown(assistant_message)

            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.session_state['messages'].append({"role": "assistant", "content": error_message})
                st.error(error_message)

    with st.sidebar:
        st.header("About")
        st.write("Naman Gupta")
        st.write("[GitHub](https://github.com/Namangupta123)")
        st.write("[LinkedIn](https://www.linkedin.com/in/naman-gupta-cse)")
        st.write("This project, ChefGPT, helps you generate Indian recipes based on ingredients you provide, including any dietary restrictions like low-carb or vegan.")

        if st.button(lang['reset_label']):
            st.session_state['recipe_history'].clear()
            st.session_state['messages'].clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
