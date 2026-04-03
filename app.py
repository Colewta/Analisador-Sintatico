from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

token_specification = [
    ('INT', r'\bint\b'),
    ('FLOAT', r'\bfloat\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),

    ('NUM', r'\d+(\.\d+)?'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('OP', r'[\+\-\*/=]'),
    ('PONTO_VIRGULA', r';'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),

    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('ERRO', r'.')
]

token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)

def analisar(codigo):
    tokens = []
    linha = 1
    coluna = 1

    for match in re.finditer(token_regex, codigo):
        tipo = match.lastgroup
        valor = match.group()

        if tipo == 'NEWLINE':
            linha += 1
            coluna = 1
            continue

        if tipo == 'SKIP':
            coluna += len(valor)
            continue

        if tipo == 'ERRO':
            tokens.append({
                'tipo': 'ERRO',
                'valor': valor,
                'linha': linha,
                'coluna': coluna
            })
        else:
            tokens.append({
                'tipo': tipo,
                'valor': valor,
                'linha': linha,
                'coluna': coluna
            })

        coluna += len(valor)

    return tokens

@app.route('/analisar', methods=['POST'])
def analisar_rota():
    data = request.get_json()
    codigo = data.get('codigo', '')

    tokens = analisar(codigo)
    return jsonify(tokens)

if __name__ == '__main__':
    app.run(debug=True)