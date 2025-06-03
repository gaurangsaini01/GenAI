import tiktoken

text = "Hello I am a text ready to be tokenized"
encoder = tiktoken.encoding_for_model("gpt-4o")

encoded = encoder.encode(text)

print("Encoded text is:",encoded)

decoded = encoder.decode(encoded)
print("The Decoded binary is:",decoded)