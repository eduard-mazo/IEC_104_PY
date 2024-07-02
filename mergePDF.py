from glob import glob
from PyPDF2 import PdfMerger



def pdf_merge():
    ''' Merges all the pdf files in current directory '''
    merger = PdfMerger()
    allpdfs = [a for a in glob("*.pdf")]
    [merger.append(pdf) for pdf in allpdfs]
    with open("Merged_pdfs.pdf", "wb") as new_file:
        merger.write(new_file)


if __name__ == "__main__":
    pdf_merge()