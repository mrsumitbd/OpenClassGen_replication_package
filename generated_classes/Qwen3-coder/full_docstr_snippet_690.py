class ImportExportCertificate(object):
    '''
    Mixin to provide certificate import and export methods to relevant
    classes.
    '''

    def import_certificate(self, certificate):
        '''
        Import a valid certificate. Certificate can be either a file path
        or a string of the certificate. If string certificate, it must include
        the -----BEGIN CERTIFICATE----- string.
        
        :param str certificate_file: fully qualified path to certificate file
        :raises CertificateImportError: failure to import cert with reason
        :raises IOError: file not found, permissions, etc.
        :return: None
        '''
        if certificate is None:
            raise CertificateImportError("Certificate cannot be None")
            
        # Check if certificate is a file path
        if '\n' not in certificate and '\r' not in certificate:
            # Treat as file path
            try:
                with open(certificate, 'r') as f:
                    cert_data = f.read()
            except IOError:
                raise
            except Exception as e:
                raise CertificateImportError("Failed to read certificate file: {}".format(str(e)))
        else:
            # Treat as certificate string
            cert_data = certificate
            
        # Validate certificate format
        if "-----BEGIN CERTIFICATE-----" not in cert_data:
            raise CertificateImportError("Invalid certificate format: missing BEGIN CERTIFICATE header")
            
        if "-----END CERTIFICATE-----" not in cert_data:
            raise CertificateImportError("Invalid certificate format: missing END CERTIFICATE footer")
            
        # Store the certificate data (assuming the class has a certificate attribute)
        self._certificate = cert_data

    def export_certificate(self, filename=None):
        '''
        Export the certificate. Returned certificate will be in string
        format. If filename is provided, the certificate will also be saved
        to the file specified.
        
        :raises CertificateExportError: error exporting certificate
        :rtype: str or None
        '''
        if not hasattr(self, '_certificate') or self._certificate is None:
            raise CertificateExportError("No certificate available to export")
            
        cert_data = self._certificate
        
        if filename is not None:
            try:
                with open(filename, 'w') as f:
                    f.write(cert_data)
            except IOError:
                raise
            except Exception as e:
                raise CertificateExportError("Failed to write certificate to file: {}".format(str(e)))
                
        return cert_data