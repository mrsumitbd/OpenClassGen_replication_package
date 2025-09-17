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
        try:
            st = os.stat(metadata_script)
            os.chmod(metadata_script, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            self.logger.info(
                'ScriptExecutor(%s): Made %s executable',
                self.script_type, metadata_script)
        except Exception as e:
            self.logger.error(
                'ScriptExecutor(%s): Failed to make %s executable: %s',
                self.script_type, metadata_script, e)

    def _RunScript(self, metadata_key, metadata_script):
        '''Run a script and log the streamed script output.

        Args:
          metadata_key: string, the key specifying the metadata script.
          metadata_script: string, the file location of an executable script.
        '''
        cmd = [metadata_script]
        if self.default_shell:
            cmd = [self.default_shell, metadata_script]
        self.logger.info(
            'ScriptExecutor(%s): Running script %s (%s)',
            self.script_type, metadata_key, metadata_script)
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True)
            for line in proc.stdout:
                self.logger.info(
                    'ScriptExecutor(%s)[%s]: %s',
                    self.script_type, metadata_key, line.rstrip('\n'))
            proc.wait()
            if proc.returncode != 0:
                self.logger.error(
                    'ScriptExecutor(%s): Script %s exited with code %d',
                    self.script_type, metadata_key, proc.returncode)
            else:
                self.logger.info(
                    'ScriptExecutor(%s): Script %s completed successfully',
                    self.script_type, metadata_key)
        except Exception as e:
            self.logger.error(
                'ScriptExecutor(%s): Error running script %s: %s',
                self.script_type, metadata_key, e)

    def RunScripts(self, script_dict):
        '''Run the metadata scripts; execute a URL script first if one is provided.

        Args:
          script_dict: a dictionary mapping metadata keys to script files.
        '''
        # Identify URL scripts first
        url_keys = [k for k in script_dict if k.lower().endswith('-url')]
        other_keys = [k for k in script_dict if k not in url_keys]
        # Run URL scripts first
        for key in url_keys + other_keys:
            script_path = script_dict.get(key)
            if not script_path:
                continue
            if not os.path.exists(script_path):
                self.logger.error(
                    'ScriptExecutor(%s): Script file for %s not found: %s',
                    self.script_type, key, script_path)
                continue
            self._MakeExecutable(script_path)
            self._RunScript(key, script_path)