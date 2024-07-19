import requests
import json
import re
import speech_recognition as sr
from threading import Thread, Event, Lock, Condition
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import os
import time
import enchant
import queue
import threading
import nltk
from nltk.corpus import wordnet as wn

def is_verb(word):
    """Check if a word is a verb using WordNet."""
    synsets = wn.synsets(word, pos=wn.VERB)
    return bool(synsets)

# Replace with your Ollama api endpoint (should be correct as is)
api_url = "http://localhost:11434/api/chat"

# List to maintain conversation history
conversation_history = []

# Event to signal termination
terminate_event = Event()

# Lock and condition for managing TTS operations
tts_lock = Lock()
tts_condition = Condition(tts_lock)

# Global variable to track TTS status
tts_active = False

def correct_spaces(text):
    # Initialize enchant English dictionary
    d = enchant.Dict("en_US")

    # Define patterns to detect and correct common incorrectly spaced words and contractions, because we are creating our own chat we need to
    # Do various spelling and spacing corrections to ensure what is being fed by the API is correctly received, doing this will allow more customization in the future!
    patterns = [
        (r'\b(I)\s+\'\s*(m|d|ll|ve|s)\b', r'\1\'\2'),    # Matches "I ' m", "I ' d", "I ' ll", "I ' ve", "I ' s"
        (r'\b(you|they|we)\s+\'\s*(re|ve|ll|d|s)\b', r'\1\'\2'),  # Matches "you ' re", "they ' re", "we ' ve", etc.
        (r'\b(it|that|he|she)\s+\'\s*(s|ll|d|s)\b', r'\1\'\2'),  # Matches "it ' s", "that ' ll", "he ' d", etc.
        (r'\b(\w+)\s+\'\s*s\b', r'\1\'s'),  # Matches possessive forms like "John ' s", "dog ' s", etc.
        (r'\b(can|should|could|would|might)\s+\'\s*not\b', r'\1 not'),  # Matches contractions like "can ' not", "should ' not", etc.
        (r'\b(he|she|it)\s+\'\s*(s|d)\b', r'\1\'\2'),  # Matches contractions like "he ' s", "she ' s", "he ' d", etc.
        (r'\b(is|was)\s+n\s+\'\s*t\b', r'\1n\'t'),  # Matches negative contractions like "is n ' t", "was n ' t", etc.
        (r'\b(its)\s+\'\s*\b', r'\1\''),  # Matches possessive pronouns like "its ' ".
        (r'\b(can|wo|should|would|must|might|ought)\s+\'\s*(t|ve|d|s)\b', r'\1\'\2'),  # Matches "can ' t", "wo ' ve", "should ' d", etc.
        (r'\b(\w+)\s+\'\s*\b', r'\1\''),  # Matches plural possessives like "dogs '", "cats '", etc.
        (r'\b(children|women|men|people|feet|teeth)\s+\'\s*s\b', r'\1\'s'),  # Matches irregular possessives like "children ' s", "women ' s", etc.
        (r'\b(would|should|could)\s+\'\s*(n|ve|t|re)\b', r'\1\'\2'),  # Matches "wouldn ' t", "shouldn ' t", "couldn ' t", etc.
        (r'\s+([,.!?])', r'\1'),  # Remove space before punctuation
        (r'([,.!?])(\w)', r'\1 \2'),  # Ensure space after punctuation
        (r'\*', r'')  # Remove asterisks
    ]

    # Apply corrections based on patterns
    corrected_text = text
    for pattern, replacement in patterns:
        corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.IGNORECASE)

    # Split text into words
    words = corrected_text.split()

    # Validate and correct words using enchant, preserving original words
    corrected_words = []
    for word in words:
        # Check if the word exists in dictionary
        if d.check(word):
            corrected_words.append(word)  # Word is correct, keep it unchanged
        else:
            corrected_words.append(word.replace(' ', ''))  # Remove spaces but keep the word as is

    # Join corrected words into a corrected sentence
    corrected_sentence = ' '.join(corrected_words)

    # Replace escaped apostrophes with regular apostrophes
    corrected_sentence = corrected_sentence.replace(r'\'', "'")
    
    return corrected_sentence

