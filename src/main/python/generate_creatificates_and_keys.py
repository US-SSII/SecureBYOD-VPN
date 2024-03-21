import OpenSSL
from OpenSSL import crypto
import jks


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


def save_key_and_certificate_with_alias(key, cert, alias):
    # Guardar la clave privada
    keystore_filename = "../resources/keystore.jks"
    keystore_password = "keystore_password"
    try:
        try:
            keystore = jks.KeyStore.load(keystore_filename, keystore_password)
        except jks.BadKeystoreError:
            keystore = jks.KeyStore.new("jks", [])

        dumped_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
        dumped_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, key)
        private_key = jks.PrivateKeyEntry.new(alias, [dumped_cert], dumped_key, 'rsa_raw')
        keystore.entries[alias] = private_key

        # Guardar el almacén de claves en el archivo
        keystore.save(keystore_filename, keystore_password)
        print(f"Key and certificate with alias '{alias}' saved to keystore successfully.")
    except Exception as e:
        print(f"Error saving key and certificate: {e}")


# Generar claves y certificados para el servidor
if __name__ == "__main__":
    server_key = generate_key_pair()
    server_cert = generate_certificate(server_key, "server.example.com")
    save_key_and_certificate_with_alias(server_key, server_cert, "server_alias")

    # Generar claves y certificados para el cliente
    client_key = generate_key_pair()
    client_cert = generate_certificate(client_key, "client.example.com")
    save_key_and_certificate_with_alias(client_key, client_cert, "client_alias")
