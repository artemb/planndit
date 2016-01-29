from django.db import connection


def print_queries():
        for query in connection.queries:
            print(query)