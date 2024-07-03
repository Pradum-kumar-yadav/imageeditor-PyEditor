import ttkbootstrap as ttk
from tkinter import*
from tkinter import font
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab,ImageEnhance
import numpy as np
import torch
import torchvision.transforms as transforms


root = ttk.Window(themename="cosmo")
root.title("Py-Editor")
root.geometry("1400x880")
icon = ttk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)
 #menu
 
# create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# create a menu
file_menu = Menu(menubar)

# add a menu item to the menu
file_menu.add_command(
    label='Exit',background="red",
    command=root.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)

# defining global variables
WIDTH = 1200
HEIGHT = 950
file_path = ""
pen_size = 3
pen_color = "black"
root.iconphoto(False, icon)
# the left frame to contain buttons
left_frame = ttk.Frame(root, width=200, height=800)
left_frame.pack(side="left", fill="y")

# canvas for displaying the image
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# label for qoutes
label=font.Font(weight="bold",size="15")
filter_label = ttk.Label(left_frame, text="\"SAVE YOUR MEMORIES\n AS YOU WANT\"",
                         font=label,foreground="black",  background="aqua")
filter_label.pack(padx=0, pady=2)

# label
filter_label = ttk.Label(left_frame, text="Choose Option:", font=label,background="yellow")
filter_label.pack(padx=0, pady=2)

#list of filters
image_filters = ["Sketch", "Black and White",  "yellow-filter","blue-filter","pink-filter","Blur",
                 "Detail","Invert-color", "Emboss", "Edge Enhance", "Sharpen", "Smooth","contrast",
                 "vibrance","brightness","Border-15","Border-30","Border-45","Border-60","color1","color2","color3"]

# combobox for filters
filter_combobox = ttk.Combobox(left_frame, values=image_filters, width=15)
filter_combobox.pack(padx=10, pady=5)

# loading the icons for  buttons
image_icon = ttk.PhotoImage(file = 'add.png').subsample(12, 12)
flip_icon = ttk.PhotoImage(file = 'flip.png').subsample(12, 12)
rotate_icon = ttk.PhotoImage(file = 'rotate.png').subsample(12, 12)
color_icon = ttk.PhotoImage(file = 'color.png').subsample(12, 12)
erase_icon = ttk.PhotoImage(file = 'erase.png').subsample(12, 12)
save_icon = ttk.PhotoImage(file = 'saved.png').subsample(12, 12)
 


# function to open the image file
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        global image, photo_image
        image = Image.open(file_path)
        new_width = int((WIDTH))
        image = image.resize((new_width, HEIGHT), Image.LANCZOS)
            
        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)

#global variable for checking the flip state 
is_flipped = False

def flip_image():
    try:
        global image, photo_image, is_flipped
        if not is_flipped:
            # open the image and flip it left and right
            image = Image.open(file_path).transpose(Image.FLIP_LEFT_RIGHT)
            is_flipped = True
        else:
            # reset the image to its original state
            image = Image.open(file_path)
            is_flipped = False
        # resize the image to fit the canvas
        new_width = int((WIDTH))
        image = image.resize((new_width, HEIGHT), Image.LANCZOS)
        #PIL Tkinter PhotoImage display it on the canvas
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)

    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')

#global variable for rotation angle
rotation_angle = 0

#defaultimage 
image=Image.open("iconic1.png")

new_width = int((WIDTH))

image = image.resize((new_width, HEIGHT), Image.LANCZOS)
        #PIL Tkinter PhotoImage display it on the canvas
photo_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=photo_image)

# function for rotating the image
def rotate_image():
    try:
        global image, photo_image, rotation_angle
        # open the image and rotate it
        
        image = Image.open(file_path)
        new_width = int((WIDTH))
        image = image.resize((new_width, HEIGHT), Image.LANCZOS)
        rotated_image = image.rotate(rotation_angle + 90)
        rotation_angle += 90
        # reset image if angle is a multiple of 360 degrees
        if rotation_angle % 360 == 0:
            rotation_angle = 0
            image = Image.open(file_path)
            image = image.resize((new_width, HEIGHT), Image.LANCZOS)
            rotated_image = image
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(rotated_image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)
    # catches errors
    except:
        showerror(title='Rotate Image Error', message='Please select an image to rotate!')

