import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel, showinfo, WARNING

import os.path
import re



class TextAnalyzer:
    def __init__(self,main) -> None:

        # initializing some of the attributes
        main.title('Text Analyzer')
        main.configure(background = '#F0FFFF')
        
        #empty containers for our analysis result
        self.wordCount = 0
        self.charCount = 0
        self.blankCount = 0
        self.wordDict = dict ()
        self.active = True
        self.path = ""
        self.root = main

        #setting a canvas and grid system
        self.canvas = tk.Canvas(self.root, width=700, height=100, bg="#F0FFFF")
        self.canvas.grid(columnspan=3)

        #defining App Label and position
        self.instruction = tk.Label(self.root, text= 'Welcome! Kindly Select a Text File for Analysis')
        self.instruction.grid(column=1, row=0)

        # Browse buttons 
        self.browse_text = tk.StringVar()
        self.browse_btn = tk.Button(self.root, textvariable=self.browse_text, command=lambda:self.browse() )
        self.browse_text.set("Browse")
        self.browse_btn.grid(column=0, row=0)

        # Process Button 
        tk.Button(self.root, text='Process', command=lambda:self.Process()).grid(column=0 , row=1)

        
        # save file button 
        self.save_text = tk.StringVar()
        self.save_btn = tk.Button(self.root, textvariable=self.save_text, command=lambda:self.save_file())
        self.save_text.set("Save File")
        self.save_btn.grid(column=1, row=2)

        #Exit button 
        self.exit_text = tk.StringVar()
        self.exit_btn = tk.Button(self.root, textvariable=self.exit_text, command=lambda:self.exit_app())
        self.exit_text.set('Exit')
        self.exit_btn.grid(column=2, row=2)

        # entry box
        self.EntryText = tk.StringVar()
        self.entry_box = tk.Entry(self.root, textvariable=self.EntryText, width = 70, font = ('Arial', 10))
        self.entry_box.grid(column=1, row=1)


    
    # the browse function
    def browse (self):
        self.browse_text.set('loading')
        self.path = askopenfilename(filetypes=[("Text File", '*.txt')])
        self.EntryText.set(self.path)
        self.active = True
        self.saving = True

        #preview the text file to be sure its user content
        if self.path:
            with open(self.path, 'r') as content:
                text_box = tk.Text(self.root, height=10, width=20, padx=15, pady=15)
                text_box.insert(1.0, content.read())
                text_box.grid(column=1, row=3)
            self.browse_text.set('Browse')

    # the proess function
    def Process(self):

        # open file and analyse
        with open(self.path, 'r') as myFile:

            # loop through each of the lines 
            for text in myFile:
                text = text.strip()
                text = re.sub('[^A-Za-z0-9\s]+', '', text)

                #covert to lowercase and split to get individual words
                text = text.lower()
                words = text.split(" ")

                #store the number of words and characters in their container defined with self
                self.wordCount += len(words)
                self.charCount += len(text)

                # count the number of blank spaces and its percentage
                self.blankCount += text.count(" ")
                self.percentCount = (self.blankCount/self.charCount)*100

                # checking for word frequencies
                for word in words: 
                    if word in self.wordDict:
                        self.wordDict[word] += 1
                    else: 
                        self.wordDict[word] = 1

                
            self.active = False
            myFile.close()
            messagebox.showinfo(title= 'Congratulations', message='File Processed! Kindly SaveFile')


    # save file function
    def save_file (self):
        self.fileName = os.path.basename(self.path)
        self.fileName = self.fileName.split('.')[0]
            
        # defining the output file format
        self.outputFileName = self.fileName + "-" + "TextAnalyzed.txt"


        if (self.active == False and self.path != ""):

            output = {
                 'The name of the file is :': str(self.fileName),
                 'Total number of Words is :' : str(self.wordCount),
                 'Total number of charactersis :' : str(self.charCount),
                 'Total number of Blanks is :' : str(self.blankCount),
                 'Total percentage of Blank is :': str(self.percentCount)
             }


            #write in the analysis to thr output file
            with open (self.outputFileName, "w") as self.outputFile:
                for key in output.keys():
                    self.outputFile.write(str(key) + str(output[key]))
                    self.outputFile.write("\n") 

                #looping into the word dictionary to output each word and occurance
                for keys in list(self.wordDict.keys()):
                    self.outputFile.write("\n" + str(keys) + ":" + str(self.wordDict[keys]))
                messagebox.showinfo('Analysis', 'Completed.\nFile saved to: "' + os.path.abspath(self.outputFileName) + '"') 

        # else, if file is empty, prompt an error message
        elif (self.path == ""): 
            messagebox.showinfo(title = 'Error!', message = 'No file selected')
        else:
            messagebox.showinfo(title = 'Error!', message = 'Processing Incomplete')
            
        #setting variables back to default to allow user to process another file
        self.outputFile.close()
        self.saving = False
        self.wordDict = dict ()
        self.wordCount = 0
        self.charCount = 0
        self.blankCount = 0
        self.percentCount =0
        

    
     #exit application
    def exit_app(self):
        if self.active == True:
            answer = askokcancel(title='INFO', message='File Not Processed!!... Do you want to Quit?', icon=WARNING)
            if answer:
                self.root.destroy()

        elif self.active == False:
            report = askokcancel(title='Cool', message='You can now exit')
            self.root.destroy()
        




def main():
    root = tk.Tk()
    textanalyzer = TextAnalyzer(root)
    root.mainloop()

if __name__ == '__main__': main()