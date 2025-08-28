class Split(object):
    
    def __init__(self, allele_file, extension='.fasta', number=True):
        self.allele_file = allele_file
        self.extension = extension
        self.number = number
        self.sequences = {}
        
    def read_split_file(self):
        try:
            with open(self.allele_file, 'r') as file:
                current_header = None
                current_sequence = []
                
                for line in file:
                    line = line.strip()
                    if line.startswith('>'):
                        if current_header is not None:
                            self.sequences[current_header] = ''.join(current_sequence)
                        current_header = line[1:]
                        current_sequence = []
                    else:
                        current_sequence.append(line)
                
                if current_header is not None:
                    self.sequences[current_header] = ''.join(current_sequence)
                    
            if self.number:
                for i, (header, sequence) in enumerate(self.sequences.items(), 1):
                    filename = f"{header.split()[0]}_{i}{self.extension}"
                    with open(filename, 'w') as output_file:
                        output_file.write(f">{header}\n{sequence}\n")
            else:
                for header, sequence in self.sequences.items():
                    filename = f"{header.split()[0]}{self.extension}"
                    with open(filename, 'w') as output_file:
                        output_file.write(f">{header}\n{sequence}\n")
                        
        except FileNotFoundError:
            print(f"Error: File '{self.allele_file}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")