# function for applying filters to the opened image file
def apply_filter(filter):
    global image, photo_image
    try:
        # check if the image has been flipped or rotated
        if is_flipped:
            # flip the original image left and right
            flipped_image = Image.open(file_path).transpose(Image.FLIP_LEFT_RIGHT)
            # rotate the flipped image
            rotated_image = flipped_image.rotate(rotation_angle)
            # apply the filter to the rotated image
            if filter == "Black and White":
                rotated_image = ImageOps.grayscale(rotated_image)
            elif filter == "Blur":
                rotated_image = rotated_image.filter(ImageFilter.GaussianBlur(10))
            elif filter == "Sketch":
                rotated_image = rotated_image.filter(ImageFilter.CONTOUR)
            elif filter == "Detail":
                rotated_image = rotated_image.filter(ImageFilter.DETAIL)
            elif filter == "Emboss":
                rotated_image = rotated_image.filter(ImageFilter.EMBOSS)
            elif filter == "Edge Enhance":
                rotated_image = rotated_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Sharpen":
                rotated_image = rotated_image.filter(ImageFilter.SHARPEN)
            elif filter == "Smooth":
                rotated_image = rotated_image.filter(ImageFilter.SMOOTH)
            elif filter =="contrast":
                rotated_image =rotated_image.filter(ImageFilter.UnsharpMask(10))
            elif filter == "vibrance":
                rotated_image=ImageEnhance.Color(rotated_image).enhance(3)
            elif filter == "brightness":
                rotated_image = ImageEnhance.Brightness(rotated_image).enhance(1.3)
            elif filter == "Border-15":
                rotated_image = ImageOps.expand( rotated_image,border=15,fill="black")
            elif filter == "Border-30":
                 rotated_image = ImageOps.expand( rotated_image,border=30,fill="black")
            elif filter == "Border-45":
                 rotated_image = ImageOps.expand( rotated_image,border=45,fill="black")
            elif filter == "Border-60":
                 rotated_image = ImageOps.expand( rotated_image,border=60,fill="black")
            elif filter == "color1":
                transform=transforms.ColorJitter(brightness=(0.5,1.5),contrast=(1), saturation=(0.5,1.5), hue=(-0.1,0.1))
                rotated_image=transform( rotated_image)
            elif filter == "color2":
                transform=transforms.ColorJitter(brightness=(1.0),contrast=(0.5), saturation=(1), hue=(0.1))
                rotated_image=transform( rotated_image)
            elif filter=="Invert-color":
                rotated_image= Image.open(file_path).convert('RGB')
                rotated_image = ImageOps.invert(rotated_image)
            elif filter=="yellow-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array(rotated_image, np.uint8)
                img_arr[::, ::, 2]=0
                rotated_image=Image.fromarray(img_arr)
            elif filter=="blue-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array( rotated_image, np.uint8)
                img_arr[::, ::, 0]=0
                rotated_image=Image.fromarray(img_arr)
            elif filter=="pink-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array( rotated_image, np.uint8)
                img_arr[::, ::, 1]=0
                rotated_image=Image.fromarray(img_arr)

                
            elif filter == "color3":
                transform=transforms.ColorJitter(brightness=(0.1),contrast=(0.5), saturation=(0.1), hue=(0.1))
                rotated_image=transform( rotated_image)
            
            else:
                rotated_image = Image.open(file_path).transpose(Image.FLIP_LEFT_RIGHT).rotate(rotation_angle)
        elif rotation_angle != 0:
            # rotate the original image
            rotated_image = Image.open(file_path).rotate(rotation_angle)
            # apply the filter to the rotated image
            if filter == "Black and White":
                rotated_image = ImageOps.grayscale(rotated_image)
            elif filter == "Blur":
                rotated_image = rotated_image.filter(ImageFilter.GaussianBlur(10))
            elif filter == "Sketch":
                rotated_image = rotated_image.filter(ImageFilter.CONTOUR)
            elif filter == "Detail":
                rotated_image = rotated_image.filter(ImageFilter.DETAIL)
            elif filter == "Emboss":
                rotated_image = rotated_image.filter(ImageFilter.EMBOSS)
            elif filter == "Edge Enhance":
                rotated_image = rotated_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Sharpen":
                rotated_image = rotated_image.filter(ImageFilter.SHARPEN)
            elif filter == "Smooth":
                rotated_image = rotated_image.filter(ImageFilter.SMOOTH)
            elif filter =="contrast":
                rotated_image =rotated_image.filter(ImageFilter.UnsharpMask(10))
            elif filter == "vibrance":
                rotated_image=ImageEnhance.Color(rotated_image).enhance(3)
            elif filter == "brightness":
                rotated_image = ImageEnhance.Brightness(rotated_image).enhance(1.3)
            elif filter == "Border-15":
                rotated_image = ImageOps.expand( rotated_image,border=15,fill="black")
            elif filter == "Border-30":
                 rotated_image = ImageOps.expand( rotated_image,border=30,fill="black")
            elif filter == "Border-45":
                 rotated_image = ImageOps.expand( rotated_image,border=45,fill="black")
            elif filter == "Border-60":
                 rotated_image = ImageOps.expand( rotated_image,border=60,fill="black")
            elif filter == "color1":
                transform=transforms.ColorJitter(brightness=(0.5,1.5),contrast=(1), saturation=(0.5,1.5), hue=(-0.1,0.1))
                rotated_image=transform( rotated_image)
            elif filter == "color2":
                transform=transforms.ColorJitter(brightness=(1.0),contrast=(0.5), saturation=(1), hue=(0.1))
                rotated_image=transform( rotated_image)
            elif filter=="Invert-color":
                rotated_image = Image.open(file_path).convert('RGB')
                rotated_image = ImageOps.invert(rotated_image)
            elif filter == "color3":
                transform=transforms.ColorJitter(brightness=(0.1),contrast=(0.5), saturation=(0.1), hue=(0.1))
                rotated_image=transform( rotated_image)
            elif filter=="yellow-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array(rotated_image, np.uint8)
                img_arr[::, ::, 2]=0
                rotated_image=Image.fromarray(img_arr)
            elif filter=="blue-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array( rotated_image, np.uint8)
                img_arr[::, ::, 0]=0
                rotated_image=Image.fromarray(img_arr)
            elif filter=="pink-filter":
                rotated_image = Image.open(file_path)
                img_arr=np.array( rotated_image, np.uint8)
                img_arr[::, ::, 1]=0
                rotated_image=Image.fromarray(img_arr)
            else:
                rotated_image = Image.open(file_path).rotate(rotation_angle)
        else:
            # apply the filter to the original image/
            image = Image.open(file_path)
            if filter == "Black and White":
                image = ImageOps.grayscale(image)
            elif filter == "Blur":
                image = image.filter(ImageFilter.GaussianBlur(10))
            elif filter == "Sharpen":
                image = image.filter(ImageFilter.SHARPEN)
            elif filter == "Smooth":
                image = image.filter(ImageFilter.SMOOTH)
            elif filter == "Emboss":
                image = image.filter(ImageFilter.EMBOSS)
            elif filter == "Detail":
                image = image.filter(ImageFilter.DETAIL)
            elif filter =="contrast":
                image =image.filter(ImageFilter.UnsharpMask(10))
            elif filter == "vibrance":
                image=ImageEnhance.Color(image).enhance(3)
            elif filter == "brightness":
                image = ImageEnhance.Brightness(image).enhance(1.3)
            elif filter == "Border-15":
                image = ImageOps.expand(image,border=15,fill="black")
            elif filter == "Border-30":
                image = ImageOps.expand(image,border=30,fill="black")
            elif filter == "Border-45":
                image = ImageOps.expand(image,border=45,fill="black")
            elif filter == "Border-60":
                image = ImageOps.expand(image,border=60,fill="black")
            elif filter == "color1":
                transform=transforms.ColorJitter(brightness=(0.5,1.5),contrast=(1), saturation=(0.5,1.5), hue=(-0.1,0.1))
                image=transform(image)
            elif filter == "color2":
                transform=transforms.ColorJitter(brightness=(0.5),contrast=(0.9), saturation=(0.1), hue=(0.1))
                image=transform(image)
            elif filter=="Invert-color":
                image = Image.open(file_path).convert('RGB')
                image = ImageOps.invert(image)
            elif filter == "color3":
                transform=transforms.ColorJitter(brightness=(0.1),contrast=(0.5), saturation=(0.1), hue=(0.1))
                image=transform(image)
          
            elif filter=="yellow-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 2]=0
                image=Image.fromarray(img_arr)
            elif filter=="blue-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 0]=0
                image=Image.fromarray(img_arr)
            elif filter=="pink-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 1]=0
                image=Image.fromarray(img_arr)
        
                
              
                  
               
            elif filter == "Edge Enhance":
                image = image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Sketch":
                image = image.filter(ImageFilter.CONTOUR)
            rotated_image = image
        # resize the rotated/flipped image to fit the canvas
        new_width = int((WIDTH))
        rotated_image = rotated_image.resize((new_width, HEIGHT), Image.LANCZOS)
        # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(rotated_image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)
    except:
        showerror(title='Error', message='Please select an image first!')

