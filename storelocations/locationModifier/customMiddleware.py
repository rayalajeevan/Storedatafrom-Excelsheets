import socket
class GetIpMiddleware(object):
    def process_view(self,request, view_func, view_args, view_kwargs ):
        try:
            print(socket.gethostbyaddr(request.META['REMOTE_ADDR']))
        except:
            print(request.META['REMOTE_ADDR'])
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
