import openai
import os

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Please follow the format "gpt-35-turbo_team{ID}", and replace "ID" with your team number.
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # "gpt-35-turbo_team{ID}".format(ID="426")

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = AZURE_OPENAI_KEY

client = openai.AzureOpenAI(
  azure_endpoint=AZURE_OPENAI_ENDPOINT,
  api_key=AZURE_OPENAI_KEY,
  api_version="2023-05-15"
)

print("Running chron job\n")

print("Found outdated dependencies: ")
print("  Flask v2.3.1 (Current) -> v3.1.2\n")
print("Searching *.py files for dependency Flask:")
print("  app.py\n")
print("Retrieving breaking changes for Flask v2.3.1...")
print("Sending update request to GPT...")

languageDefault = "Python3"

updateDefault = "Flask v3.0.1"

breakingDefault = """
    Remove previously deprecated code. #5223

    Deprecate the __version__ attribute. Use feature detection, or importlib.metadata.version("flask"), instead. #5230

    Restructure the code such that the Flask (app) and Blueprint classes have Sans-IO bases. #5127

    Allow self as an argument to url_for. #5264

    Require Werkzeug >= 3.0.0.
"""

breakingMessage = "These breaking changes were introduced in {update}: ```{breaking}```"

codeDefault = """
import flask

if __name__ == "__main__":
  print(flask.__version__)
  app.run(debug=True)
"""

codeMessage = "Given the breaking changes, what should this {language} code be instead? ```{code}```"

# systemMessage = """
# You are a helpful coding assistant. When given a list of breaking changes in a language
# or framework update, and code using that language or framework, you will provide a bulleted
# list of steps on how to update the code to fix the breaking changes, with the updated code
# at the end. Ensure that the resulting code does not include any deprecated fields or functions
# included in the list of breaking changes.
# """

systemMessage = """
You are a helpful coding assistant. When given a list of breaking changes in a language
or framework update, and code using that language or framework, you will return ONLY updated code 
to fix the breaking changes (no comments before or after). Ensure that the resulting code does not include any deprecated 
fields or functions included in the list of breaking changes. If there is any text returned that is
not part of the code, insert it as a comment.
"""


def get_response(language, update, breaking, code):
    breakingContent = breakingMessage.format(update=update, breaking=breaking)
    codeContent = codeMessage.format(language=language, code=code)
    response = client.chat.completions.create(
        # engine=DEPLOYMENT_NAME,
        model="gpt-35-turbo-16k_canadaeast",
        messages=[
            {"role": "system", "content": systemMessage},
            {"role": "user", "content": breakingContent},
            {"role": "user", "content": codeContent}
        ],
        # temperature=0.5
    )

    # print(response)
    return (response.usage.total_tokens, response.choices[0].message.content)


(usage, code) = get_response(languageDefault, updateDefault, breakingDefault, codeDefault)
print(f"Used {usage} tokens\n")
print(f"New code:\n{code}\n")

cve_default = """
  CVE-2023-30861
"""

print("CVEs for Flask v2.3.1:")
print(cve_default)

