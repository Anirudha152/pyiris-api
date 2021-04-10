# API
# done
import pyiris_api.library.modules.key_from_val as key_from_val
import pyiris_api.library.modules.generator_id_parser as generator_id_parser
import pyiris_api.library.modules.check_loaded_components as check_loaded_components


def load_com(self, load_on):
	if self.config.scout_values['Windows'][0] == 'True':
		if load_on in list(self.config.win_components.keys()):
			load_on = self.config.win_components[load_on]
		if load_on in list(self.config.loaded_components.values()):
			self.log.war("Component already loaded")
			return {"status": "warning", "message": "Component already loaded", "data": None}
		else:
			id = key_from_val.main(self.config.win_components, load_on)
			if not id:
				raise KeyError
			self.config.loaded_components[id] = load_on
			self.log.pos("Loaded : " + load_on)
			return {"status": "ok", "message": "Loaded : " + load_on, "data": None}
	else:
		if load_on in list(self.config.lin_components.keys()):
			load_on = self.config.lin_components[load_on]
		if load_on in list(self.config.loaded_components.values()):
			self.log.war("Component already loaded")
			return {"status": "warning", "message": "Component already loaded", "data": None}
		else:
			id = key_from_val.main(self.config.lin_components, load_on)
			if not id:
				raise KeyError
			self.config.loaded_components[id] = load_on
			self.log.pos("Loaded : " + load_on)
			return {"status": "ok", "message": "Loaded : " + load_on, "data": None}


def main(self, command):
	try:
		load_on = generator_id_parser.main(self, command, 'components', 'load')["data"]
		load_on = list(map(str, load_on))
		for i in load_on:
			self.log.inf('Loading : ' + i)
			load_com(self, str(i))
		check_loaded_components.main(self)
		return {"status": "ok", "message": "Loaded components successfully", "data": {"loaded_components": self.config.loaded_components}}
	except (KeyError, IndexError):
		self.log.err("Generator found no IDs")
		return {"status": "error", "message": "Generator found no IDs", "data": None}