import string
import random
import os
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing, Rect, colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import reportlab.lib.colors as colors
import time
from PIL import Image
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import ghostscript

from django.contrib.auth.decorators import user_passes_test


def generate_random_password(size):
    return ''.join(random.SystemRandom().choice(string.hexdigits) for n in xrange(size))


def user_is_professor(function):
    return user_passes_test(lambda x: hasattr(x, "professor"))(function)


def force_encoding(string):
    try:
        return string.encode("Utf-8")
    except UnicodeDecodeError:
        pass

    try:
        return string.decode("Utf-8")
    except UnicodeDecodeError:
        pass

    try:
        return string.encode("latin")
    except UnicodeDecodeError:
        pass

    return string.decode("latin")


def insertion_sort_file(filelist):
    i=0
    j=0
    while i < len(filelist)-1:
        j = i+1
        min = filelist[i]
        ind = i
        while j < len(filelist):
            if min.name > filelist[j].name:
                min = filelist[j]
                ind = j
            j += 1
        (filelist[i], filelist[ind]) = (filelist[ind], filelist[i])
        i += 1

def all_different(l):
    seen = set()
    for i in l:
        if i in seen:
            return False
        seen.add(i)
    return True


PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Mon test"
def generate_pdf(list,id):
    print(list)
    print(id)
    if not os.path.isdir(settings.STATIC_ROOT +"/tests/pdf"):
        os.makedirs(settings.STATIC_ROOT +"/tests/pdf")

    doc = SimpleDocTemplate(settings.STATIC_ROOT+"/tests/pdf/"+str(id)+".pdf")

    Story = [Spacer(1,2*inch)]
    styles = stylesheet()
    global Title

    # Add 10 questions with boxes below
    for i in list:
        if not i[0] in "skills-scan" and not i[0] in "csrfmiddlewaretoken" and not i[0] in "titre":
            tmp = int(i[0])+1
            bogustext = (str(tmp)+". %s" %  i[1])
            p = Paragraph(bogustext, styles['default'])
            # Write the paragraph

            draw = Drawing()
            # rect(x1,y1,width,height)
            rec = Rect(0, 100, 450, 150)
            rec.fillColor = colors.white
            # draw the rect under each paragraph
            draw.add(rec)
            p.keepWithNext = True
            Story.append(p)
            Story.append(draw)
            Story.append(Spacer(1,-0.9 * inch))
        elif i[0] in "titre":
            Title = i[1]
    # build the document by inserting the whole story
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    print(str(id)+".pdf")
    return str(id)+".pdf"


def stylesheet():
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=60,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= colors.black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=colors.purple,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=colors.yellow,
        borderColor=colors.black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles


def myFirstPage(canvas, doc):

    canvas.saveState()
    #url = pyqrcode.create(canvas.getPageNumber())
    #url.png('qr.png', scale=8)

    #canvas.drawInlineImage('qr.png', 45, 760, width=60,height=60)
    canvas.rect(370,760,200,40)
    canvas.setFont('Times-Bold',16)

    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-130,  Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % canvas.getPageNumber())
    canvas.restoreState()

def myLaterPages(canvas, doc):

    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    #url = pyqrcode.create(canvas.getPageNumber())
    #url.png('qr.png', scale=8)

    #canvas.drawInlineImage("qr.png", 530, 0.75*inch, width=45,height=45)
    canvas.drawString(inch, 0.75 * inch, "Page %d " % (doc.page))
    canvas.restoreState()

def generate_coordinates(file):
    # Open a PDF file.
    fp = open(settings.STATIC_ROOT+"/tests/pdf/"+file, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document
    i=0
    content = {}

    for page in PDFPage.create_pages(document):
        i+=1
        content[i] = [[],[]]
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        # extract text from this object
        parse_obj(layout._objs,content[i])

    return content


def parse_obj(lt_objs,content):

    # loop over the object list


    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTRect):
            content[0].append(int(obj.x0))
            content[0].append(int(obj.x1))
            content[1].append(int(obj.y1))
            content[1].append(int(obj.y0))



def pt_to_px(dpi,coord,i=0):


    if i == 0:
        return ((int(coord)*dpi)/72)
    else:
        return ((842*dpi)/72)-((int(coord)*dpi)/72)



def pdf2png(pdf_input_path, png_output_path):
    args = ["pdf2png", # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=png",
            "-r144",
            "-sOutputFile=" + png_output_path,
            pdf_input_path]
    ghostscript.Ghostscript(*args)


