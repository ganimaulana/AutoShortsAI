class RetryService:

    def run(
        self,
        fn,
        retries=3,
    ):

        error = None

        for _ in range(retries):

            try:

                return fn()

            except Exception as e:

                error = e

        raise error