# function for changing the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# function for erasing lines on the opened image
def erase_lines():
    global file_path
    if file_path:
        canvas.delete("oval")
 
# the function for saving an image
def save_image():
    global file_path, is_flipped, rotation_angle
    if file_path:
        # create a new PIL Image object from the canvas
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        # check if the image has been flipped or rotated
        if is_flipped or rotation_angle % 360 != 0:
            # Resize and rotate the image
            new_width = int((WIDTH))
            image = image.resize((new_width, HEIGHT), Image.LANCZOS)
            if is_flipped:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            if rotation_angle % 360 != 0:
                image = image.rotate(rotation_angle)
            # update the file path to include the modifications in the file name
            file_path = file_path.split(".")[0] + "_mod.jpg"
        # apply any filters to the image before saving
        filter = filter_combobox.get()
        if filter:
            if filter == "Black and White":
                image = ImageOps.grayscale(image)
            elif filter == "Blur":
                image = image.filter(ImageFilter.GaussianBlur(10))
            elif filter == "Sharpen":
                image = image.filter(ImageFilter.SHARPEN)
            elif filter == "Smooth":
                image = image.filter(ImageFilter.SMOOTH)
            elif filter =="contrast":
                image =image.filter(ImageFilter.UnsharpMask(10))
            elif filter == "vibrance":
                image=ImageEnhance.Color(image).enhance(3)
            elif filter == "brightness":
                image = ImageEnhance.Brightness(image).enhance(1.3)
            elif filter == "Border-15":
                image = ImageOps.expand(image,border=15,fill="black")
            elif filter == "Border-30":
                image = ImageOps.expand(image,border=30,fill="black")
            elif filter == "Border-45":
                image = ImageOps.expand(image,border=45,fill="black")
            elif filter == "Border-60":
                image = ImageOps.expand(image,border=60,fill="black")
            elif filter == "color1":
                transform=transforms.ColorJitter(brightness=(0.5,1.5),contrast=(1), saturation=(0.5,1.5), hue=(-0.1,0.1))
                image=transform(image)
            elif filter == "color2":
                transform=transforms.ColorJitter(brightness=(1.0),contrast=(0.5), saturation=(1), hue=(0.1))
                image=transform(image)
            elif filter == "color3":
                transform=transforms.ColorJitter(brightness=(0.1),contrast=(0.5), saturation=(0.1), hue=(0.1))
                image=transform(image)
            elif filter=="Invert-color":
                image = Image.open(file_path).convert('RGB')
                image = ImageOps.invert(image)
            elif filter=="yellow-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 2]=0
                image=Image.fromarray(img_arr)
            elif filter=="blue-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 0]=0
                image=Image.fromarray(img_arr)
            elif filter=="pink-filter":
                image = Image.open(file_path)
                img_arr=np.array(image, np.uint8)
                img_arr[::, ::, 1]=0
                image=Image.fromarray(img_arr)
            
            elif filter == "Emboss":
                image = image.filter(ImageFilter.EMBOSS)
            elif filter == "Detail":
                image = image.filter(ImageFilter.DETAIL)
            elif filter == "Edge Enhance":
                image = image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Sketch":
                image = image.filter(ImageFilter.CONTOUR)
            # update the file path to include the filter in the file name
            file_path = file_path.split(".")[0] + "_" + filter.lower().replace(" ", "_") + ".jpg"
        # open file dialog to select save location and file type
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                # save the image to a file
                image.save(file_path)

