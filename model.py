# coding: utf-8
from sqlalchemy.orm import Session
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import StaleDataError
from flask_cors import CORS

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
    def __init__(self):
        self.db = AcessDB
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.route('/query', methods=['POST'])(self.get_consulta)
        self.app.run(host = '0.0.0.0')


    def run(self):
        self.app.run(debug=True)

    def get_consulta(self):
        body = request.get_json()

        consulta_dinamica = self.query_parse(body)
        if 'error' in consulta_dinamica:
            return consulta_dinamica, 400

        resultados = self.db.consulta(consulta_dinamica)
        json = [dict(row) for row in resultados]
        return jsonify(json)

    def query_parse(self, body):
        query = ""
        try:
            select, group = self.select_parse(body)

            query += select

            query += self.join_parse(body)

            query += self.where_parse(body)

            query += group

            query += self.order_parse(body)

            if body['limit'] != None:
                query += f" limit {body['limit']}"

            print(query)
            return query
        except ValueError as e:
            return ({'error': str(e)})

    def select_parse(self, body):
        select = body['select']
        select_fields = []
        agreggate_fields = body['func_agregada']
        group_field = []

        select_query = "SELECT "
        group_query = " GROUP BY "

        if 'games' in select:
            for fields in select['games']:
                if 'games' in agreggate_fields and agreggate_fields['games'][0] == fields:
                    select_fields.append(agreggate_fields['games'][1] + "(g." + fields + ")"+ " AS game_" + agreggate_fields['games'][1] + "_" +fields)
                else:
                    select_fields.append("g." + fields + " AS game_" + fields)
                    group_field.append("g." + fields)

        if 'companies' in select:
            for fields in select['companies']:
                if 'companies' in agreggate_fields and agreggate_fields['companies'][0] == fields:
                    select_fields.append(agreggate_fields['companies'][1] + "(cp." + fields + ")"+ " AS companies_" + agreggate_fields['companies'][1] + "_" +fields)
                else:
                    select_fields.append("cp." + fields + " AS companies_" + fields)
                    group_field.append("cp." + fields)

        if 'characters' in select:
            for fields in select['characters']:
                if 'characters' in agreggate_fields and agreggate_fields['characters'][0] == fields:
                    select_fields.append(agreggate_fields['characters'][1] + "(ch." + fields + ")"+ " AS characters_" + agreggate_fields['characters'][1] + "_" +fields)
                else:
                    select_fields.append("ch." + fields + " AS characters_" + fields)
                    group_field.append("ch." + fields)

        if 'plataforms' in select:
            for fields in select['plataforms']:
                if 'plataforms' in agreggate_fields and agreggate_fields['plataforms'][0] == fields:
                    select_fields.append(agreggate_fields['plataforms'][1] + "(p." + fields + ")"+ " AS plataforms_" + agreggate_fields['plataforms'][1] + "_" +fields)
                else:
                    select_fields.append("p." + fields + " AS plataforms_" + fields)
                    group_field.append("p." + fields)

        if 'genres' in select:
            for fields in select['genres']:
                if 'genres' in agreggate_fields and agreggate_fields['genres'][0] == fields:
                    select_fields.append(agreggate_fields['genres'][1] + "(gr." + fields + ")"+ " AS genres_" + agreggate_fields['genres'][1] + "_" +fields)
                else:
                    select_fields.append("gr." + fields + " AS genres_" + fields)
                    group_field.append("gr." + fields)

        if 'gameModes' in select:
            for fields in select['gameModes']:
                if 'gameModes' in agreggate_fields and agreggate_fields['gameModes'][0] == fields:
                    select_fields.append(agreggate_fields['gameModes'][1] + "(gmd." + fields + ")"+ " AS gameModes_" + agreggate_fields['gameModes'][1] + fields)
                else:
                    select_fields.append("gmd." + fields + " AS gameModes_" + fields)
                    group_field.append("gmd." + fields)

        if not select_fields:
            return 'SELECT *', ''

        for field in select_fields[:-1]:
            select_query += field + ", "

        select_query += select_fields[-1]

        if body['group_by'] and len(group_field) >= 1:
            for field in group_field[:-1]:
                group_query += field + ", "

            group_query += group_field[-1]
        else:
            if (len(select_fields) - len(group_field)) != 0 and len(select_fields) > 1:
                raise ValueError("Não é possível utilizar a função agregada com mais de um campo")
            else:
                group_query = ""

        return select_query, group_query


    def join_parse(self, body):
        join = body['join']
        join_query = " FROM "

        if 'games' in join:
            join_query += "games g"

            if 'companies' in join:
                join_query += " JOIN game_company gc ON g.id = gc.id_game JOIN companies cp ON gc.id_company = cp.id"

            if 'characters' in join:
                join_query += " JOIN game_character gch ON gch.id_game = g.id JOIN character ch ON gch.id_character = ch.id"

            if 'plataforms' in join:
                join_query += " JOIN game_plataform gp ON gp.id_game = g.id JOIN plataform p ON gp.id_plataform = p.id"

            if 'genres' in join:
                join_query += " JOIN game_genre gg ON gg.id_game = g.id JOIN genres gr ON gg.id_genre = gr.id"

            if 'gameModes' in join:
                join_query += " JOIN game_gamemode gms ON gms.id_game = g.id JOIN games_modes gmd ON gms.id_game_mode = gmd.id"

            return join_query

        elif len(join) == 1:
            if 'companies' in join:
                return ' FROM companies cp'

            if 'characters' in join:
                return ' FROM character ch'

            if 'plataforms' in join:
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
        if 'condition' in body:
            condition = body['condition']
        else:
            condition = "AND"

        where_fields = []
        where_query = " WHERE"

        if 'games' in wheres:
            for where, operator, value in zip(wheres['games'], operators['games'], values['games']):
                where_fields.append(self.where_field_parse("g.", where, operator, value))

        if 'companies' in wheres:
            for where, operator, value in zip(wheres['companies'], operators['companies'], values['companies']):
                where_fields.append(self.where_field_parse("cp.", where, operator, value))

        if 'characters' in wheres:
            for where, operator, value in zip(wheres['characters'], operators['characters'], values['characters']):
                where_fields.append(self.where_field_parse("ch.", where, operator, value))

        if 'plataforms' in wheres:
            for where, operator, value in zip(wheres['plataforms'], operators['plataforms'], values['plataforms']):
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
            'release_date': 'date',
            'country': 'text',
            'id': 'int',
            'abbreviation': 'text',
            'alternative_name': 'text'
            }

        if type_fields[where] == 'int':
            return " " + table + where + " " + operator + " " + str(value) + " "
        elif type_fields[where] == 'date':
            return " " + table + where + " " + operator + " '" + str(value) + "' "
        else:
            return " " + table + where + " " + operator + " '%" + str(value) + "%'" + " "

    def order_parse(self, body):
        order = body['order_by']
        if order == None:
            return ''

        order_query = " ORDER BY "
        if 'games' in order:
            order_query += "g." + order['games'][0] + " " + order['games'][1]

        if 'companies' in order:
            order_query += "cp." + order['companies'][0] + " " + order['companies'][1]

        if 'characters' in order:
            order_query += "ch." + order['characters'][0] + " " + order['characters'][1]

        if 'plataforms' in order:
            order_query += "p." + order['plataforms'][0] + " " + order['plataforms'][1]

        if 'genres' in order:
            order_query += "gr." + order['genres'][0] + " " + order['genres'][1]

        if 'gameModes' in order:
            order_query += "gmd." + order['gameModes'] + " " + order['gameModes'][1]

        return order_query
