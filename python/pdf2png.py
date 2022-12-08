# parallelized version

import io
import os
from itertools import chain
from multiprocessing import Pool
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image, ImageSequence


def pdf2png_job(f):
    try:
        pdf_pages = convert_from_path(f)
        temp = io.BytesIO()
        pdf_pages[0].save(
            temp, save_all=True, append_images=pdf_pages[1:], format="TIFF"
        )
        temp.seek(0)
        pil_img = Image.open(temp)
        for i, page in enumerate(ImageSequence.Iterator(pil_img)):
            out_fname = str(f.with_name(f.stem + "_" + str(i)).with_suffix(".png"))
            page.save(out_fname)

            # verify image properly written, last try this wasnt necessary at all. consider removing. this increases
            # runtime dramatically
            try:
                Image.open(Path(out_fname)).load()
            except:
                print(f"cannot load {out_fname}, consider deleting.")
    except Exception as e:
        print(f"Failed to load {str(f)}. {e=}")


class pdf2png:
    def __init__(self, sources: list):
        self.pdf_list = list()
        for source in sources:
            p = Path(source)
            self.pdf_list.extend(chain(p.glob("**/*.PDF"), p.glob("**/*.pdf")))

    def run(self):
        pool = Pool(os.cpu_count() - 1)  # leave one :D
        pool.map(pdf2png_job, self.pdf_list)


def main():
    sources = list()
    sources.append(".")
    job = pdf2png(sources)
    job.run()


if __name__ == "__main__":
    main()
