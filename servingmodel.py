import joblib
import pandas as pd
import json
import numpy as np
from flask import Flask, jsonify, request
import tensorflow as tf

import os
import threading

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder

@app.route("/", methods=['GET', 'POST'])
def call_home(request = request):
    print(request.values)
    return "SERVER IS RUNNING!"

#http://127.0.0.1:8080/modelo01?casa_propria=1&renda=333&genero_male=0
#http://127.0.0.1:8080/modelo01?p1=1&p2=3
#http://127.0.0.1:8080/modelo01?idade=2&renda=2222&genero_male=0&casa_propria=1

@app.route("/modelo01", methods=['GET', 'POST'])
def call_modelo01(request = request):

    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        idade_str = request.values.get('idade')
        renda_str = request.values.get('renda')
        genero_male_str = request.values.get('genero_male')
        casa_propria_str = request.values.get('casa_propria')

        if idade_str is None:
            raise NotImplementedError("Parametro idade obrigatorio.")
        if renda_str is None:
            raise NotImplementedError("Parametro renda obrigatorio.")
        if genero_male_str is None:
            raise NotImplementedError("Parametro genero_male obrigatorio.")
        if casa_propria_str is None:
            raise NotImplementedError("Parametro casa_propria obrigatorio.")

        idade = 0
        renda = 0
        genero_male = 0
        casa_propria = 0

        try:
            idade = int(idade_str)
            renda = int(renda_str)
            genero_male = int(genero_male_str)
            casa_propria = int(casa_propria_str)
        except:
            raise Exception("Os parâmetros devem ser numericos.")

        idade_25 = 0
        idade_25_34 = 0
        idade_35_44 = 0
        idade_45_54 = 0
        idade_55_64 = 0
        idade_65_74 = 0
        idade_74 = 0

        if idade <= 25:
            idade_25 = 1
        elif idade <= 34:
            idade_25_34 = 1
        elif idade <= 44:
            idade_35_44 = 1
        elif idade <= 54:
            idade_45_54 = 1
        elif idade <= 64:
            idade_55_64 = 1
        elif idade <= 74:
            idade_65_74 = 1
        else:
            idade_74 = 1

        novo_cliente = {"casa_propria": int(casa_propria), "renda": int(renda), "genero_male": int(genero_male), "idade_25-34": int(idade_25_34),
             "idade_35-44": int(idade_35_44), "idade_45-54": int(idade_45_54), "idade_55-64": int(idade_55_64),
             "idade_65-74": int(idade_65_74), "idade_<25": int(idade_25), "idade_>74": int(idade_74)}

        entrada = np.array(list(novo_cliente.values())).reshape(1, -1)

        ret = json.dumps({'idade': str(idade),
                          'renda': str(renda),
                          'genero_male': str(genero_male),
                          'casa_propria': str(casa_propria),
                          'mensagem': "Obrigado pela chamada de API",
                          'autor': "Miller"}, cls=NpEncoder)

        #Fazer uma previsão com novos dados
        #prediction = modelo01.predict(entrada)

        previsao = modelo01.predict_proba(entrada)[:, 1]
        # print("Probabilidade de inadimplência: ", previsao)

        ret = json.dumps({'Probabilidade de inadimplencia:': list(previsao)}, cls=NpEncoder)

        return app.response_class(response=ret, mimetype='application/json')


    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')


@app.route("/modelo02", methods=['GET', 'POST'])
def call_modelo02(request = request):

    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        idade_str = request.values.get('idade')
        renda_str = request.values.get('renda')
        genero_male_str = request.values.get('genero_male')
        casa_propria_str = request.values.get('casa_propria')

        if idade_str is None:
            raise NotImplementedError("Parametro idade obrigatorio.")
        if renda_str is None:
            raise NotImplementedError("Parametro renda obrigatorio.")
        if genero_male_str is None:
            raise NotImplementedError("Parametro genero_male obrigatorio.")
        if casa_propria_str is None:
            raise NotImplementedError("Parametro casa_propria obrigatorio.")

        idade = 0
        renda = 0
        genero_male = 0
        casa_propria = 0

        try:
            idade = int(idade_str)
            renda = int(renda_str)
            genero_male = int(genero_male_str)
            casa_propria = int(casa_propria_str)
        except:
            raise Exception("Os parâmetros devem ser numericos.")

        idade_25 = 0
        idade_25_34 = 0
        idade_35_44 = 0
        idade_45_54 = 0
        idade_55_64 = 0
        idade_65_74 = 0
        idade_74 = 0

        if idade <= 25:
            idade_25 = 1
        elif idade <= 34:
            idade_25_34 = 1
        elif idade <= 44:
            idade_35_44 = 1
        elif idade <= 54:
            idade_45_54 = 1
        elif idade <= 64:
            idade_55_64 = 1
        elif idade <= 74:
            idade_65_74 = 1
        else:
            idade_74 = 1

        novo_cliente = {"casa_propria": int(casa_propria), "renda": int(renda), "genero_male": int(genero_male),
                        "idade_25-34": int(idade_25_34),
                        "idade_35-44": int(idade_35_44), "idade_45-54": int(idade_45_54),
                        "idade_55-64": int(idade_55_64),
                        "idade_65-74": int(idade_65_74), "idade_<25": int(idade_25), "idade_>74": int(idade_74)}

        entrada = np.array(list(novo_cliente.values())).reshape(1, -1)

        ret = json.dumps({'idade': str(idade),
                          'renda': str(renda),
                          'genero_male': str(genero_male),
                          'casa_propria': str(casa_propria),
                          'mensagem': "Obrigado pela chamada de API",
                          'autor': "Miller"}, cls=NpEncoder)

        # Fazer uma previsão com novos dados
        prediction = modelo02.predict(entrada)

        ret = json.dumps({'Classe do novo cliente': list(prediction)}, cls=NpEncoder)

        return app.response_class(response=ret, mimetype='application/json')


    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')



