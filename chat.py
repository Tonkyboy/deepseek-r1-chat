from openai import OpenAI, APIError, AuthenticationError

# Initialize client
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com/v1"
)

# Function to initialize conversation history
def initialize_history():
    return [{"role": "system", "content": "You are a helpful assistant."}]

# Initialize conversation history
conversation_history = initialize_history()

def chat_with_reasoner():
    global conversation_history  # Allow resetting history
    while True:
        # Get user input
        user_input = input("You: ").strip().lower()
        # Handle special commands
        if user_input in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input == "clear":
            conversation_history = initialize_history()
            print("Chat history cleared. Starting a new conversation...\n")
            continue

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        try:
            # Request a response from the reasoner model
            stream = client.chat.completions.create(
                model="deepseek-reasoner",  # Use the reasoner model
                messages=conversation_history,
                stream=True,
            )

            # Print reasoning and response
            print("\nReasoning:")
            reasoning_response = ""
            assistant_response = ""
            for chunk in stream:
                # Print reasoning content
                if chunk.choices[0].delta.reasoning_content:
                    reasoning = chunk.choices[0].delta.reasoning_content
                    print(reasoning, end="", flush=True)
                    reasoning_response += reasoning
                # Print assistant response
                if chunk.choices[0].delta.content:
                    if not assistant_response:
                        print("\n\nResponse:")
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    assistant_response += content

            # Append assistant's response to conversation history
            conversation_history.append({"role": "assistant", "content": assistant_response})
            print("\n")

        # Handle exceptions
        except AuthenticationError:
            print("Error: Authentication failed. Check your API key.")
        except APIError as e:
            print(f"API Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

# Start the chat
if __name__ == '__main__':
    chat_with_reasoner()
