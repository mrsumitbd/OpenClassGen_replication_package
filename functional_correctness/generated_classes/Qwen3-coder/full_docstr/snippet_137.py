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
        self.default_shell = default_shell or '/bin/bash'

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
        self._MakeExecutable(metadata_script)
        
        try:
            process = subprocess.Popen(
                [self.default_shell, metadata_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Stream output line by line
            for line in process.stdout:
                line = line.rstrip('\n')
                self.logger.info(f'{self.script_type} {metadata_key}: {line}')
            
            process.wait()
            
            if process.returncode != 0:
                self.logger.error(
                    f'{self.script_type} {metadata_key} failed with return code {process.returncode}'
                )
            else:
                self.logger.info(f'{self.script_type} {metadata_key} succeeded')
                
        except Exception as e:
            self.logger.error(f'Error running {self.script_type} {metadata_key}: {str(e)}')

    def RunScripts(self, script_dict):
        '''Run the metadata scripts; execute a URL script first if one is provided.

        Args:
          script_dict: a dictionary mapping metadata keys to script files.
        '''
        if not script_dict:
            return

        # Check if any script is a URL (starts with http)
        url_scripts = {}
        file_scripts = {}
        
        for key, script in script_dict.items():
            if script.startswith(('http://', 'https://')):
                url_scripts[key] = script
            else:
                file_scripts[key] = script

        # Execute URL scripts first
        for key, url in url_scripts.items():
            try:
                # Download the script to a temporary file
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as temp_file:
                    temp_filename = temp_file.name
                    with urllib.request.urlopen(url) as response:
                        script_content = response.read().decode('utf-8')
                        temp_file.write(script_content)
                
                # Run the downloaded script
                self._RunScript(key, temp_filename)
                
                # Clean up the temporary file
                os.unlink(temp_filename)
                
            except Exception as e:
                self.logger.error(f'Error downloading/executing URL script {key}: {str(e)}')

        # Execute file scripts
        for key, script_file in file_scripts.items():
            if os.path.exists(script_file):
                self._RunScript(key, script_file)
            else:
                self.logger.error(f'Script file {script_file} does not exist for key {key}')