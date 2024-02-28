#
# AlphaZero
#
# This code is open-source. Feel free to modify and redistribute as you want.
#
# a python e-typewriter using eink and a USB keyboard
# this program outputs directly to the SPI eink screen, and is driven by a
# raspberry pi zero (or any pi).  it handles keyboard input directly via keyboard library.
#
# Code build for Waveshare 7in5_V2
#

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
from os import listdir
from os.path import isfile, join
from pathlib import Path


class alphaZero:
    """
    A class to build and send emails

    ...

    Attributes
    ----------
    to : list
        a list of strings for the email addresses to send to


    Methods
    -------
    add_message(email, content, tag='p')
        Adds the string to the email, by default it will wrap it in paragraph tags, but you can specify the tag

    """ 
    def __init__(self ):
        """
        Width is 800
        Height is 480
        Parameters
        ----------
        to : list
            Who recieves the email

        """
        self.epd = epd7in5_V2.EPD()
        self.epd.init_fast()
        
        self.font = self.change_font(font='Font.ttc', size=22)
        
        self.xStart = 10
        self.yStart = 30
        self.xPosition = self.xStart
        self.yPosition = self.yStart
        self.lineheight = self.get_text_dimensions('test', self.change_font(font='Font.ttc', size=28))[1] + 10
        self.row = ""
        self.lines = []
        
        self.document_name = ""
        self.open_document("test.txt")
        self.currentFile = "test.txt"
    
    
    def open_document(self, filename):
        self.fresh_screen()
        #self.epd.init_fast()
        with open("/home/alphazero/alphazero/documents/" + filename, "r") as file:
            self.document = file.read().replace('\n', '')
        self.update_display(self.document[-270:]) # 270
        self.epd.init_part()
    
    def save_document(self):
        with open("/home/alphazero/alphazero/documents/" + self.currentFile, "w") as file:
            file.write(self.document)
            
    def new_document(self):
        self.document = ""
        self.row = ""
        self.lines = []
        self.xPosition = self.xStart
        self.yPosition = self.yStart
        self.fresh_screen()
        #self.epd.init_fast()
        self.epd.init_part()
            
    def update_document(self, text):
        self.document += text
        self.update_display(text)
        
    def get_documents(self):
        # list available documents and return
        files = [f for f in listdir("/home/alphazero/alphazero/documents") if isfile(join("/home/alphazero/alphazero/documents", f))]
        self.xPosition = self.xStart
        self.yPosition = self.yStart
        self.fresh_screen()
        #self.epd.init_fast()
        self.draw.line((20, 30, 780, 30), fill = 0)
        self.draw.line((780, 30, 780, 460), fill = 0)
        self.draw.line((20, 30, 20, 460), fill = 0)
        self.draw.line((20, 460, 780, 460), fill = 0)      
        
        self.draw.text((0, 0), "Input a corresponding letter to open file.", font = self.font, fill = 0)
        xp = 30
        yp = 30
        i = 1
        for file in files:
            self.draw.text((xp, yp), chr(ord('`')+i)+": "+file, font = self.font, fill = 0)
            i += 1
            if i == 26:
                break
            yp += self.lineheight
            if yp+self.lineheight >= 430:
                xp = 370
                yp = 30
        self.update_screen()   
        return files
        
    
    def process_backspace(self):
        self.document = self.document[:-1]
        self.row = self.row[:-1]
        # if we deleted the last character on display, display earlier text, or do nothing
        if not self.row and not self.lines:
            if self.document:
                if len(self.document) >= 270:
                    self.update_display(self.document[-270:])
                else:
                    self.update_display(self.document)
        # if we deleted the end of a line
        elif not self.row:
            self.draw.rectangle((self.xStart, self.yPosition, 790, self.yPosition+self.lineheight), fill = 255)
            self.lines = self.lines[:-1]
            self.row = self.lines[-1]
            self.yPosition -= self.lineheight
        # else just remove the single character
        else:
            self.draw.rectangle((self.xStart, self.yPosition, 790, self.yPosition+self.lineheight), fill = 255)
            self.draw.text((self.xStart, self.yPosition), self.row, font = self.font, fill = 0)
        self.xPosition = self.xStart + self.get_text_dimensions(self.row, self.font)[0]
        self.update_screen()
    
    def update_display(self, row_text):
        self.draw_display(row_text)
        
    def draw_display(self, row_text):
        # Check if the line does NOT have room to display the current text queue
        if (self.xPosition + self.get_text_dimensions(row_text, self.font)[0]) >= 780: 
            self.draw_looper(row_text)
        # else if the current line has room for the text queue, then just display it
        else:  
            # Display new text in the current line and update the x position
            self.draw.text((self.xPosition, self.yPosition), row_text, font = self.font, fill = 0)
            self.xPosition += self.get_text_dimensions(row_text, self.font)[0]
            self.row += row_text
        self.update_screen()
            
    def draw_looper(self, row_text):
        # compensate for the first character being a space, since the split function will turn that into a NoneType for the first row and annoy me in the for loop
        if row_text[:1] == " ":
            line = " "
            row_text = row_text[1:]
        else:
            line = ""
        res = row_text.split(" ") 
        # Loop through words
        for i in range(len(res)):
            # check if the new word fits in the row
            if self.get_text_dimensions(line+res[i], self.font)[0] < 780 - self.xPosition:
                # add a space if we still have more words.
                if i == len(res):
                    line += res[i]
                else:
                    line += res[i] + " "
                # lets check if we are the last word, if so, then print to the page.
                if(i+1 == len(res)):
                    #self.check_y_space()
                    self.draw.text((self.xPosition, self.yPosition), line, font=self.font, fill=0)
                    self.lines.append(line)
                    self.row = line
                    self.xPosition = self.get_text_dimensions(self.row, self.font)[0] + self.xStart
            # new word doesn't fit in the row, lets print the row now
            else:
                self.check_y_space() 
                self.draw.text((self.xPosition, self.yPosition), line, font=self.font, fill=0)
                self.lines.append(line)
                self.yPosition += self.lineheight
                self.xPosition = self.xStart
                self.row = line
                if i == len(res):
                    line = res[i]
                else:
                    line = res[i] + " "
    def check_y_space(self):
        if self.lineheight + self.yPosition > 460:
            self.xPosition = self.xStart
            self.yPosition = self.yStart
            self.fresh_screen()
    
    def update_screen(self):
        self.epd.display_Partial(self.epd.getbuffer(self.base_image),0, 0, self.epd.width, self.epd.height)
    
    def fresh_screen(self):
        self.base_image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw = ImageDraw.Draw(self.base_image)
        self.epd.display(self.epd.getbuffer(self.base_image))
        self.epd.init_fast()
    
    def get_text_dimensions(self, text_string, font):
       # if text_string.isspace():
       #     text_string = "n" 
        ascent, descent = font.getmetrics()
        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent
        return (text_width, text_height)

    def change_font(self, font='Font.ttc', size=22):
        """Sets/changes the default font used for the display

        I have defaults set for them to simplify a few things, but it probably should only be used without parameters on intialization.  
        
        TODO: Change initialization to check a file for the saved default font and size

        Parameters
        ----------
        font : str
            The font type
        size : int
            The font size

        """
        return ImageFont.truetype('/home/alphazero/alphazero/fonts/'+font, size)
        
    def sleep(self):
        self.epd.init()
        Himage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        sleep_image = Image.open('/home/alphazero/alphazero/bg1.jpg')
        self.epd.display(self.epd.getbuffer(sleep_image))
        self.epd.sleep()
    
    
