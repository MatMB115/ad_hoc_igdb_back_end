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

        consulta_dinamica = self.query_parse(body)

        resultados = self.db.consulta(consulta_dinamica)
        json = [dict(row) for row in resultados]
        return jsonify(json)

    def query_parse(self, body):
        query = ""

        query += self.select_parse(body)

        query += self.join_parse(body)

        query += self.where_parse(body)

        query += " limit 10"
        print(query)
        return query

    def select_parse(self, body):
        select = body['select']
        select_fields = []
        
        select_query = "SELECT "

        if 'games' in select:
            for fields in select['games']:
                select_fields.append("g." + fields + " AS game_" + fields)

        if 'companies' in select:
            for fields in select['companies']:
                select_fields.append("cp." + fields + " AS companies_" + fields)

        if 'character' in select:
            for fields in select['character']:
                select_fields.append("ch." + fields + " AS character_" + fields)

        if 'plataform' in select:
            for fields in select['plataform']:
                select_fields.append("p." + fields + " AS plataform_" + fields)

        if 'genres' in select:
            for fields in select['genres']:
                select_fields.append("gr." + fields + " AS genres_" + fields)

        if 'gameModes' in select:
            for fields in select['gameModes']:
                select_fields.append("gmd." + fields + " AS games_modes_" + fields)

        if not select_fields:
            return 'SELECT *'

        for field in select_fields[:-1]:
            select_query += field + ", "

        select_query += select_fields[-1]

        return select_query


    def join_parse(self, body):
        join = body['join']
        join_query = " FROM "

        if 'games' in join:
            join_query += "games g"

            if 'companies' in join:
                join_query += " JOIN game_company gc ON g.id = gc.id_game JOIN companies cp ON gc.id_company = cp.id"

            if 'character' in join:
                join_query += " JOIN game_character gch ON gch.id_game = g.id JOIN character ch ON gch.id_character = ch.id"

            if 'plataform' in join:
                join_query += " JOIN game_plataform gp ON gp.id_game = g.id JOIN plataform p ON gp.id_plataform = p.id"

            if 'genres' in join:
                join_query += " JOIN game_genre gg ON gg.id_game = g.id JOIN genres gr ON gg.id_genre = gr.id"

            if 'gameModes' in join:
                join_query += " JOIN game_gamemode gms ON gms.id_game = g.id JOIN games_modes gmd ON gms.id_game_mode = gmd.id"

            return join_query

        elif len(join) == 1:
            if 'companies' in join:
                return ' FROM companies cp'

            if 'character' in join:
                return ' FROM character ch'

            if 'plataform' in join:
                return ' FROM plataform p'

            if 'genres' in join:
                return ' FROM genres gr'

            if 'gameModes' in join:
                return ' FROM games_modes gmd'

        else:
            raise ValueError("Tabelas não podem dar join")

    def where_parse(self, body):
        wheres = body['where']
        operators = body['operators']
        values = body['values']
        condition = body['condition']
        where_fields = []
        where_query = " WHERE "

        if 'games' in wheres:
            for where, operator, value in zip(wheres['games'], operators['games'], values['games']):
                where_fields.append(self.where_field_parse("g.", where, operator, value))

        if 'companies' in wheres:
            for where, operator, value in zip(wheres['companies'], operators['companies'], values['companies']):
                where_fields.append(self.where_field_parse("cp.", where, operator, value))

        if 'character' in wheres:
            for where, operator, value in zip(wheres['character'], operators['character'], values['character']):
                where_fields.append("ch." + where + " " + operator + " '" + value + "'")

        if 'plataform' in wheres:
            for where, operator, value in zip(wheres['plataform'], operators['plataform'], values['plataform']):
                where_fields.append(self.where_field_parse("p.", where, operator, value))

        if 'genres' in wheres:
            for where, operator, value in zip(wheres['genres'], operators['genres'], values['genres']):
                where_fields.append(self.where_field_parse("gr.", where, operator, value))

        if 'gameModes' in wheres:
            for where, operator, value in zip(wheres['gameModes'], operators['gameModes'], values['gameModes']):
                where_fields.append(self.where_field_parse("gmd.", where, operator, value))
        
        if not where_fields:
            return ''

        for field in where_fields[:-1]:
            where_query += field + condition

        where_query += where_fields[-1]

        return where_query
    
    def where_field_parse(self, table , where, operator, value):
        type_fields = {
            'name': 'text',
            'created_at': 'date',
            'updated_at': 'date',
            'url': 'text',
            'summary': 'text',
            'game_engines': 'text',
            'follows': 'int',
            'release_date': 'text',
            'country': 'text',
            'id': 'int', 
            'abbreviation': 'text',
            'alternative_name': 'text'
            }
        
        if type_fields[where] == 'int' or type_fields[where] == 'date':
            return " " + table + where + " " + operator + " " + str(value) + " "
        else:
            return " " + table + where + " " + operator + " '%" + str(value) + "%'" + " "
