# parallelized version

import os
from itertools import chain
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageSequence


def tiff2png_job(f):
    try:
        with Image.open(str(f)) as img:
            for i, page in enumerate(ImageSequence.Iterator(img)):
                out_fname = str(f.with_name(f.stem + "_" + str(i)).with_suffix(".png"))
                page.save(out_fname)

                # verify image properly written, last try this wasnt necessary at all. consider removing. this increases
                # runtime dramatically
                try:
                    Image.open(Path(out_fname)).load()
                except:
                    print(f"cannot load {out_fname}, consider deleting.")
    except:
        print(f"Failed to load {str(f)}.")


class tiff2png:
    def __init__(self, sources: list):
        self.tif_list = list()
        for source in sources:
            p = Path(source)
            self.tif_list.extend(
                chain(
                    p.glob("**/*.tiff"),
                    p.glob("**/*.TIFF"),
                    p.glob("**/*.tif"),
                    p.glob("**/*.TIF"),
                )
            )

    def run(self):
        pool = Pool(os.cpu_count() - 1)  # leave one :D
        pool.map(tiff2png_job, self.tif_list)


def main():
    sources = list()
    sources.append(".")
    job = tiff2png(sources)
    job.run()


if __name__ == "__main__":
    main()
