import socket
from concurrent import futures
from contextlib import closing
import mysql.connector as connector

import grpc

import not_pb2
import not_pb2_grpc


class send_notificationsServicer(not_pb2_grpc.send_notificationsServicer):
    def sendNotifications(self, request, context):
        with grpc.insecure_channel('localhost:7000') as channel:
            stub = not_pb2_grpc.send_notificationsStub(channel=channel)
            with closing(connector.connect(user='root', password="1234",
                                           host='127.0.0.1', database='gos1')) as connection:
                with connection.cursor(dictionary=True) as cursor:
                    for i in request.data:
                        insert_request = f"UPDATE zayavki_polz SET status='{i.status}' where id={i.id}"
                        select_request = f"select username from polzovateli where id={i.id_user}"
                    cursor.execute(insert_request)
                    connection.commit()
                    cursor.execute(select_request)
                    data = cursor.fetchall()

        message = b'[' + b'{"username": "' + bytes(data[0]['username'], encoding='utf-8')
        message += b'"}' + b']'

        print(message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 9020))
            s.sendall(message)

        return not_pb2.response(data=message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    not_pb2_grpc.add_send_notificationsServicer_to_server(send_notificationsServicer(), server=server)
    server.add_insecure_port('[::]:7010')
    server.start()
    print('server started')
    server.wait_for_termination()


main()
