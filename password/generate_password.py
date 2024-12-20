import string
import secrets

# Caracteres seguros para generar contraseñas
CHARS = string.ascii_letters
NUMBERS = string.digits

for _ in range(10):
    PASSWORD = ''
    # Generar contraseña aleatoria de 6 caracteres
    for _ in range(3):
        PASSWORD += ''.join(secrets.choice(CHARS)) + ''.join(secrets.choice(NUMBERS))

    PASS_UPPER = PASSWORD.upper()

    print(PASS_UPPER)
