import pyiris_api.library.modules.config as config


def main(self, **kwargs):
	config.init_constants()
	self.config = config
	for key, value in kwargs.items():
		setattr(self.config, key, value)
	config.init_variables(self)
