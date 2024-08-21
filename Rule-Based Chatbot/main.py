import re


def chatbot_response(user_input):
    # Convert user input to lowercase for case-insensitive matching
    user_input = user_input.lower()

    # Define responses based on patterns
    if re.search(r'hello|hi|hey', user_input):
        return "Hello! How can I assist you today?"
    elif re.search(r'how are you|how are you doing', user_input):
        return "I'm just a bot, but I'm doing great! How about you?"
    elif re.search(r'what is your name|who are you', user_input):
        return "I'm your friendly chatbot here to help you out!"
    elif re.search(r'thank you|thanks', user_input):
        return "You're welcome! If you have more questions, feel free to ask."
    elif re.search(r'bye|goodbye|see you', user_input):
        return "Goodbye! Have a great day!"
    else:
        # Fallback response for unrecognized inputs
        return "I'm sorry, I don't understand that. Can you please rephrase?"


def main():
    print("Chatbot: Hi! I'm here to help you. Type 'bye' to exit.")

    while True:
        # Get user input
        user_input = input("You: ")

        # Get chatbot response
        response = chatbot_response(user_input)

        # Print the response
        print("Chatbot:", response)

        # Exit the loop if the user says goodbye
        if re.search(r'bye|goodbye|see you', user_input.lower()):
            break


if __name__ == "__main__":
    main()
