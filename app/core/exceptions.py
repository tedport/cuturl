class URLShortenerError(Exception):
    pass

class SlugTakenError(URLShortenerError):
    pass

class SlugGenerationError(URLShortenerError):
    pass

class LinkNotFoundError(URLShortenerError):
    pass

class LinkExpiredError(URLShortenerError):
    pass

class InvalidURLError(URLShortenerError):
    pass