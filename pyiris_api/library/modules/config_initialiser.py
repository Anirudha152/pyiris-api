import pyiris_api.library.modules.config as config

config.main()

def main(self, **kwargs):
	self.config = config
	for key, value in kwargs.items():
		setattr(self.config, key, value)
