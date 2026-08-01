"""
==================================================
Cancelable Pipeline Token
==================================================
"""

class CancelToken:

    def __init__(self):

        self._cancelled = False

    # ---------------------------------------------

    def cancel(self):

        self._cancelled = True

    # ---------------------------------------------

    @property
    def cancelled(self):

        return self._cancelled