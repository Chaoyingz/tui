# tui

Turning ideas into web app fast.

tui is a project inspired by [FastUI](https://github.com/pydantic/FastUI), designed to simplify and accelerate web application development. It is built on the powerful combination of FastAPI for backend efficiency and Shadcn UI for creating stylish and responsive user interfaces.

## Example

Create a file main.py with:

```python
from fastapi import FastAPI
from tui import init_tui
from tui import components as c

app = FastAPI()

@app.get("/")
def read_root() -> c.AnyComponents:
    return [c.Button(children="Hello tui!")]

init_tui(app)
```

Then run `uvicorn main:app` in your terminal and visit http://127.0.0.1:8000/ in your browser.

## Docs

Visit https://tui-w8c1.onrender.com/ to view the documentation.
