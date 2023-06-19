#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#import sys
#import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import sys, pathlib, fitz

def PdfToText(file_name):
    with fitz.open(file_name) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
    # write as a binary file to support non-ASCII characters
    pathlib.Path(file_name + ".txt").write_bytes(text.encode())

def PdfToImage(file_name):
    doc = fitz.open(file_name)
    print("Исходный документ", doc)
#    print("\nКоличество страниц: %i\n\n------------------\n\n" % doc.pageCount)
    print(doc.metadata)
    page_count = 0
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
    	    xref = img[0]
    	    pix = fitz.Pixmap(doc, xref)
    	    pix1 = fitz.Pixmap(fitz.csRGB, pix)
    	    page_count += 1
    	    pix1.save("images/picture_number_%s_from_page_%s.png" % (page_count, i+1))
    	    print("Image number ", page_count, " writed...")
    	    pix1 = None
    page = doc[0]
    paths = page.get_drawings()

    # make a new PDF and a new page in it
    outpdf = fitz.open()
    # give new pages same width / height as source page
    outpage = outpdf.new_page(width=page.rect.width, height=page.rect.height)
    shape = outpage.new_shape()  # make a drawing canvas for the output page
    # --------------------------------------
    # loop through the paths and draw them
    # --------------------------------------
    for path in paths:
#        print (path)
        # ------------------------------------
        # draw each entry of the 'items' list
        # ------------------------------------
        for item in path["items"]:  # these are the draw commands
            # treat each of them accordingly ...
            if item[0] == "l":  # line
                shape.draw_line(item[1], item[2])
            elif item[0] == "re":  # rectangle
                shape.draw_rect(item[1])
            elif item[0] == "qu":  # quad
                shape.draw_quad(item[1])
            elif item[0] == "c":  # curve
                shape.draw_bezier(item[1], item[2], item[3], item[4])
            else:
                raise ValueError("unhandled drawing", item) # should not happen
        # ----------------------------------------------------------
        # all items are drawn, now apply the geneal path properties
        # ----------------------------------------------------------
        shape.finish(
            fill=path["fill"],  # fill color
            color=path["color"],  # line color
            dashes=path["dashes"],  # line dashing
            even_odd=path.get("even_odd", True),  # control color of overlaps
            closePath=path["closePath"],  # whether to connect last and first point
            lineJoin=path["lineJoin"],  # how line joins should look like
            lineCap=max(path["lineCap"]),  # how line ends should look like
            width=path["width"],  # line width
            stroke_opacity=path.get("stroke_opacity", 1),  # same value for both
            fill_opacity=path.get("fill_opacity", 1),  # opacity parameters
            )
    # all paths processed - commit the shape to its page
    shape.commit()
    outpdf.save("reproduced-drawings.pdf")

def main():
    PdfToImage("test.pdf")

if __name__ == "__main__":
    main()