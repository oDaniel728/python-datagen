from datagen.extras.entities._util.hasproperties import HasProperties


class BucketableEntities[T: HasProperties]():
    def with_from_bucket(self: T, from_bucket: bool) -> T:
        """
        Whether or not the entity was spawned from a bucket.
        If true, the entity will not despawn naturally and will not drop any experience upon death.
        """
        self.properties["FromBucket"] = int(from_bucket)
        return self