#windowdistroy
def close():
    root.destroy()

 
 
     
 
# button for adding/opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="white", command=open_image)
image_button.pack(pady=5)
filter_label = ttk.Label(left_frame, text="ADD IMAGE", font=label,background="white")
filter_label.pack(padx=0, pady=0)
 

# button for flipping the image file
flip_button = ttk.Button(left_frame, image=flip_icon, bootstyle="white", command=flip_image)
flip_button.pack(pady=5)
filter_label = ttk.Label(left_frame, text="FLIP IMAGE",font=label, background="white")
filter_label.pack(padx=3, pady=0)

# button for rotating the image file
rotate_button = ttk.Button(left_frame, image=rotate_icon, bootstyle="white", command=rotate_image)
rotate_button.pack(pady=5)
filter_label = ttk.Label(left_frame, text="ROTATE IMAGE", font=label,background="white")
filter_label.pack(padx=3, pady=0)

# button for choosing pen color
color_button = ttk.Button(left_frame, image=color_icon, bootstyle="white", command=change_color)
color_button.pack(pady=5)
filter_label = ttk.Label(left_frame, text="CHOOSE COLOR",font=label, background="white")
filter_label.pack(padx=3, pady=0)

# button for erasing the lines drawn over the image file
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="white",command=erase_lines)
erase_button.pack(pady=5)
filter_label = ttk.Label(left_frame, text="ERASE ", font=label,background="white")
filter_label.pack(padx=3, pady=0)

# button for saving the image file
save_button = ttk.Button(left_frame, image=save_icon, bootstyle="white", command=save_image)
save_button.pack(pady=5)
filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))
filter_label = ttk.Label(left_frame, text="SAVE IMAGE",font=label, background="white")
filter_label.pack(padx=3, pady=0)


 
 #closebutttooon
Close = ttk.Button(left_frame, text='Close', command=close)
Close.pack(padx=3, pady=0)
filter_label = ttk.Label(left_frame, text="CLOSE WINDOW",font=label, background="white", foreground="red")
filter_label.pack(padx=3, pady=0)
 
# function for drawing lines on the opened image
def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")
# binding the Canvas to the B1-Motion event
canvas.bind("<B1-Motion>", draw)
print("done")
 
root.mainloop()


