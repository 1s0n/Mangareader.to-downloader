import os
import fitz  # pip install --upgrade pip; pip install --upgrade pymupdf
from tqdm import tqdm # pip install tqdm

workdir = "/"

files = os.listdir("temppdfs")
doc = fitz.Document("test1.pdf")

for i in tqdm(range(len(doc)), desc="pages"):
    for img in tqdm(doc.get_page_images(i), desc="page_images"):
        xref = img[0]
        image = doc.extract_image(xref)
        pix = fitz.Pixmap(doc, xref)
        pix.save("%s_p%s-%s.png")
                
print("Done!")