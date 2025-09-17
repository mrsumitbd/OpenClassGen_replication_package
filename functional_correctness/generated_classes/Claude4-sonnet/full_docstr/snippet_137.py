class ScriptExecutor(object):
    '''A class for executing user provided metadata scripts.'''

    def __init__(self, logger, script_type, default_shell=None):
        '''Constructor.

        Args:
          logger: logger object, used to write to SysLog and serial port.
          script_type: string, the type of the script we are running.
          default_shell: string, the default shell to execute the script.
        '''
        self.logger = logger
        self.script_type = script_type
        self.default_shell = default_shell

    def _MakeExecutable(self, metadata_script):
        '''Add executable permissions to a file.

        Args:
          metadata_script: string, the path to the executable file.
        '''
        current_permissions = os.stat(metadata_script).st_mode
        os.chmod(metadata_script, current_permissions | stat.S_IEXEC)

    def _RunScript(self, metadata_key, metadata_script):
        '''Run a script and log the streamed script output.

        Args:
          metadata_key: string, the key specifing the metadata script.
          metadata_script: string, the file location of an executable script.
        '''
        self.logger.info('Running %s script found in metadata.', self.script_type)
        
        try:
            self._MakeExecutable(metadata_script)
            
            if self.default_shell:
                cmd = [self.default_shell, metadata_script]
            else:
                cmd = [metadata_script]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in iter(process.stdout.readline, ''):
                self.logger.info(line.rstrip())
            
            process.wait()
            
            if process.returncode != 0:
                self.logger.warning('%s script %s failed with return code %d',
                                  self.script_type, metadata_key, process.returncode)
            else:
                self.logger.info('%s script %s completed successfully',
                               self.script_type, metadata_key)
                
        except Exception as e:
            self.logger.error('Error running %s script %s: %s',
                            self.script_type, metadata_key, str(e))

    def RunScripts(self, script_dict):
        '''Run the metadata scripts; execute a URL script first if one is provided.

        Args:
          script_dict: a dictionary mapping metadata keys to script files.
        '''
        if not script_dict:
            return
        
        # Execute URL script first if present
        if 'startup-script-url' in script_dict:
            self._RunScript('startup-script-url', script_dict['startup-script-url'])
            
        # Execute other scripts
        for metadata_key, script_file in script_dict.items():
            if metadata_key != 'startup-script-url':
                self._RunScript(metadata_key, script_file)