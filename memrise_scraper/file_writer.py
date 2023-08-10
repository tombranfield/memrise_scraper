"""file_writer.py"""


class FileWriter:
    """Responsible for saving the wordpairs to a file"""
    def __init__(self, word_pairs, separator, output_filename):
        self.word_pairs = word_pairs
        self.separator = separator
        self.output_filename = output_filename

    def write_to_file(self):
        """Writes the word pairs to the file"""
        with open(self.output_filename, "w", encoding="utf-8") as out_file:
            for pair in self.word_pairs:
                line = pair[0] + self.separator + pair[1] + "\n"
                out_file.write(line)
