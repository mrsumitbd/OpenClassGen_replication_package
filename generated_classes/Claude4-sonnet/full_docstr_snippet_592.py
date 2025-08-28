class Compiler:
    '''Wrapper of execution of CoffeeScript compiler script'''

    def __init__(self, compiler_script, runtime):
        '''compiler_script is a CoffeeScript compiler script in JavaScript.
        runtime is a instance of execjs.Runtime.
        '''
        self.runtime = runtime
        self.context = runtime.compile(compiler_script)

    def compile(self, script, bare=False):
        '''compile a CoffeeScript code to a JavaScript code.

        if bare is True, then compile the JavaScript without the top-level
        function safety wrapper (like the coffee command).
        '''
        options = {'bare': bare}
        return self.context.call('CoffeeScript.compile', script, options)

    def compile_file(self, filename, encoding="utf-8", bare=False):
        '''compile a CoffeeScript script file to a JavaScript code.

        filename can be a list or tuple of filenames,
        then contents of files are concatenated with line feeds.

        if bare is True, then compile the JavaScript without the top-level
        function safety wrapper (like the coffee command).
        '''
        if isinstance(filename, (list, tuple)):
            contents = []
            for fname in filename:
                with open(fname, 'r', encoding=encoding) as f:
                    contents.append(f.read())
            script = '\n'.join(contents)
        else:
            with open(filename, 'r', encoding=encoding) as f:
                script = f.read()
        
        return self.compile(script, bare=bare)