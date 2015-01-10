import zope.interface

from letsencrypt.client import errors
from letsencrypt.client import interfaces
from letsencrypt.client import recovery_token

class ClientAuthenticator(object):
    """Authenticator for CONFIG.CLIENT_CHALLENGES.

    :ivar rec_token: Performs "recoveryToken" challenges
    :type rec_token: :class:`letsencrypt.client.recovery_token.RecoveryToken`

    """
    zope.interface.implements(interfaces.IAuthenticator)

    # This will have an installer soon for get_key/cert purposes
    def __init__(self, server):
        """Initialize Client Authenticator.

        :param str server: ACME CA Server

        """
        self.rec_token = recovery_token.RecoveryToken(server)

    def get_chall_pref(self, domain):  # pylint: disable=no-member-use
        """Return list of challenge preferences."""
        return ["recoveryToken"]

    def perform(self, chall_list):
        """Perform client specific challenges."""
        responses = []
        for chall in chall_list:
            if isinstance(chall, challenge_util.RecTokenChall):
                responses.append(self.rec_token.perform(chall))
            else:
                raise errors.LetsEncryptClientAuthError("Unexpected Challenge")
        return responses

    def cleanup(self, chall_list):
        for chall in chall_list:
            if isinstance(chall, challenge_util.RecTokenChall):
                self.rec_token.cleanup(chall)
            else:
                raise errors.LetsEncryptClientAuthError("Unexpected Challenge")
