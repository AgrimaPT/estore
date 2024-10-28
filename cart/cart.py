# class Cart():
#     def __init__(self,request) :
#         self.session = request.session

#         #to  get the current session key if it exist
#         cart = self.session.get('session_key')

#         #if user is new no session key then create session key
#         if 'session_key' not in request.session:
#             cart= self.session['session_key'] = {}

#         self.cart=cart