from supabase import create_client, Client
import os
from django.core.files.storage import Storage
import uuid
import mimetypes

class SupabaseStorage(Storage):
    def __init__(self):
        self.url = os.environ.get('SUPABASE_URL')  # Ensure your SUPABASE_URL and API_KEY are set in the environment
        self.api_key = os.environ.get('SUPABASE_API_KEY')
        self.bucket = 'the-reader-ebook'
        self.client: Client = create_client(self.url, self.api_key)

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, content_type=None):
        # Check if file already exists before uploading
        if self.exists(name):
            raise Exception(f"File with name {name} already exists.")

        file_data = content.read()
        # Default content_type fallback
        if not content_type:
            content_type, _ = mimetypes.guess_type(name)
            bucket = self.client.storage.from_(self.bucket)
            bucket.upload(name, file_data, {"content-type": content_type})
            return f'{self.url}/storage/v1/object/public/{self.bucket}/{name}'

    def get_url(self, name):
        return f'{self.url}/storage/v1/object/public/{self.bucket}/{name}'

    def exists(self, name):
        # Check if the file exists in the Supabase storage bucket
        bucket = self.client.storage.from_(self.bucket)
        try:
            file = bucket.get(name)
            return file.status_code == 200  # If the file exists, status_code should be 200
        except:
            return False
