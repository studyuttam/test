import openai

openai.api_key = 'your-api-key'

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt="Feedback: The product was good but the delivery was late.\n\nSummarize:",
  temperature=0.3,
  max_tokens=60
)

summary = response.choices[0].text.strip()
st.write(summary)