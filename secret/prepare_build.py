import os

# patch the secret key into ssrando.py
secret_key = os.environ['SSR_SECRET_KEY']

with open('ssrando.py','r+') as f:
    data = f.read()
    data = data.replace('self.rng.seed(self.seed+0x123456)', f'self.rng.seed(self.seed+{secret_key})')
    f.truncate(0)
    f.seek(0)
    f.write(data)