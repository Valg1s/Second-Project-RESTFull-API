from sweter import api
from resources.index import Index
from resources.about import About
from resources.auth.login import Login
from resources.auth.logout import Logout
from resources.auth.registration import Registration
from resources.contact import Contact
from resources.menu.account import Account
from resources.menu.calendar_ import Calendar
from resources.menu.coaches import Coaches
from resources.menu.players import Players
from resources.services import Services

api.add_resource(Index, "/", "/main")
api.add_resource(About, "/about")
api.add_resource(Services, "/services")
api.add_resource(Contact, '/contacts')
api.add_resource(Login, '/login')
api.add_resource(Registration, "/registration")
api.add_resource(Logout, "/logout")
api.add_resource(Account, "/account")
api.add_resource(Players, '/players')
api.add_resource(Coaches, '/coaches')
api.add_resource(Calendar, '/calendar')
