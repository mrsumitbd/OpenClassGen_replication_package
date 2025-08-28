class Split(object):
    def __init__(self, allele_file, extension='.fasta', number=True):
        self.allele_file = allele_file
        self.extension = extension if extension.startswith('.') else '.' + extension
        self.number = number
        self.read_split_file()

    def read_split_file(self):
        if os.path.isdir(self.allele_file):
            pattern = os.path.join(self.allele_file, f"*{self.extension}")
            files = glob.glob(pattern)
        elif os.path.isfile(self.allele_file):
            files = [self.allele_file]
        else:
            raise ValueError(f"No such file or directory: {self.allele_file}")

        for filepath in files:
            self._split_file(filepath)

    def _split_file(self, filepath):
        seqs = {}
        header = None
        with open(filepath) as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                if line.startswith('>'):
                    if header:
                        seqs[header] = ''.join(lines)
                    header = line[1:].split()[0]
                    lines = []
                else:
                    lines.append(line)
            if header:
                seqs[header] = ''.join(lines)

        base_dir = os.getcwd()
        idx = 1
        for h, seq in seqs.items():
            safe_h = re.sub(r'[^A-Za-z0-9._-]', '_', h)
            if self.number:
                fname = f"{idx}_{safe_h}{self.extension}"
            else:
                fname = f"{safe_h}{self.extension}"
            out_path = os.path.join(base_dir, fname)
            with open(out_path, 'w') as out:
                out.write(f">{h}\n")
                for i in range(0, len(seq), 60):
                    out.write(seq[i:i+60] + '\n')
            idx += 1