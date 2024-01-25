import streamlit as st
import os
from main import Main
import shutil
import config

os.environ['GRADIENT_ACCESS_TOKEN'] = config.GRADIENT_ACCESS_TOKEN
os.environ['GRADIENT_WORKSPACE_ID'] = config.GRADIENT_WORKSPACE_ID

def chatbot_response(query_engine,user_input):
# Simple rule-based responses
    if "hello" in user_input.lower():
        return "Hello! How can I help you today?"
    elif "how are you" in user_input.lower():
        return "I'm just a computer program, but thanks for asking!"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        response = query_engine.query(user_input)
        return response

st.set_page_config(page_title="ChatBot")

# Display the app title
st.title("Interact with PDF's using Llama index")


def main():
    
    file_paths = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    # Define the folder to save PDF files
    save_folder = "document"

    # Ensure the save folder exists
    os.makedirs(save_folder, exist_ok=True)

    # List to store uploaded PDF file paths
    uploaded_pdfs = []

    # Display uploaded PDFs and allow the user to clear them
    if file_paths:
        for file_path in file_paths:
            # Save the uploaded PDF file to the documents folder
            pdf_filename = os.path.join(save_folder, file_path.name)
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(file_path.read())

            # Append the PDF file path to the list
            uploaded_pdfs.append(pdf_filename)

    # Allow the user to clear a specific PDF in the sidebar
    st.sidebar.title("Uploaded PDFs")
    if uploaded_pdfs:
        pdf_to_clear = st.sidebar.selectbox("Select PDF to clear:", uploaded_pdfs, key="clear_pdf")
        if st.sidebar.button("Clear PDF"):
            # Remove the selected PDF from the list
            uploaded_pdfs.remove(pdf_to_clear)

            # Delete the PDF file
            os.remove(pdf_to_clear)

            # Display a success message in the sidebar
            st.sidebar.success(f"PDF cleared: {pdf_to_clear}")
    else:
        st.sidebar.warning("No PDFs uploaded yet.")


    if file_paths:

        main_obj = Main("document")
       
        llm = main_obj.create_llm()
        model = main_obj.create_model()

        query_engine = main_obj.create_query_engine(llm,model)

        user_input = st.text_input("You: ", "")

        if st.button("Ask"):
            bot_response = chatbot_response(query_engine,user_input)
            st.write(bot_response.response)
    
    
if __name__ == "__main__":
    main()
    shutil.rmtree("document")
    os.makedirs("document", exist_ok=True)