@app.route("/modelo03", methods=['GET', 'POST'])
def call_modelo03(request = request):

    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        idade_str = request.values.get('idade')
        renda_str = request.values.get('renda')
        genero_male_str = request.values.get('genero_male')
        casa_propria_str = request.values.get('casa_propria')

        if idade_str is None:
            raise NotImplementedError("Parametro idade obrigatorio.")
        if renda_str is None:
            raise NotImplementedError("Parametro renda obrigatorio.")
        if genero_male_str is None:
            raise NotImplementedError("Parametro genero_male obrigatorio.")
        if casa_propria_str is None:
            raise NotImplementedError("Parametro casa_propria obrigatorio.")

        idade = 0
        renda = 0
        genero_male = 0
        casa_propria = 0

        try:
            idade = int(idade_str)
            renda = int(renda_str)
            genero_male = int(genero_male_str)
            casa_propria = int(casa_propria_str)
        except:
            raise Exception("Os parâmetros devem ser numericos.")

        idade_25 = 0
        idade_25_34 = 0
        idade_35_44 = 0
        idade_45_54 = 0
        idade_55_64 = 0
        idade_65_74 = 0
        idade_74 = 0

        if idade <= 25:
            idade_25 = 1
        elif idade <= 34:
            idade_25_34 = 1
        elif idade <= 44:
            idade_35_44 = 1
        elif idade <= 54:
            idade_45_54 = 1
        elif idade <= 64:
            idade_55_64 = 1
        elif idade <= 74:
            idade_65_74 = 1
        else:
            idade_74 = 1

        novo_cliente = {"casa_propria": int(casa_propria), "renda": int(renda), "genero_male": int(genero_male),
                        "idade_25-34": int(idade_25_34),
                        "idade_35-44": int(idade_35_44), "idade_45-54": int(idade_45_54),
                        "idade_55-64": int(idade_55_64),
                        "idade_65-74": int(idade_65_74), "idade_<25": int(idade_25), "idade_>74": int(idade_74), 'clusters': 0}

        entrada = np.array(list(novo_cliente.values())).reshape(1, -1)

        ret = json.dumps({'idade': str(idade),
                          'renda': str(renda),
                          'genero_male': str(genero_male),
                          'casa_propria': str(casa_propria),
                          'mensagem': "Obrigado pela chamada de API",
                          'autor': "Miller"}, cls=NpEncoder)

        # Fazer uma previsão com novos dados
        prediction = modelo03.predict(entrada)

        ret = json.dumps({'Classe do novo cliente': list(prediction)}, cls=NpEncoder)

        return app.response_class(response=ret, mimetype='application/json')


    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')

#teste
@app.route("/soma", methods=['GET', 'POST'])
def call_soma(request = request):
    print(f"Sou o processo server, id: {os.getpid()}, thread: {threading.current_thread().ident}")
    print(request.values)

    try:
        p1 = request.values.get('p1')
        if p1 is None:
            raise NotImplementedError("Parametro p1 obrigatório.")
        p2 = request.values.get('p2')

        try:
            par1 = float(p1)
            par2 = float(p2)
        except:
            raise Exception("Os parâmetros da soma devem ser numéricos.")

        ret = json.dumps({'resultado': par1 + par2,
                          'operacao': "soma",
                          'mensagem': "Obrigado pela chamada de API",
                          'autor': "Miller"}, cls=NpEncoder)
        return app.response_class(response=ret, status=200, mimetype='application/json')
    except Exception as err:
        ret = json.dumps({"error_message": str(err)})
        return app.response_class(response=ret, status=500, mimetype='application/json')



if __name__ == '__main__':
    modelo01 = joblib.load('../models/modelo01.joblib')
    modelo02 = joblib.load('../models/modelo02.joblib')
    modelo03 = joblib.load('../models/modelo03.joblib')
    #modelo01 = joblib.load('../models/propensaoinadimplencia.joblib')
    #modelo02 = joblib.load('../models/clusterizacaoclassificacao.joblib')
    #modelo03 = joblib.load('../models/clusterizacaoclassificacao.joblib')
    #modelo03 = joblib.load('../models/modelodeeplearning.joblib')

    app.run(port=8080)



