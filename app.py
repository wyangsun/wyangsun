import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import db,MyAnsible
import hashlib
from tornado.options import define, options


define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		session = db.DBSession()
		List_hosts = session.query(db.Hostinfo).filter().all()
		items = []
		for o in List_hosts:
			items.append([ o.hid ] + [ o.hostname ] + [ o.groupname ] + [ o.lan_ip ] + [ o.wan_ip ])
		session.close()
		self.render('index.html', user=self.current_user, items = items )

class LoginHandler(BaseHandler):
	def get(self):
		self.render('login.html')
	def post(self):
		WyMd5 = hashlib.md5()
		session = db.DBSession()
		getusername = self.get_argument("username")
		getpassword = self.get_argument("password")
		WyMd5.update(getpassword)
		DBuser = session.query(db.User).filter(db.User.name==getusername).one()
		if DBuser.password == WyMd5.hexdigest():
			self.set_secure_cookie("user", self.get_argument("username"), expires_days=0.2 )
			self.redirect("/")
		else:
			wrong=self.get_secure_cookie("wrong")
			if wrong==False or wrong == None:
				wrong=0  
			self.set_secure_cookie("wrong", str(int(wrong)+1))
			self.write(' login <a href="/login"> error </a> '+str(wrong))
		session.close()

class RegHandler(BaseHandler):
	session = db.DBSession()
	session.close()

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect(self.get_argument("next", "/"))

class HostHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		session = db.DBSession()
		List_hosts = session.query(db.Hostinfo).filter().all()
		items = []
		for o in List_hosts:
			items.append([ o.hid ] + [ o.hostname ] + [ o.groupname ] + [ o.lan_ip ] + [ o.wan_ip ])
		session.close()
		self.render("host.html",title="Manage Hosts",items = items)
	def post(self):
		action = self.get_argument("action")
		if "add" == action:
			session = db.DBSession()
			new_hosts = db.Hostinfo(hostname = self.get_argument("hosts"),groupname = self.get_argument("group"),lan_ip = self.get_argument("lan"),wan_ip = self.get_argument("wan"))
			session.add(new_hosts)
			session.commit()
			session.close()
		if "delete" == action:
			session = db.DBSession()
			session.query(db.Hostinfo).filter(db.Hostinfo.hid == self.get_argument("id")).delete()
			session.commit()
			session.close()
		if "update" == action:
			session = db.DBSession()
			update_hosts = db.Hostinfo(hid=self.get_argument("id"),hostname = self.get_argument("hosts"),groupname = self.get_argument("group"),lan_ip = self.get_argument("lan"),wan_ip = self.get_argument("wan"))
			session.merge(update_hosts)
			session.commit()
			session.close()
		if "command" == action:
			self.redirect("/ansible")
		MyAnsible.EditAnsibleHost()
		self.redirect("/host")

class AnsibleHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		session = db.DBSession()
		List_command = session.query(db.Commandhistory).order_by(db.Commandhistory.datetime.desc()).limit(10).all()
		items = []
		for o in List_command:
			items.append([ o.cid ] + [ o.hosts ] + [ o.module ] + [ o.command ] + [ o.datetime ])
		session.close()
		self.render('command.html',title="Exe Command",items = items)
	def post(self):
		WYhosts = self.get_argument("hosts")
		WYcommand = self.get_argument("command")
		Module = self.get_argument("module")
		items = MyAnsible.WyCommand(WYhosts,WYcommand,Module)
		self.write(items)

class AnsiblePlayBook(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		session = db.DBSession()
		List_book = session.query(db.Playbook.bookname).group_by(db.Playbook.bookname).all()
		session.close()
		items = []
		for book in List_book:
			items.append(book.bookname)
		self.render('playbook.html',title="playbook",items = items)
	def post(self):
		if "play" == self.get_argument("action"):
			session = db.DBSession()
			command_list = session.query(db.Playbook).filter(db.Playbook.bookname == self.get_argument("bookname")).order_by("bookpage").all()
			session.close()
			for o in command_list:
				WYhosts = o.hosts
				WYcommand = o.command
				Module = o.module
				json_result = MyAnsible.WyCommand(WYhosts,WYcommand,Module)
				self.write(json_result)
		else:
			if "update" == self.get_argument("action"):
				session = db.DBSession()
				new_bookpage = db.Playbook(pid = self.get_argument("pid"), bookname = self.get_argument("bookname"), bookpage = self.get_argument("bookpage"), hosts = self.get_argument("hosts"), module = self.get_argument("module"), command = self.get_argument("command"))
				session.merge(new_bookpage)
				session.commit()
				session.close()
			if "add" == self.get_argument("action"):
				session = db.DBSession()
				new_bookpage = db.Playbook(bookname = self.get_argument("bookname"), bookpage = self.get_argument("bookpage"), hosts = self.get_argument("hosts"), module = self.get_argument("module"), command = self.get_argument("command"))
				session.add(new_bookpage)
				session.commit()
				session.close()
			if "delete" == self.get_argument("action"):
				session = db.DBSession()
				session.query(db.Playbook).filter(db.Playbook.pid == self.get_argument("pid")).delete()
				session.commit()
				session.close()
			session = db.DBSession()
			command_list = session.query(db.Playbook).filter(db.Playbook.bookname == self.get_argument("bookname")).order_by("bookpage").all()
			session.close()
			items = []
			for o in command_list:
				items.append([o.bookname] + [o.hosts] + [o.module] + [o.command] + [o.bookpage] + [o.pid] )
			self.render('playbook_edit.html',title="edit playbook", items = items )

class testHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("json.html")
	def post(self):
		self.render("json.html")

class ChatHandler(tornado.websocket.WebSocketHandler):
	socket_handlers = set()
	def open(self):
		print "WebSocket opened"
	def on_message(self,message):
		message = message.split(',')
		items = MyAnsible.WyCommand(message[0],message[1],message[2])
		self.write_message(items)
	def on_close(self):
		print "WebSocket closed"
	def ping(self):
		print('ping')
	def check_origin(self, origin):
		return True

class Application(tornado.web.Application):
	def __init__(self):
		base_dir = os.path.dirname(__file__)
		settings = {
			"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
			"login_url": "/login",
			'template_path': os.path.join(base_dir, "templates"),
			'static_path': os.path.join(base_dir, "static"),
			'debug':True,
			"xsrf_cookies": True,
		}

		tornado.web.Application.__init__(self, [
			tornado.web.url(r'/login', LoginHandler, name="login"),
			tornado.web.url(r'/logout', LogoutHandler, name="logout"),
			tornado.web.url(r'/host', HostHandler, name="host"),
			tornado.web.url(r'/ansible', AnsibleHandler, name="ansible"),
			tornado.web.url(r'/ansibleplaybook', AnsiblePlayBook, name="playbook"),
			tornado.web.url(r'/test', testHandler, name="test"),
			tornado.web.url(r'/chat', ChatHandler),
			tornado.web.url(r'/', MainHandler, name="main"),
		], **settings)

def main():
	tornado.options.parse_command_line()
	Application().listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
