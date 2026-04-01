from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analisar_lexico(codigo):
    tokens = []
    palavras = codigo.replace(';', ' ;').split()

    for p in palavras:
        if p == 'int':
            tokens.append({'tipo': 'INT', 'valor': p})
        elif p == 'float':
            tokens.append({'tipo': 'FLOAT', 'valor': p})
        elif p == ';':
            tokens.append({'tipo': 'PONTO_VIRGULA', 'valor': p})
        elif p.isidentifier():
            tokens.append({'tipo': 'ID', 'valor': p})
        else:
            tokens.append({'tipo': 'ERRO', 'valor': f'Token inválido: {p}'})

    tokens.append({'tipo': '$', 'valor': '$'})
    return tokens

tokens = []
pos = 0
erros = []

def atual():
    if pos < len(tokens):
        return tokens[pos]
    return {'tipo': '$', 'valor': '$'}

def avancar():
    global pos
    pos += 1

def erro(msg):
    erros.append({
        'tipo': 'ERRO',
        'valor': msg,
        'posicao': pos
    })

def sincronizar():
    global pos
    while atual()['tipo'] not in ['PONTO_VIRGULA', '$']:
        pos += 1
    if atual()['tipo'] == 'PONTO_VIRGULA':
        pos += 1

def match(tipo):
    if atual()['tipo'] == tipo:
        avancar()
        return True
    else:
        erro(f"Esperado {tipo}, encontrado {atual()['valor']}")
        return False

def DECL():
    if not TIPO():
        sincronizar()
        return

    if not match('ID'):
        sincronizar()
        return

    if not match('PONTO_VIRGULA'):
        sincronizar()
        return

def TIPO():
    if atual()['tipo'] == 'INT':
        match('INT')
        return True
    elif atual()['tipo'] == 'FLOAT':
        match('FLOAT')
        return True
    else:
        erro("Esperado tipo (int ou float)")
        return False

def PROGRAMA():
    while atual()['tipo'] != '$':
        DECL()

@app.route('/analisar', methods=['POST'])
def analisar():
    global tokens, pos, erros

    data = request.get_json()
    codigo = data.get('codigo', '')

    tokens = analisar_lexico(codigo)

    pos = 0
    erros = []

    PROGRAMA()

    if erros:
        return jsonify(erros)
    else:
        return jsonify([{'tipo': 'SUCESSO', 'valor': 'Programa válido'}])

if __name__ == '__main__':
    app.run(debug=True)