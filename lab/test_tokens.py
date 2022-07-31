import pydantic
from tokenize import tokenize, generate_tokens
import io

input = '{"a": null, b: 35}'

def content():
    yield input

for tok in tokenize(io.BytesIO(input.encode()).readline):
    print(tok)
