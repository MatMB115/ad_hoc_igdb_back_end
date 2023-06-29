# coding: utf-8
from sqlalchemy.orm import Session
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import StaleDataError

from DAO import *
from mapeamento import *

from flask import Flask, jsonify, request
import json

class AcessDB:

    def consulta(query_string):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            consulta = session.execute(query_string)
            session.commit()
            session.close()
            return consulta.fetchall() 
        except:
            return []

class API:
    app = Flask(__name__)
    def __init__(self):
        self.db = AcessDB
        self.app = Flask(__name__)
        self.app.route('/query', methods=['POST'])(self.get_consulta)
        self.app.run(debug=True)

    def run(self):
        self.app.run(debug=True)
    
    def get_consulta(self):
        body = request.get_json()

        consulta_dinamica = self.query_parse(body);

        resultados = self.db.consulta(consulta_dinamica)
        json = [dict(row) for row in resultados]
        return jsonify(json)
    
    def query_parse(self, body):
        query = ""
        
        query += self.select_parse(body)

        return query
    
    def select_parse(self, body):
        select = body['select']
        select_fields = []
        select_query = "SELECT "

        if 'games' in select:
            for game_fields in select['games']:
                select_fields.append("g." + game_fields + " AS game_" + game_fields)
        
        for field in select_fields[:-1]:
            select_query += field + ", "
        
        select_query += select_fields[-1]
        
        select_query += " FROM games g limit 5"

        return select_query


    def join_parse(self, body):
        pass

    def where_parse(self, body):
        pass
