from contextlib import closing

import grpc, signal
from django.db.models.expressions import connector

import not_pb2
import not_pb2_grpc
from concurrent import futures
import socket


def signal_handler(signal, frame):
    global exit
    exit = False

class send_notificationsServicer(not_pb2_grpc.send_notificationsServicer):
    def sendNotifications(self, request, context):
        with grpc.insecure_channel('localhost:7000') as channel:
            stub = not_pb2_grpc.send_notificationsStub(channel=channel)
            with closing(connector.connect(user='root', password="1234",
                                           host='127.0.0.1', database='gos1')) as connection:
                with connection.cursor(dictionary=True) as cursor:
                    signal.signal(signal.SIGINT, signal_handler)
                    insert_request = 'UPDATE zayavki_polz SET status=%s where id=%s'
                    # cursor.execute(insert_request, request.data)
                    data = request.data
                    print(request.data)
                    response = stub.sendNotifications(not_pb2.notifications(data=data))
                    # connection.commit()
                    # response = stub.sendNotifications(not_pb2.notifications(data=data_to_insert))
        num = 0

        message = b'['

        for item in request.data:
            num += 1
            message += b'{ "id": ' + bytes(str(item.id), encoding='utf-8') + \
                       b', "id_user": ' + bytes(str(item.id_user), encoding='utf-8') + \
                       b', "id_service": ' + bytes(str(item.id_service), encoding='utf-8') + \
                       b', "status": ' + bytes(str(item.status), encoding='utf-8') + b'}, '

        message = message[: -2]
        message += b']'

        print(message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 9020))
            s.sendall(message)

        return not_pb2.response(data=message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    not_pb2_grpc.add_send_notificationsServicer_to_server(send_notificationsServicer(), server=server)
    server.add_insecure_port('[::]:7000')
    server.start()
    print('server started')
    server.wait_for_termination()


main()
