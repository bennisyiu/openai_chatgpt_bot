from tkinter import *
import customtkinter
import openai
import os
import pickle

# Initiate App
root = customtkinter.CTk()
root.title("Bennis' ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico')  # https://tkinter.com/ai_lt.ico

# Set Color Scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Submit to ChatGPT


def speak():
    # check if there is anything submitted
    if chat_entry.get():
        # do something
        file_name = "api_key"
        try:
            if os.path.isfile(file_name):
                # Open the file
                input_file = open(file_name, 'rb')
                # Load the data from the file into a variable
                file_content = pickle.load(input_file)

                # Query ChatGPT
                # define our API key to ChatGPT
                openai.api_key = file_content
                # create an instance
                openai.Model.list()
                # Define our Query
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=chat_entry.get(),
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                my_text.insert(END, response["choices"][0]["text"].strip())
                my_text.insert(END, "\n\n")

            else:
                # Create the file
                input_file = open(file_name, 'wb')
                # Close the file
                input_file.close()
                # Error msg - you need an api key
                my_text.insert(
                    END, "\n\n Please input your API Key to talk with ChatGPT. Get one here: https://platform.openai.com/account/api-keys")
        except Exception as e:
            my_text.insert(END, f"\n\n There was an error: {e}")

    else:
        my_text.insert(
            END, "\n\n No input provided. Are you trying to say something?")
    chat_entry.delete(0, END)

# Clear the Screens


def clear():
    # Clear the main text box
    my_text.delete(1.0, END)
    # Clear the query entry box
    chat_entry.delete(0, END)

# DO API stuff


def key():
    # Define our filename
    file_name = "api_key"
    try:
        if os.path.isfile(file_name):
            # Open the file
            input_file = open(file_name, 'rb')
            # Load the data from the file into a variable
            file_content = pickle.load(input_file)

            # Output content to our entry box
            api_entry.insert(END, file_content)
        else:
            # Create the file
            input_file = open(file_name, 'wb')
            # Close the file
            input_file.close()
    except Exception as e:
        my_text.insert(END, f"\n\n There was an error: {e}")

    # Resize App -> Larger
    root.geometry('600x750')
    # Reshow API Frame
    api_frame.pack(pady=30)


# Save the API Key


def save_key():
    # Define our filename
    file_name = "api_key"

    # Open file
    output_file = open(file_name, 'wb')

    # Add the data to the file
    pickle.dump(api_entry.get(), output_file)

    # Delete Entry Box
    api_entry.delete(0, END)
    # HIde API Frame
    api_frame.pack_forget()
    # Resize App -> Smaller
    root.geometry('600x600')


# Create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add text widget to get ChatGPT Responses
my_text = Text(text_frame,
               bg="#343638",
               width=65,
               bd=1,
               fg="#d6d6d6",
               relief="flat",
               wrap=WORD,
               selectbackground="#1f5385")
my_text.grid(row=0, column=0)

# Create scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame, command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

# Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry widget to type content to ChatGPT
chat_entry = customtkinter.CTkEntry(root, placeholder_text="Type something to ChatGPT ...",
                                    width=535,
                                    height=50,
                                    border_width=2)
chat_entry.pack(pady=10)

# Create button frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create buttons

# 1. Speak button
submit_button = customtkinter.CTkButton(button_frame,
                                        text="Speak to ChatGPT",
                                        command=speak)
submit_button.grid(row=0, column=0, padx=25)

# 2. Clear button
clear_button = customtkinter.CTkButton(button_frame,
                                       text="Clear Response",
                                       command=clear)
clear_button.grid(row=0, column=1, padx=35)

# 3. API button
api_button = customtkinter.CTkButton(button_frame,
                                     text="Update API Key",
                                     command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
                                   placeholder_text="Enter Your API Key",
                                   width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
                                          text="Save Key",
                                          command=save_key)
api_save_button.grid(row=0, column=1, padx=10)


root.mainloop()
