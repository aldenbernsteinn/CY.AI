Create Your own Personal Artificial Intelligence Chatbot Application From CY.AI! 
--

This program serves as a working template for users to personalize, expand, and create their own AI chat applications.

Includes a custom chat box and custom voice-to-voice function that facitilitaes conversation between user and AI.

ALL dependencies are completely free. WILL work instantly locally on a computer. Require VPS or Cloud Services to run on a Website.

Please see instructions bellow:

===================================

KEY:

- Instructions will be formated like this
   --
* comments and information that could be helpful during your setup are formated like this


===================================

# Step 1: Setting Up Ollama


- Download Ollama here locally to your system: https://ollama.com/
   ---

* See this video for how to set this up properly for your respective systems:

https://www.youtube.com/watch?v=oI7VoTM9NKQ

===================================

- Before proceeding to the next step, here is some information about Ollama models, compatibility, and how to customize other models besides Llama3 and Gemma2.

- The CY.AI.py python script was built while using Llama3 and Gemma2. Llama3 is great for natural conversation, while Gemma2 has the most up-to-date information and is better for informational queries than Llama3. I have created templates that are  included, meant for implementing custom models for both Lamma3 and Gemma2. If this sounds good to you then proceed and use the already created templates for Llama3 or Gemma2.

* If you would prefer to use other models such as Phi3, or Mistral, then you will have to make your own custom yaml. yourself. The  parameters/template are handled differently for each and every model. Ollama provides the information you would need to set this up, but you will have to format it for yaml. 


===================================

# Step 2: Copy Template YAML. to Project Directory


- Create copies of either the Llama or Gemma2 template and put them somewhere you can access in your project directory
   --
* I have included 2 template YAML files for you and set up the proper parameters/templates.


===================================

# Step 3: Change the personality of your AI (Optional)

* I would recommend keeping the original template files and making renamed copies of them such as "Custom.yaml"

* In your new copy of the yaml. file, see the "SYSTEM" portion, this part is responsible for telling the AI who it is, and how it should act.

* To make changes you can say things in the following format "YOU are named John, YOU are a chef"

* I recommend keeping your "SYSTEM" somewhat brief, be direct in your instructions

* FYI: As you will see in the Gemma2 template, The "YOU never use * in your responses" is in place in the templates to prevent the AI from saying things such as "smirks" because without this modification it tends to talk in the third person. If this arises in your Llama3 model, consider adding "YOU never use * in your responses" as well.

* Make sure to save your changes!

* Be sure to run the Optional command seen in Step 4 and Step 9 as well when you reach it.

===================================

# Step 4: Create the model

*Note that the default name set in CY.AI.py will be GeneralAI, please do the following if you want your model to work later with the placeholder model in the CY.AI.py script (this can easily be changed later)

- Run the following command in the terminal within the same location as the yaml.:
   --

 ollama create General AI - f Gemma2_9bTemplate.yaml      OR      ollama create General AI - f Llama3yamltemplate.yaml (not as accurate)

* OR (Optional): If you want to create your own model using your own custom yaml file with a different name:

- ollama create (NAME YOUR MODEL) - f (NAME OF YOUR CUSTOM YAML FILE)

- Run the following command in ANY terminal to see if Ollama has created your new model
   --

- ollama list

* Note you will have to change the model name in the CY.AI.py to reflect your changes, there will be instructions on this later once your python file is set up properly). Also You can create as many models as you want with Ollama.  (See Step 9 for more information on how to do this)

===================================

# Step 5: 

-- Create a new Python file in your project directory
   --

---

# Step 6: Ensure Dependencies

- First, Create virtual environment
  --  
- python -m venv venv

- Then do one of the following:
   --

   - Activate virtual environment (Windows)
      --

   - venv\Scripts\activate

- OR
   --

   - Activate virtual environment (macOS/Linux)
      --
   - source venv/bin/activate

- Next, Install packages from requirements.txt
   --
- pip install -r requirements.txt

===================================

# Step 7: Install NLTK in your PY environment 

- Run the following python code (in your  py) once to download the necessary NLTK data:
   --

- import nltk
  nltk.download('wordnet')

- Remove nltk.download('wordnet') once downloaded
   --

- Lastly, Deactivate virtual environment
   --
- deactivate

===================================

# Step 8:  Setting Up CY.AI

- Copy and paste contents from the downloaded CY.AI.py into your python file.
   --

===================================

# Step 9 (Optional) : Implementing Custom Personalities (See Step 4)

- IF you changed the model name in your yaml. file please navigate to the following part of the python code (line 436 defaulted):
--

if __name__ == "__main__":
    model = "GeneralAI"  # Replace "GeneralAI" with the specific model name used..
.....

* If unsure of your model name use comamnd "ollama list" in your terminal to find the exact model name you used.

===================================

# Step 10: Run

- Modify or expand this code however you would like!
