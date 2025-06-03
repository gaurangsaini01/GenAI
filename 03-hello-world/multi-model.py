from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json

load_dotenv()

gptClient = OpenAI()
geminiClient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# System prompt for GPT
SYSTEM_PROMPT = """
You are a Mathematics and coding expert. Solve any problem using these steps:
Step 1 : Think
Step 2 : Validate
Repeat steps in this sequence until reaching the result.

Rules:
- Perform one step at a time.
- Respond in strict JSON format like:
  {"step":"Think", "content":"your thinking..."}
  {"step":"Validate", "content":"your validation..."}
  {"step":"Result", "content":"final answer..."}
"""

user_question = input("Enter your math or coding problem: ")
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question}]

while True:
    gpt_response = gptClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type":"json_object"},
    )
    
    gpt_content = gpt_response.choices[0].message.content.strip()

    try:
        parsed = json.loads(gpt_content)
    except json.JSONDecodeError:
        print("❌ GPT response was not valid JSON. Here's what came back:\n", gpt_content)
        break

    step = parsed.get("step")
    content = parsed.get("content")
    print(f"🧠 GPT ({step}): {content}")

    if step == "Result":
        break

    messages.append({"role": "assistant", "content": gpt_content})

    # Validating using Gemini if step is "Think"
    if step == "Think":
        gemini_response = geminiClient.models.generate_content(
            model="gemini-1.5-flash",  
            contents=f"Validate the following step: '{content}'",
        )
        validation_text = gemini_response.text.strip()
        print(f"✅ Gemini (Validate): {validation_text}")
        validation_json = {
            "step": "Validate",
            "content": validation_text
        }
        messages.append({"role": "assistant", "content": json.dumps(validation_json)})
