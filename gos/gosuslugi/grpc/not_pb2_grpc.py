# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import not_pb2 as not__pb2


class send_notificationsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sendNotifications = channel.unary_unary(
                '/send_notifications/sendNotifications',
                request_serializer=not__pb2.notifications.SerializeToString,
                response_deserializer=not__pb2.response.FromString,
                )


class send_notificationsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sendNotifications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_send_notificationsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sendNotifications': grpc.unary_unary_rpc_method_handler(
                    servicer.sendNotifications,
                    request_deserializer=not__pb2.notifications.FromString,
                    response_serializer=not__pb2.response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'send_notifications', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class send_notifications(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def sendNotifications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/send_notifications/sendNotifications',
            not__pb2.notifications.SerializeToString,
            not__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)