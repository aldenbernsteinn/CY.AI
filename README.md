Create Your own Artificial Intelligence chatbot with CY.AI! 

Complete with a custom chat box and voice-to-voice conversation functions.

This program serves as a working template for users to expand upon and personalize.

ALL dependencies are completely free. WILL work instantly locally on a computer. Require VPS or Cloud Services to run on a Website.

Please see below on how to set up the AI Chat.

KEY:

Instructions will be Numbered (1.  , 2.   , 3.   )
--
* Are comments and information that could be helpful during your setup. 


=====================

# Step 1: Setting Up Ollama


1. Download Ollama here locally to your system: https://ollama.com/
   ---

*See this video for how to set this up properly for your respective systems:

https://www.youtube.com/watch?v=oI7VoTM9NKQ

=====================================

* Before proceeding to the next step, here is some information about Ollama models, compatibility, and how to customize other models besides Llama3 and Gemma2.

* The CY.AI.py python script was built while using Llama3 and Gemma2. Llama3 is great for natural conversation, while Gemma2 has the most up-to-date information and is better for informational queries than Llama3. I have created templates that are  included, meant for implementing custom models for both Lamma3 and Gemma2. If this sounds good to you then proceed and use the already created templates for Llama3 or Gemma2.

 -  * If you would prefer to use other models such as Phi3, or Mistral, then you will have to make your own custom yaml. yourself. The  parameters/template are handled differently for each and every model. Ollama provides the information you would need to set this up, but you will have to format it for yaml. 


=======================================

YAML
----------

# Step 2: Custom Files (Implement your Custom Models (How to name your model, change its personality, and more)


1. Create copies of either the Llama or Gemma2 template and put them somewhere you can access in your project directory
   --


* optional
- * I have included 2 template YAML files for you and set up the proper parameters/templates. The purpose of this is to create a new unique tampered model to use for your code.

- * I would recommend keeping the original template files and making copies of them when you want to make changes.



---------

# Step 3: The easy way to change the personality of your AI (Optional)

- * In your own copy of the yaml. file, see the "SYSTEM" portion, this part is responsible for telling the AI who it is, and how it should act.

- * To make changes you can say things in the following format "YOU are named John, YOU are a chef"

- * I recommend keeping your "SYSTEM" somewhat brief, be direct in your instructions

- * FYI: As you will see in the Gemma2 template, The "YOU never use * in your responses" is in place to prevent the AI from saying things such as "smirks" because without this modification it tends to talk in the third person. If this arises in your Llama3 model, consider adding "YOU never use * in your responses" as well.

- * Make sure to save your changes!

---------

# Step 4: Create the model


1. Note that the default name set in CY.AI.py will be GeneralAI, if you want your model to work immediately with no personal customization. run the following command in the terminal within the same location that the yaml. file is located:
   --

 ollama create General AI - f Gemma2_9bTemplate.yaml      OR      ollama create General AI - f Llama3yamltemplate.yaml (not as accurate)

* If you want to create multiple models or change the name of the models then execute the following command:

ollama create (NAME OF YOUR MODEL) - f (NAME OF YOUR YAML FILE)

2. Run the following command in ANY terminal to see if Ollama has created your new model
   --

ollama list

* Note you will have to change the model name in the CY.AI.py to reflect your changes, there will be instructions on this later once your python file is set up properly). Also You can create as many models as you want with Ollama.



=========================================

PYTHON Setting up your Python environment
--
# Step 5: 

1. Create a new Python file in your project directory
   --

---

# Step 6: Ensure Dependencies

1. Create virtual environment
   --  
python -m venv venv

2.Activate virtual environment (Windows)
   --

venv\Scripts\activate

OR
--

2. Activate virtual environment (macOS/Linux)
   --
source venv/bin/activate

3. Install packages from requirements.txt
   --
pip install -r requirements.txt

---

# Step 7: Install NLTK in your PY environment 

1. Run the following python code (in your  py) once to download the necessary NLTK data:
   --

import nltk
nltk.download('wordnet')

2. remove nltk.download('wordnet') once downloaded
   --

3. Deactivate virtual environment
   --
deactivate

-----

# Step 8:  Setting Up CY.AI

1. Copy and paste contents from the downloaded CY.AI.py into your python file.
   --

---

# Step 9: Implementing custom personalities (Optional)

* IF you changed the model name in your yaml. file please navigate to the following part of the python code (line 436 defaulted):

if __name__ == "__main__":
    model = "GeneralAI"  # Replace with the specific model name..
.....


1. Change the model name to match the one you created with this command: ollama create (NAME OF YOUR MODEL) - f (NAME OF YOUR YAML FILE)
   --

=======

Run and modify however you would like! 

