# Imports
import sys

# Project Imports
import config
import public_proto_pb2
from session import session

api_url = 'https://pgorelease.nianticlabs.com/plfe/rpc'


def api_call(api_endpoint, api_requests):
    try:
        request_envelope = public_proto_pb2.RequestEnvelope()
        request_envelope.unknown1 = 2

        # TODO: What should this value be?
        request_envelope.rpc_id = 8145806132888207460

        # Add API request to request_envelope
        request_envelope.requests.MergeFrom(api_requests)

        # TODO: What should this value be?
        request_envelope.unknown12 = 989

        request_envelope.auth.provider = config.account_type
        request_envelope.auth.token.contents = config.access_token
        # TODO: What should this value be?
        request_envelope.auth.token.unknown13 = 59

        protocol_buffer = request_envelope.SerializeToString()

        headers = {'User-Agent': config.client_UA}
        response = session.post(api_endpoint, headers=headers, data=protocol_buffer, timeout=3)

        response_envelope = public_proto_pb2.ResponseEnvelope()
        response_envelope.ParseFromString(response.content)
        return response_envelope

    except Exception as error:
        if config.debug:
            print("[+] Failed API call:", error)
        return None


def get_api_endpoint():
    request_envelope = public_proto_pb2.RequestEnvelope()

    request1 = request_envelope.requests.add()
    request1.type = 2

    request2 = request_envelope.requests.add()
    request2.type = 126

    request3 = request_envelope.requests.add()
    request3.type = 4

    request4 = request_envelope.requests.add()
    request4.type = 129

    request5 = request_envelope.requests.add()
    request5.type = 5

    api_response = api_call(api_url, request_envelope.requests)

    try:
        config.api_endpoint = "https://%s/rpc" % api_response.api_url
    except Exception as error:
        if config.debug:
            print("[+] Failed to get API endpoint:", error)
        print("[*] Failed to get API endpoint\n")
        sys.exit(-1)

    print("[.] API Endpoint: %s" % config.api_endpoint)


def get_profile():
    request_envelope = public_proto_pb2.RequestEnvelope()

    request1 = request_envelope.requests.add()
    request1.type = 2

    api_response = api_call(config.api_endpoint, request_envelope.requests)

    if api_response:
        return api_response
    else:
        if config.debug:
            print("[+] Failed to retrieve profile", error)
        print("[*] Failed to retrieve profile\n")
        sys.exit(-1)
