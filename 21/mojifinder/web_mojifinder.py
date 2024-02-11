from pathlib import Path
from unicodedata import name

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from charindex import InvertedIndex

STATIC_PATH = Path(__file__).parent.absolute() / 'static'

app = FastAPI(
    title='Mojifinder Web',
    description='Search for Unicode characters by name.'
)


def init(app):
    app.state.index = InvertedIndex()
    app.state.form = (STATIC_PATH / 'form.html').read_text()


init(app)


class CharName(BaseModel):
    char: str
    name: str


@app.get('/search', response_model=list[CharName])
async def search(q: str):
    chars = sorted(app.state.index.search(q))
    return ({'char': c, 'name': name(c)} for c in chars)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def form():
    return app.state.form


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='web_mojifinder:app', reload=True)
