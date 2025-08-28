class ImportExportCertificate(object):
    '''
    Mixin to provide certificate import and export methods to relevant
    classes.
    '''

    def __init__(self):
        self._certificate = None

    def import_certificate(self, certificate):
        '''
        Import a valid certificate. Certificate can be either a file path
        or a string of the certificate. If string certificate, it must include
        the -----BEGIN CERTIFICATE----- string.
        
        :param str certificate: fully qualified path to certificate file or certificate string
        :raises CertificateImportError: failure to import cert with reason
        :raises IOError: file not found, permissions, etc.
        :return: None
        '''
        try:
            if '-----BEGIN CERTIFICATE-----' in certificate:
                # Certificate is provided as string
                cert_data = certificate.encode('utf-8')
            else:
                # Certificate is provided as file path
                if not os.path.exists(certificate):
                    raise IOError(f"Certificate file not found: {certificate}")
                
                with open(certificate, 'rb') as cert_file:
                    cert_data = cert_file.read()
            
            # Parse the certificate
            self._certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
            
        except IOError:
            raise
        except Exception as e:
            raise CertificateImportError(f"Failed to import certificate: {str(e)}")

    def export_certificate(self, filename=None):
        '''
        Export the certificate. Returned certificate will be in string
        format. If filename is provided, the certificate will also be saved
        to the file specified.
        
        :raises CertificateExportError: error exporting certificate
        :rtype: str or None
        '''
        try:
            if self._certificate is None:
                raise CertificateExportError("No certificate available to export")
            
            # Convert certificate to PEM format string
            cert_pem = self._certificate.public_bytes(x509.Encoding.PEM)
            cert_string = cert_pem.decode('utf-8')
            
            if filename:
                with open(filename, 'w') as cert_file:
                    cert_file.write(cert_string)
                return None
            else:
                return cert_string
                
        except Exception as e:
            raise CertificateExportError(f"Failed to export certificate: {str(e)}")