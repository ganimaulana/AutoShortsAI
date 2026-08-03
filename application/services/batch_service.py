class BatchService:

    def split(
        self,
        items,
        batch_size,
    ):

        for i in range(
            0,
            len(items),
            batch_size,
        ):

            yield items[
                i:i + batch_size
            ]