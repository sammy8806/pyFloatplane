import time
import logging

from PyFloatplane.config import VALIDITY_PERIOD

log = logging.getLogger('Floatplane.Cache')

_cache = {}
_cache_time = {}

def normalize_key(key, *args, **kwargs):
	log.debug("Key: {}".format(key))
	log.debug("Args: {}".format(args))
	log.debug("KwArgs: {}".format(kwargs))

	arg_str = ['']
	for it in args:
		it_str = '_'.join(map(str,it))
		log.debug('>> {}'.format(it_str))
		arg_str.append(it_str)

	for key, value in kwargs:
		arg_str.append('{}={}'.format(key, value))

	cache_key = (key +
		'#' + '_'.join(arg_str)
	)

	log.debug("CacheKey: {}".format(cache_key))

	return cache_key

def memorize(key):
	def _decorating_wrapper(func):
		def _caching_wrapper(*args, **kwargs):
			cache_key = normalize_key(key, args, kwargs)
			now = time.time()

			log.debug('Cache: {}'.format(key))

			# if cached and still valid -> use it
			if _cache_time.get(cache_key, now) > now:
				log.debug('Cache still valid')
				return _cache[cache_key]

			log.debug('Cache invalid ... running function')
			ret = func(*args, **kwargs)

			_cache[cache_key] = ret
			_cache_time[cache_key] = now + VALIDITY_PERIOD

			log.debug('Cache: Saving value until {}'.format(_cache_time[cache_key]))
			return ret
		return _caching_wrapper
	return _decorating_wrapper
