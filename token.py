import re

# Define regex patterns for different token types
KEYWORDS = r'\b(data|set|if|then|else|do|end|proc|run|in|by|merge|retain|input|output|length)\b'
OPERATORS = r'[+\-*/=<>!&|^]'
NUMERIC = r'\b\d+(\.\d+)?\b'
VARIABLE = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
STRING = r'"([^"\\]|\\.)*"'  # To match strings with escaped characters
COMMENT = r'/*.*?*/|//.*?$'  # To match block comments or line comments

# Combine all patterns
TOKEN_REGEX = f'({KEYWORDS}|{OPERATORS}|{NUMERIC}|{VARIABLE}|{STRING}|{COMMENT})'


def tokenize_sas(code):
    # Use re.findall to find all matches based on the combined pattern
    tokens = re.findall(TOKEN_REGEX, code)

    # Filter out empty matches
    return [token for token in tokens if token.strip()]


# Example SAS code to tokenize
sas_code = """
data mydata;
  set old_data;
  if age >= 18 then do;
    output;
  end;
run;
"""

tokens = tokenize_sas(sas_code)

# Output the tokenized code
for token in tokens:
    print(f"Token: {token}")
