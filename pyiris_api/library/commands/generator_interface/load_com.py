# API
# done
import pyiris_api.library.modules.key_from_val as key_from_val
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def load_com(self, load_on):
	if self.config.scout_values['Windows'][0] == 'True':
		if load_on in list(self.config.win_components.keys()):
			if self.config.win_components[load_on].startswith('windows/bases/') and self.config.win_components[load_on] not in list(self.config.loaded_components.values()):
				self.config.win_base_to_use = self.config.win_components[load_on]
				self.log.pos("Replaced the loaded on base with new base : " + self.config.win_components[load_on])
				return {"status": "ok", "message": "Replaced the loaded on base with new base : " + self.config.win_components[load_on], "data": None}
			else:
				load_on = self.config.win_components[load_on]
		if load_on in list(self.config.loaded_components.values()):
			self.log.war("Component already loaded")
			return {"status": "warning", "message": "Component already loaded", "data": None}
		else:
			id = key_from_val.main(self.config.win_components, load_on)
			if not id:
				raise KeyError
			if load_on.startswith('windows/bases/'):
				self.config.win_base_to_use = load_on
				self.log.pos("Replaced the loaded on base with new base : " + load_on)
				return {"status": "ok", "message": "Replaced the loaded on base with new base : " + load_on, "data": None}
			else:
				self.config.loaded_components[id] = load_on
				self.log.pos("Loaded : " + load_on)
			return {"status": "ok", "message": "Loaded : " + load_on, "data": None}
	else:
		if load_on in list(self.config.lin_components.keys()):
			if self.config.lin_components[load_on].startswith('linux/bases/') and self.config.lin_components[load_on] not in list(self.config.loaded_components.values()):
				self.config.lin_base_to_use = self.config.lin_components[load_on]
				self.log.pos("Replaced the loaded on base with new base : " + self.config.lin_components[load_on])
				return {"status": "ok", "message": "Replaced the loaded on base with new base : " + self.config.lin_components[load_on], "data": None}
			else:
				load_on = self.config.lin_components[load_on]
		if load_on in list(self.config.loaded_components.values()):
			self.log.war("Component already loaded")
			return {"status": "warning", "message": "Component already loaded", "data": None}
		else:
			id = key_from_val.main(self.config.lin_components, load_on)
			if not id:
				raise KeyError
			if load_on.startswith('linux/bases/'):
				self.config.lin_base_to_use = load_on
				self.log.pos("Replaced the loaded on base with new base : " + load_on)
				return {"status": "ok", "message": "Replaced the loaded on base with new base : " + load_on, "data": None}
			self.config.loaded_components[id] = load_on
			self.log.pos("Loaded : " + load_on)
			return {"status": "ok", "message": "Loaded : " + load_on, "data": None}


def main(self, command):
	try:
		load_on = command
		load_on = generator_id_parser.main(self, load_on, 'components', 'load')["data"]
		load_on = list(map(str, load_on))
		for i in load_on:
			self.log.inf('Loading : ' + i)
			load_com(self, str(i))
		return {"status": "ok", "message": "Loaded components successfully", "data": {"loaded_components": self.config.loaded_components}}
	except (KeyError, IndexError):
		self.log.err("Generator found no IDs")
		return {"status": "error", "message": "Generator found no IDs", "data": None}