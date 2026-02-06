import mimetypes
import os

from django.core.management.base import BaseCommand

from topcomputersapp.models import StoredFile
from topcomputersapp.utils import S3_CLIENT, BUCKET_NAME


class Command(BaseCommand):
    help = "Sync files from Wasabi bucket into StoredFile records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--prefix",
            default="products/",
            help="Bucket prefix to scan (default: products/)",
        )

    def handle(self, *args, **options):
        prefix = options["prefix"]
        created = 0
        updated = 0
        skipped = 0

        continuation_token = None
        while True:
            if continuation_token:
                response = S3_CLIENT.list_objects_v2(
                    Bucket=BUCKET_NAME,
                    Prefix=prefix,
                    ContinuationToken=continuation_token,
                )
            else:
                response = S3_CLIENT.list_objects_v2(
                    Bucket=BUCKET_NAME,
                    Prefix=prefix,
                )

            objects = response.get("Contents", [])
            for obj in objects:
                key = obj.get("Key", "")
                if not key or key.endswith("/"):
                    skipped += 1
                    continue

                filename = key.split("/")[-1]
                title = filename.rsplit(".", 1)[0] if "." in filename else filename

                size_mb = round(obj.get("Size", 0) / (1024 * 1024), 2)
                file_type, _ = mimetypes.guess_type(filename)
                file_type = file_type or "unknown"
                file_extension = os.path.splitext(filename)[1].lower()
                is_image = file_type.startswith("image/")

                instance, was_created = StoredFile.objects.get_or_create(
                    file=filename,
                    defaults={
                        "title": title,
                        "description": "",
                        "file_size_mb": size_mb,
                        "file_type": file_type,
                        "file_extension": file_extension,
                        "is_image": is_image,
                        "likes_count": 0,
                    },
                )

                if was_created:
                    created += 1
                else:
                    fields_changed = False
                    if instance.title != title:
                        instance.title = title
                        fields_changed = True
                    if instance.file_size_mb != size_mb:
                        instance.file_size_mb = size_mb
                        fields_changed = True
                    if instance.file_type != file_type:
                        instance.file_type = file_type
                        fields_changed = True
                    if instance.file_extension != file_extension:
                        instance.file_extension = file_extension
                        fields_changed = True
                    if instance.is_image != is_image:
                        instance.is_image = is_image
                        fields_changed = True

                    if fields_changed:
                        instance.save()
                        updated += 1
                    else:
                        skipped += 1

            if not response.get("IsTruncated"):
                break
            continuation_token = response.get("NextContinuationToken")

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. Created: {created}, Updated: {updated}, Skipped: {skipped}"
            )
        )
