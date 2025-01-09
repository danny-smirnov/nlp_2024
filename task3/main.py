from flask import Flask, request
from utils import get_closest
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

print('Wait a bit, model is loading')
model = SentenceTransformer("all-mpnet-base-v2", device='cuda', model_kwargs={"torch_dtype": "bfloat16"})
print('Loading is complete')

@app.route("/")
def hello_world():
    return "I'm alive, you can send queries by /search?query=<query>"


@app.route('/search')
def search():
    query = request.args.get('query', type = str)
    print(query)
    emb = model.encode(query)
    closest = get_closest(emb)
    replies = "<br>".join(map(lambda x: f'<a href="{x[1]}">{x[0]}</a>', closest))
    return f'<h3>Closest results are</h3> <br><br> {replies}'

