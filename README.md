# Create Your Own Personal Voiced Artificial Intelligence Chatbot Application From CY.AI

This program serves as a working template for users to personalize, expand, and create their own voice operated AI chat applications, facilitating voice-to-voice conversation between the user and AI.

All dependencies are completely free and will work instantly locally on a computer. However, to run on a website, you will require VPS or Cloud Services.

## Instructions

### Step 1: Setting Up Ollama

- **Download Ollama**: [Download Ollama here](https://ollama.com/).
- **Setup Guide**: Watch [this video](https://www.youtube.com/watch?v=oI7VoTM9NKQ) for setup instructions specific to your system.

**Note**: The `CY.AI.py` script was built using Llama3 and Gemma2. Llama3 is great for natural conversation, while Gemma2 provides the most up-to-date information. Templates are included for both Llama3 and Gemma2. If you prefer other models like Phi3 or Mistral, you'll need to create your own custom YAML file. Ollama provides information to set this up, but you’ll need to format it for YAML.

### Step 2: Copy Template YAML to Project Directory

- **Templates Provided**: Two YAML templates (for Llama3 and Gemma2) are included. Copy the relevant template to your project directory.

### Step 3 (Optional): Change the Personality of Your AI

- **Customize YAML**: Rename and modify a copy of the YAML file, especially the "SYSTEM" portion, which dictates the AI’s behavior and personality. For example, you can say: "YOU are named John, YOU are a chef."
- **Avoid Third-Person Responses**: If the AI talks in third person, add "YOU never use * in your responses" to prevent this behavior.

### Step 4: Create the Model

- **Default Model Name**: The script uses `GeneralAI` by default. To create your model, run:
    ```bash
    ollama create GeneralAI -f Gemma2_9bTemplate.yaml
    ```
    or
    ```bash
    ollama create GeneralAI -f Llama3yamltemplate.yaml
    ```
- **Custom Model**: To use a custom YAML file:
    ```bash
    ollama create (NAME_YOUR_MODEL) -f (NAME_OF_YOUR_CUSTOM_YAML_FILE)
    ```
- **Verify Model Creation**:
    ```bash
    ollama list
    ```

**Note**: Update the model name in `CY.AI.py` if you used a custom name. You can create multiple models with Ollama (see Step 9 for more details).

### Step 5: Create a New Python File

- **Setup**: Create a new Python file in your project directory.

### Step 6: Ensure Dependencies

- **Create Virtual Environment**:
    ```bash
    python -m venv venv
    ```
- **Activate Virtual Environment**:
    - **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    - **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
- **Install Packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Step 7: Install NLTK in Your Python Environment

- **Download NLTK Data**:
    ```python
    import nltk
    nltk.download('wordnet')
    ```
- **Remove Download Command**: Once downloaded, remove `nltk.download('wordnet')`.
- **Deactivate Virtual Environment**:
    ```bash
    deactivate
    ```

### Step 8: Setting Up CY.AI

- **Copy Script**: Copy and paste the contents of `CY.AI.py` into your Python file.

### Step 9 (Optional): Implementing Custom Personalities

- **Update Model Name**: If you changed the model name in your YAML file, update it in the Python code (line 436 by default):
    ```python
    if __name__ == "__main__":
        model = "GeneralAI"  # Replace with the specific model name used.
    ```
- **Check Model Name**: Use `ollama list` to find your model name if unsure.

### Step 10: Run

- **Modify and Expand**: Feel free to modify or expand the code as needed!

---

**Enjoy creating your personalized AI chatbot!** If you have any questions or need further assistance, don't hesitate to ask.
