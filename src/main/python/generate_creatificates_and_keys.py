from OpenSSL import crypto


def generate_key_pair():
    # Generar un nuevo par de claves RSA de 2048 bits
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    return key


def generate_certificate(key, common_name):
    # Crear un certificado
    cert = crypto.X509()
    cert.get_subject().CN = common_name
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Un año de validez
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    return cert


def save_key_and_certificate(key, cert, key_filename, cert_filename):
    # Guardar la clave privada
    with open(key_filename, 'wb') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    # Guardar el certificado
    with open(cert_filename, 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))


# Generar claves y certificados para el servidor
if __name__ == "__main__":
    server_key = generate_key_pair()
    server_cert = generate_certificate(server_key, "server.example.com")
    save_key_and_certificate(server_key, server_cert, "server.key", "server.crt")

    # Generar claves y certificados para el cliente
    client_key = generate_key_pair()
    client_cert = generate_certificate(client_key, "client.example.com")
    save_key_and_certificate(client_key, client_cert, "client.key", "client.crt")
