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
        cert_str = None
        # Determine if input is a cert string
        if isinstance(certificate, str) and '-----BEGIN CERTIFICATE-----' in certificate:
            cert_str = certificate
        else:
            # Treat as file path
            try:
                with open(certificate, 'r') as f:
                    cert_str = f.read()
            except IOError:
                raise
        if not cert_str or '-----BEGIN CERTIFICATE-----' not in cert_str:
            raise CertificateImportError("Invalid certificate format")
        self._certificate = cert_str

    def export_certificate(self, filename=None):
        '''
        Export the certificate. Returned certificate will be in string
        format. If filename is provided, the certificate will also be saved
        to the file specified.
        
        :raises CertificateExportError: error exporting certificate
        :rtype: str or None
        '''
        cert = getattr(self, '_certificate', None)
        if not cert:
            raise CertificateExportError("No certificate to export")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(cert)
            except IOError as e:
                raise CertificateExportError(f"Failed to write to {filename}: {e}")
            return None
        return cert