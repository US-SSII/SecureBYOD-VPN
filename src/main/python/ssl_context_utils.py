import os
from configparser import ConfigParser

import jks
import OpenSSL

# CONSTANTS
ASN1 = OpenSSL.crypto.FILETYPE_ASN1
config = ConfigParser()
config.read("config.ini")
current_directory = os.path.dirname(os.path.abspath(__file__))
keystore_password = config.get("KEYSTORE", "password")
keystore_path = os.path.join(current_directory, config.get("KEYSTORE", "path"))

def jks_file_to_context(key_alias, key_password=None):
    keystore = jks.KeyStore.load(keystore_path, keystore_password)
    pk_entry = keystore.private_keys[key_alias]

    # if the key could not be decrypted using the store password,
    # decrypt with a custom password now
    if not pk_entry.is_decrypted():
        pk_entry.decrypt(key_password)

    pkey = OpenSSL.crypto.load_privatekey(ASN1, pk_entry.pkey)
    public_cert = OpenSSL.crypto.load_certificate(ASN1, pk_entry.cert_chain[0][1])
    trusted_certs = [OpenSSL.crypto.load_certificate(ASN1, cert.cert)
                     for alias, cert in keystore.certs]

    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
    cipher_suite = "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384"
    ctx.set_cipher_list(cipher_suite)
    ctx.use_privatekey(pkey)
    ctx.use_certificate(public_cert)
    ctx.check_privatekey() # want to know ASAP if there is a problem
    cert_store = ctx.get_cert_store()
    for cert in trusted_certs:
        cert_store.add_cert(cert)

    return ctx

