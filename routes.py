import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.template
import MySQLdb
from datetime import datetime
import json



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/lib-login", LibrarianLogInHandler),
            (r"/user-login", UserLogInHandler),
            (r"/signup", SingUpHandler),
        ]
        super(Application,self).__init__(handlers)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    db = MySQLdb.connect("localhost","root","root","library" )

class HomeHandler(BaseHandler):
    def post(self):
        print("Home page handler called")
        self.set_default_headers()
        # loader = tornado.template.Loader(".")
        # self.write(loader.load("index.html").generate())
        # self.render("index.html")
	self.write("hi this is from backend")


class UserLogInHandler(BaseHandler):
    def post(self):
        print("user LogIn api hit")
        result = {}
        self.set_default_headers()
        username = self.get_argument("user_name")
        password = self.get_argument("password")
        self.write("you entered"+username+" "+password)

        sql_query = "select * from Users where UserName= '%s' and UserPass= '%s'" % (username,password)
        
        #print(sql_query)
        sql_query1 = "select * from Users"
        cursor = self.db.cursor()
        
	try:
           # Execute the SQL command
           cursor.execute(sql_query)
           # Fetch all the rows in a list of lists.
           row = cursor.fetchall()
           print(row)
           print(type(row))
           result["data"] = row
           
           
        except:
           print "Error: unable to fecth data"

        self.write(json.dumps(result , cls=DateTimeEncoder))

	
        


class LibrarianLogInHandler(BaseHandler):
    def post(self):
        print("LogIn api hit")
        self.set_default_headers()
        username = self.get_argument("user_name")
        password = self.get_argument("password")
        self.write(username+" "+password)





class SingUpHandler(BaseHandler):
    def post(self):
        print("SignUp api hit")
        self.set_default_headers()
        username = self.get_argument("user_name")
        password = self.get_argument("password")
        
        self.write(username+" "+password)



class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


if __name__ == "__main__":
    application = Application()
    app_server = tornado.httpserver.HTTPServer(application)
    app_server.listen(8081)
    print("Application Server started on port 8081 ")
    tornado.ioloop.IOLoop.current().start()