def fix_spacing(text):
    d = enchant.Dict("en_US")
    words = text.split()
    corrected_words = []
    
    i = 0
    while i < len(words):
        word = words[i]
        combined_word = word

        # Check if the next word exists
        j = i + 1
        while j < len(words):
            next_word = words[j]
            combined_word += next_word

            # If combined_word is valid, check further
            if d.check(combined_word):
                # Check if the next word (if exists) is invalid
                if j + 1 < len(words) and not d.check(words[j + 1]):
                    break  # Exit loop to combine word

                # Check if two subsequent words are invalid
                if j + 2 < len(words) and not d.check(words[j + 1]) and not d.check(words[j + 2]):
                    break  # Exit loop to combine word
            j += 1
        
        # Check if the current and next word form a verb
        if j < len(words) and is_verb(word + words[j]):
            combined_word = word + words[j]
            corrected_words.append(combined_word)
            i = j + 1  # Skip the combined words
        # If a valid combined word was found
        elif d.check(combined_word):
            corrected_words.append(combined_word)
            i = j + 1  # Skip the combined words
        else:
            corrected_words.append(word)
            i += 1  # Move to the next word
    
    # Join the corrected words back into a single string
    corrected_text = ' '.join(corrected_words)
    return corrected_text

def clean_text(text):
    # Remove extra spaces and ensure proper spacing around punctuation
    text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'([,.!?])(\w)', r'\1 \2', text)  # Ensure space after punctuation
    return text.strip()

# Initialize a queue for TTS
tts_queue = queue.Queue()

def speak_text_from_queue():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        speak_text(text)
        tts_queue.task_done()

# Start the TTS thread
tts_thread = threading.Thread(target=speak_text_from_queue, daemon=True)
tts_thread.start()

