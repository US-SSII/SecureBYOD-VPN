import jks
import OpenSSL

ASN1 = OpenSSL.crypto.FILETYPE_ASN1

def jks_file_to_context(key_alias, key_password=None):

    keystore = jks.KeyStore.load('../resources/keystore.jks', 'keystore_password')
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
    ctx.use_privatekey(pkey)
    ctx.use_certificate(public_cert)
    ctx.check_privatekey() # want to know ASAP if there is a problem
    cert_store = ctx.get_cert_store()
    for cert in trusted_certs:
        cert_store.add_cert(cert)

    return ctx

def create_keystore():
    keystore = jks.KeyStore.new('jks', [])
    keystore.save('../resources/keystore.jks', 'keystore_password')


if __name__ == "__main__":
    create_keystore()

