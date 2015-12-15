

# The default config for apps - keep in mind that you can't even run this
# with the local.sh testing script until you
class DefaultConfig(object):
    # Default values that you should Probably override (unlike below which
    # you MUST)
    DEBUG = True
    TEST_EMAIL = 'no-one-cares@gmail.com'

    # IMPORTANT: the below properties should be overridden in a config file
    # which is identified by the env var GLUTEN_CONFIG_FILE.
    FLASK_SECRET = 'SUPPLY THIS IN A .config FILE'
    GOOGLE_OAUTH_CLIENT_ID = 'SUPPLY THIS IN A .config FILE'
    GOOGLE_OAUTH_CLIENT_SECRET = 'SUPPLY THIS IN A .config FILE'

    # These are config values that you shouldn't need to change unless you
    # really know what you're doing
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB for a single upload
    OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
    OAUTHLIB_INSECURE_TRANSPORT = '1'  # TODO: fix with https in prod

# Env variables that we would like to be added to the sys environment
env_populate = [
    'OAUTHLIB_RELAX_TOKEN_SCOPE',
    'OAUTHLIB_INSECURE_TRANSPORT'
]
