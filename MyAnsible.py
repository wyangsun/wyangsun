import db
import time
import os.path
#import tornado.websocket
import ansible.runner

def EditAnsibleHost():
	session = db.DBSession()
	List_group = session.query(db.Hostinfo.groupname).group_by('groupname').all()
	ansiblehosts = open('/etc/ansible/hosts','w')
	for g in List_group:
		ansiblehosts.write("[" + g.groupname + "]\n")
		List_lan = session.query(db.Hostinfo.lan_ip).filter(db.Hostinfo.groupname == g.groupname).all()
		for l in List_lan:
			ansiblehosts.write(l.lan_ip+"\n")
	session.close()
	ansiblehosts.close()

def WyCommand(WYhosts,WYcommand,Module):
	results = ansible.runner.Runner(
			pattern=WYhosts,forks=10,
			remote_user='sa',
			sudo=True,
			sudo_user='root',
			module_name=Module, module_args=WYcommand
			).run()
	session = db.DBSession()
	new_hosts = db.Commandhistory(hosts=WYhosts,module=Module,command=WYcommand,datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	session.add(new_hosts)
	session.commit()
	session.close()
	return results

CMDsession = WyCommand

#class ChatHandler(tornado.websocket.WebSocketHandler):
#	socket_handlers = set()
#	def open(self):
#		print "WebSocket opened"
#	def on_message(self,message):
#		print(message)
#		self.write_message(self.CMDsession)
#	def on_close(self):
#		print "WebSocket closed"
#	def ping(self):
#		print('ping')
#	def check_origin(self, origin):
#		return True
