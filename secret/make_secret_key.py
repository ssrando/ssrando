import secrets

print(f'(0x{secrets.token_hex(8)}-(0x{secrets.token_hex(8)}+0x{secrets.token_hex(8)})/0x{secrets.token_hex(8)})')