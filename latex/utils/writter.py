class Writter:
    def __init__(self):
        self.header = (
            '\\documentclass[pstricks]{standalone}\n'
            '\\usepackage{pst-node}\n'
            '\\usepackage{multido}\n'
            '\\usepackage{xcolor}\n'
            '\\begin{document}\n'
        )
        self.body = ''
        self.footer = '\\end{document}\n'

    def write_body(self, path):
        with open(path, 'w') as output:
            output.write(
                f'{self.header}{self.body}{self.footer}'
            )

    def add_to_body(self, text):
        self.body = f'{self.body}{text}\n'
