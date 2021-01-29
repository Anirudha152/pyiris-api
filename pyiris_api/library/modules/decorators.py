from functools import wraps
import pyiris_api.library.modules.generator_append as generator_append


def run_generator_append(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		generator_append.main(self)
		return func(self, *args, **kwargs)
	return wrapper


def reset_bridged(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		self.config.bridged_to = None
		return func(self, *args, **kwargs)
	return wrapper
