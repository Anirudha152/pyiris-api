from functools import wraps
import pyiris_api.library.modules.check_loaded_components as check_loaded_components


def run_component_check(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		check_loaded_components.main(self)
		return func(self, *args, **kwargs)
	return wrapper


def reset_bridged(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		self.config.bridged_to = None
		return func(self, *args, **kwargs)
	return wrapper
