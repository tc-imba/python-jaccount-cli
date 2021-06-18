"""
Adapted from https://github.com/aypro-droid/image-to-ascii

MIT License

Copyright (c) 2021 Not Aypro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

try:
    import Image as Image
except ImportError:
    import PIL
    from PIL import Image as Image

from collections import Counter


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


class ImageToAscii:
    def __init__(self, imagePath: str = None, width: int = 100, outputFile: str = None):
        """
        path - The path/name of the image ex: <image_name.png>\n
        width - The width you want the Ascii art to have\n
        outputfile - If you want to store the Ascii art in a txt file then set it to <file_name.txt> else keep it None
        """
        self.path = imagePath
        self.width = width
        try:
            self.image = PIL.Image.open(self.path)
            width, height = self.image.size
            totalPixels = width * height
        except:
            if imagePath is None:
                print("Invalid path name")
            elif self.width is None:
                print("Invalid Width provided")
        self.new_image_data = self.pixelsToAscii(
            self.converToGrayscale(self.resizeImage(self.image))
        )

        self.pixel_count = len(self.new_image_data)

        self.ascii_image = "\n".join(
            [
                self.new_image_data[index : (index + self.width)]
                for index in range(0, self.pixel_count, self.width)
            ]
        )
        if outputFile is not None:
            with open(outputFile, "w") as f:
                f.write(self.ascii_image)

    def resizeImage(self, image):
        width, height = image.size
        ratio = height / width
        new_height = int(self.width * ratio)
        resized_image = image.resize((self.width, new_height))

        return resized_image

    def converToGrayscale(self, image):
        grayscale_image = image.convert("L")
        return grayscale_image

    def pixelsToAscii(self, image):
        pixels = image.getdata()
        characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
        return characters

    def clean(self):
        def count(s, total):
            c = Counter(s)
            _blank = c.get(".", 0) + c.get(",", 0)
            _others = total - _blank
            return _blank, _others

        result = []
        for line in self.ascii_image.split("\n"):
            blank, others = count(line.strip(), self.width)
            if others > self.width / 40.0:
                result.append(line)
        height = len(result)
        start = 0
        end = self.width
        masks = [True] * self.width
        for i in range(0, self.width):
            blank, others = count([result[j][i] for j in range(height)], height)
            if others > 0:
                end = i + 1
                for j in range(start + 2, end - 2):
                    masks[j] = False
                start = i + 1
        end = self.width
        for j in range(start + 2, end - 2):
            masks[j] = False

        new_result = []
        for line in result:
            new_line = ""
            for i in range(self.width):
                if masks[i]:
                    if line[i] == "." or line[i] == ",":
                        new_line += " "
                    else:
                        new_line += line[i]
            new_result.append(new_line)

        return "\n".join(new_result)
