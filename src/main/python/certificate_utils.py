import os
from configparser import ConfigParser

import OpenSSL
from OpenSSL import crypto
import jks
from loguru import logger

# CONSTANTS
ASN1 = OpenSSL.crypto.FILETYPE_ASN1
config = ConfigParser()
current_directory = os.path.dirname(os.path.abspath(__file__))
keystore_password = config.get("KEYSTORE", "password")
keystore_path = os.path.join(current_directory, config.get("KEYSTORE", "path"))


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
    try:
        if not os.path.exists(keystore_path):
            keystore = jks.KeyStore.new("jks", [])
            # keystore.save(keystore_path, keystore_password)
        else:
            keystore = jks.KeyStore.load(keystore_path, keystore_password)
        dumped_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
        dumped_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, key)
        private_key = jks.PrivateKeyEntry.new(alias, [dumped_cert], dumped_key, 'rsa_raw')
        keystore.entries[alias] = private_key

        # Guardar el almacén de claves en el archivo
        keystore.save(keystore_path, keystore_password)
        logger.info(f"Key and certificate with alias '{alias}' saved to keystore successfully.")
    except Exception as e:
        logger.error(f"Error saving key and certificate: {e}")