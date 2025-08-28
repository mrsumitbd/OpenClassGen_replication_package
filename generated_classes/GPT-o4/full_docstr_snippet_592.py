class Compiler:
    '''Wrapper of execution of CoffeeScript compiler script'''

    def __init__(self, compiler_script, runtime):
        '''compiler_script is a CoffeeScript compiler script in JavaScript.
           runtime is a instance of execjs.Runtime.
        '''
        self.compiler_script = compiler_script
        self.runtime = runtime
        self._context = self.runtime.compile(self.compiler_script)

    def compile(self, script, bare=False):
        '''compile a CoffeeScript code to a JavaScript code.

           if bare is True, then compile the JavaScript without the top-level
           function safety wrapper (like the coffee command).
        '''
        return self._context.call('CoffeeScript.compile', script, {'bare': bare})

    def compile_file(self, filename, encoding="utf-8", bare=False):
        '''compile a CoffeeScript script file to a JavaScript code.

           filename can be a list or tuple of filenames,
           then contents of files are concatenated with line feeds.

           if bare is True, then compile the JavaScript without the top-level
           function safety wrapper (like the coffee command).
        '''
        if isinstance(filename, (list, tuple)):
            parts = []
            for fn in filename:
                with open(fn, 'r', encoding=encoding) as f:
                    parts.append(f.read())
            source = "\n".join(parts)
        else:
            with open(filename, 'r', encoding=encoding) as f:
                source = f.read()
        return self.compile(source, bare=bare)