def send_chat_message(model, user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    data = {
        "model": model,
        "messages": conversation_history
    }

    try:
        response = requests.post(api_url, json=data, stream=True)
        response.raise_for_status()

        dingus_response = ""
        partial_response = ""
        paragraph = ""

        for line in response.iter_lines():
            if line:
                line_data = line.decode('utf-8')
                
                if "<start_of_turn>" in line_data or "<end_of_turn>" in line_data:
                    continue
                
                response_data = json.loads(line_data)
                if response_data.get("done", False):
                    break
                if 'message' in response_data and response_data['message']['role'] == 'assistant':
                    content = clean_text(response_data['message']['content'])
                    partial_response += content.strip() + " "
                    
                    while any(p in partial_response for p in ['.', '!', '?', ',']):
                        for p in ['.', '!', '?', ',']:
                            if p in partial_response:
                                part, partial_response = partial_response.split(p, 1)
                                part += p
                                part_corrected = correct_spaces(part.strip())
                                part_corrected = fix_spacing(part_corrected)
                                
                                if len(paragraph) + len(part_corrected) + 1 <= 100:
                                    paragraph += part_corrected + " "
                                else:
                                    print(f"AI: {paragraph.strip()}")
                                    if paragraph.strip():
                                        tts_queue.put(paragraph.strip())
                                    paragraph = part_corrected + " "

        if paragraph:
            print(f"AI: {paragraph.strip()}")
            if paragraph.strip():
                tts_queue.put(paragraph.strip())
            dingus_response += paragraph.strip() + " "

        if partial_response.strip():
            partial_response_corrected = correct_spaces(partial_response.strip())
            partial_response_corrected = fix_spacing(partial_response_corrected)
            if len(partial_response_corrected) <= 100:
                print(f"AI: {partial_response_corrected.strip()}")
                if partial_response_corrected.strip():
                    tts_queue.put(partial_response_corrected.strip())
                dingus_response += partial_response_corrected.strip() + " "
            else:
                while len(partial_response_corrected) > 100:
                    chunk = partial_response_corrected[:100]
                    print(f"AI: {chunk.strip()}")
                    if chunk.strip():
                        tts_queue.put(chunk.strip())
                    dingus_response += chunk.strip() + " "
                    partial_response_corrected = partial_response_corrected[100:]
                if partial_response_corrected.strip():
                    print(f"AI: {partial_response_corrected.strip()}")
                    tts_queue.put(partial_response_corrected.strip())
                    dingus_response += partial_response_corrected.strip() + " "

        conversation_history.append({
            "role": "assistant",
            "content": dingus_response.strip()
        })

        return dingus_response.strip()

    except requests.exceptions.RequestException as e:
        print("Error connecting to the API:", e)
        return None

def get_initial_greeting(model):
    initial_user_message = "hello"
    conversation_history.append({
        "role": "user",
        "content": initial_user_message
    })

    data = {
        "model": model,
        "messages": conversation_history
    }

    try:
        response = requests.post(api_url, json=data, stream=True)
        response.raise_for_status()

        dingus_response = ""
        partial_response = ""

        for line in response.iter_lines():
            if line:
                line_data = line.decode('utf-8')
                
                if "</start_of_turn>" in line_data or "</end_of_turn>" in line_data:
                    continue
                
                response_data = json.loads(line_data)
                if response_data.get("done", False):
                    break
                if 'message' in response_data and response_data['message']['role'] == 'assistant':
                    content = clean_text(response_data['message']['content'])
                    partial_response += content.strip() + " "
                    
                    while any(p in partial_response for p in ['.', '!', '?']):
                        for p in ['.', '!', '?']:
                            if p in partial_response:
                                sentence, partial_response = partial_response.split(p, 1)
                                sentence += p
                                sentence_corrected = correct_spaces(sentence.strip())
                                sentence_corrected = fix_spacing(sentence_corrected)
                                print(f"AI: {sentence_corrected}")
                                dingus_response += sentence_corrected + " "
                                tts_queue.put(sentence_corrected)  # Add to queue

        dingus_response += partial_response.strip()
        if partial_response.strip():
            partial_response_corrected = correct_spaces(partial_response.strip())
            partial_response_corrected = fix_spacing(partial_response_corrected)
            print(f"AI: {partial_response_corrected}")
            tts_queue.put(partial_response_corrected)  # Add to queue

        conversation_history.append({
            "role": "assistant",
            "content": dingus_response.strip()
        })

    except requests.exceptions.RequestException as e:
        print("Error connecting to the API:", e)

# Make sure to properly shut down the TTS thread when the application ends
def stop_tts_thread():
    tts_queue.put(None)
    tts_thread.join()

# Call this function to stop the TTS thread before exiting the application
# stop_tts_thread()

def remove_emojis(text):
    # Define a regex pattern to match all emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def speak_text(text):
    global tts_active

    with tts_condition:
        tts_active = True

    with tts_lock:
        # Remove emojis from the text
        text = remove_emojis(text)
        tts = gTTS(text=text, lang='en', tld='co.uk')  # Set the language to English with UK accent
        tts.save("output.mp3")
        
        # Load the audio file
        audio = AudioSegment.from_mp3("output.mp3")
        
        # Export the audio to a temporary file in the current directory
        temp_wav_path = os.path.join(os.getcwd(), "temp_audio.wav")
        audio.export(temp_wav_path, format="wav")
        
        # Play the audio file using simpleaudio
        wave_obj = sa.WaveObject.from_wave_file(temp_wav_path)
        play_obj = wave_obj.play()
        
        play_obj.wait_done()
        
        # Clean up the audio files
        os.remove("output.mp3")
        os.remove(temp_wav_path)
        
    # Delay to ensure no gaps in speech recognition activation
    time.sleep(.001)

    with tts_condition:
        tts_active = False
        tts_condition.notify_all()  # Notify that TTS has finished

def prepare_next_text(next_text):
    # Queue the next text for TTS playback
    tts_queue.put(next_text)

# Updated speak_text_from_queue function to manage next_text
def speak_text_from_queue():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        
        # Speak the current text
        speak_text(text)
        tts_queue.task_done()


# Start the TTS thread
tts_thread = threading.Thread(target=speak_text_from_queue, daemon=True)
tts_thread.start()

def real_time_speech_recognition():
    global tts_active

    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    while not terminate_event.is_set():
        with tts_condition:
            # Wait until TTS is not active
            while tts_active:
                tts_condition.wait()
        
        if terminate_event.is_set():
            break
        
        with sr.Microphone() as source:
            print("Speak your prompt...")
            audio = recognizer.listen(source)
        
        try:
            user_prompt = recognizer.recognize_google(audio)
            print(f"You (Speech): {user_prompt}")
            if user_prompt.lower() == 'quit':
                terminate_event.set()  # Set the event to terminate
                print("Ending the conversation.")
                return None
            return user_prompt
        
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
            return None
        
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None




def handle_user_input():
    global conversation_history
    
    while True:
        user_input = input("Type your prompt (Type 'quit' to end): ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            terminate_event.set()  # Set the event to terminate
            print("Ending the conversation.")
            break
        
        dingus_response = send_chat_message(model, user_input)

if __name__ == "__main__":
    model = "GeneralAI"  # Replace with the specific model name
    get_initial_greeting(model)
    
    # Start thread for handling typed input
    input_thread = Thread(target=handle_user_input)
    input_thread.start()
    
    # Listen to user prompt via speech
    while not terminate_event.is_set():
        user_input = real_time_speech_recognition()
        
        if not user_input:
            continue
        
        if user_input and user_input.lower() == 'quit':
            terminate_event.set()  # Set the event to terminate
            print("Ending the conversation.")
            break
        
        dingus_response = send_chat_message(model, user_input)
    
    # Wait for the input thread to complete
    input_thread.join()
    
    # Stop TTS thread properly
    stop_tts_thread()
