from tkinter import *
from tkinter import ttk
import math as mt
import csv
from tkinter import filedialog

root = Tk()
root.title('On-demand paging simulator')
root.geometry("1000x800")
root.resizable(False,False)

speed = 810
anim_speed = 5
anim_speed2 = 5
true_speed = 20
file_name = None

def select_file():
    global file_name

    filetypes = (
        ('CSV Files', '*.csv'),
    )


    filename = filedialog.askopenfilename(
        title='Select the csv file with the instructions',
        initialdir='./',
        filetypes=filetypes
    )

    file_name = filename
    l = None
    for widget in root.winfo_children():
        if widget.winfo_name() == '!label7':
            l = widget
    l['text'] = f'selected route: {file_name}'

def incrementarVI():
    global speed
    if speed > 10:
        speed -= 100
    # print(speed)

def disminuirVI():
    global speed
    if speed < 1310:
        speed += 100
    # print(speed)

def incrementarAN():
    global true_speed
    if true_speed < 50:
        true_speed += 5
    # print(true_speed)

def disminuirAN():
    global true_speed
    if true_speed > 10:
        true_speed -= 5
    # print(true_speed)

def print_tablapag(tabla_pagina):
    i = 0
    s = 'Page table\n\n'
    s+='i | m | bv | bs |\n'
    for row in tabla_pagina:
        s+= f'{i} | {row[0] if row[0] != None else "-"} | {row[1]}  | {row[2]}  |\n'
        i+=1
    return s

def move(button, buttondest, content):
    root.update()
    content.update()
    x = button.winfo_x()
    y = button.winfo_y()

    xd = buttondest.winfo_x()
    yd = buttondest.winfo_y()
    # print(x, y, xd, yd)

    sp_x = true_speed if x < xd else -true_speed
    sp_y = true_speed if y < yd else -true_speed

    if x != xd or y != yd:

        x += sp_x
        y += sp_y

        if sp_x < 0:
            if x < xd:
                x = xd
        else:
            if x > xd:
                x = xd
        
        if sp_y < 0:
            if y < yd:
                y = yd
        else:
            if y > yd:
                y = yd

        button.place(x=x, y=y, relx=0, rely=0, bordermode='outside')

def start_iterations(tam_Frame, so, proc, Frames, Frames_so, instructions):
    clear()
    global anim_speed
    replacements = 0
    fallos = 0
    content = ttk.Frame(root, padding=40)

    
    
    paginas_proc = list(range(mt.ceil(proc/tam_Frame)))
    tabla_pagina = [[None, 0, 0] for pagina in paginas_proc]
    picola = []

    memoria = Frames_so + Frames
    pady=10
    # pady2=70/len(memoria)

    labelinstruccion = ttk.Label(content, text=" ", font=('Helvetica', 12))
    firstlbl = ttk.Label(content, text="Process Pages")
    tabla = ttk.Label(content, text=print_tablapag(tabla_pagina), font=('Helvetica', 14))
    framemedio = ttk.Frame(content, width=600, height=30, relief="ridge")
    secondlbl = ttk.Label(content, text="Frames in Main Memory")
    bitacora = ttk.Label(content, text="", font=('Helvetica', 12))

    labelsPaginas = [ttk.Label(content, text=f'{pagina*tam_Frame}-{(pagina*tam_Frame + (tam_Frame-1))}') for pagina in paginas_proc]
    labelsMP = [ttk.Label(content, text=f'{Frame*tam_Frame}-{(Frame*tam_Frame + (tam_Frame-1))}') for Frame in memoria]
    labelsDirLogica = [ttk.Label(content, text='         ') for Frame in memoria]

    bs = [Button(content, text=f'Page {pagina}', width=10, pady=pady, bg='white') for pagina in paginas_proc]
    ms = [Button(content, text=f'Frame {Frame}', width=10, pady=pady, bg='yellow') if Frame in Frames_so else Button(content, text=f'Frame {Frame}', width=10, pady=pady, bg='white') for Frame in memoria]

    incrementarVIbt = Button(content, text=f'+ Process speed', width=20, pady=pady, bg='#082032', fg='#DDDDDD', command=incrementarVI)
    incrementarANbt = Button(content, text=f'+ Speed ​​Animations', width=20, pady=pady, bg='#082032',fg='#DDDDDD', command=incrementarAN)
    disminuirVIbt = Button(content, text=f'- Process speed', width=20, pady=pady, bg='#FF4C29', command=disminuirVI)
    disminuirANbt = Button(content, text=f'- Speed ​​Animations', width=20, pady=pady, bg='#FF4C29', command=disminuirAN)

    framebt1 = ttk.Frame(content, width=80, height=25)
    framebt2 = ttk.Frame(content, width=80, height=25)


    last_row = max(len(paginas_proc),len(Frames)) + 2
    
    framebt1.grid(column=0, columnspan=2, row=last_row-1)

    incrementarVIbt.grid(column=0, row=last_row, columnspan=2)
    incrementarANbt.grid(column=0, row=last_row+1, columnspan=2)
    framebt2.grid(column=0, columnspan=2, row=last_row+2)
    disminuirVIbt.grid(column=0, row=last_row+3, columnspan=2)
    disminuirANbt.grid(column=0, row=last_row+4, columnspan=2)

    labelinstruccion.grid(row=0, column=2)
    content.grid(column=0, row=0)
    firstlbl.grid(column=0, row=0, columnspan=2)
    secondlbl.grid(column=3, row=0, columnspan=3)
    for pagina in paginas_proc:
        labelsPaginas[pagina].grid(column=0, row=pagina+1)
        bs[pagina].grid(column=1, row=pagina+1)
    
    tabla.grid(column=2, row=3, rowspan=max(len(paginas_proc),len(Frames)))
    framemedio.grid(column=2 , row=2)
    bitacora.grid(column=2, row=1)

    for i in range(len(memoria)):
        labelsMP[i].grid(column=3, row=i+1)
        ms[i].grid(column=4, row=i+1)
        labelsDirLogica[i].grid(column=5, row=i+1)

    salida_archivo = ''

    for instruccion in instructions:
        pag = instruccion[0]//tam_Frame
        tipo = "Reading" if instruccion[1]=='L' else "Writing"
        salida_archivo += f'Instruction:      Address {instruccion[0]} {tipo}\n'
        labelinstruccion.config(text=f'Instruction:      Address {instruccion[0]} {tipo}   >>>   Pagina {pag}')
        bitacora.config(text=f'The requested page is {pag}')
        salida_archivo += f'The requested page is {pag}\n'

        content.after(speed)
        root.update()
        content.update()

        bitacora.config(text='Entering the page table')
        salida_archivo += f'Entering the page table\n'
        content.after(speed)
        root.update()
        content.update()

        
        try:
            info = tabla_pagina[pag]
        except Exception as e:
            bitacora.config(text='The program tried to access an address that did not correspond to those of the')
            salida_archivo += f'The program tried to access an address that did not correspond to those of the\n\n'
            content.after(speed)
            root.update()
            content.update()
            continue
        
        #INSERT IN EMPTY FRAME
        if info[1] == 0:
            fallos +=1
            bitacora.config(text='Page fault, it was not loaded')
            salida_archivo += f'Page fault, it was not loaded\n'
            content.after(speed)
            root.update()
            content.update()
            if len(Frames)!=0:
                m = Frames.pop(0)

                bitacora.config(text=f'entering the page {pag} to the frame {m}')
                salida_archivo += f'entering the page {pag} to the frame {m}\n'
                content.after(speed)
                root.update()
                content.update()

                buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                bo = buttons[pag]
                
                bd = None
                for button in buttons:
                    if button['text'] == f'Frame {m}':
                        bd = button
                
                root.update()
                content.update()
                xo, yo = bo.winfo_x(), bo.winfo_y()
                ro = bo.grid_info()['row']

                rowDestino = bd.grid_info()['row']
                targetLabel = labelsDirLogica[rowDestino-1]
                targetLabel.config(text=f'Page {pag}')

                bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                bo_copy.grid(row=ro, column=1)
                bd.configure(background='red')

                while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                    root.update()
                    content.update()

                    content.after(anim_speed2, move, bo_copy, bd, content)
                    content.after(anim_speed)
                
                root.update()
                content.update()

                bo_copy.destroy()

                bitacora.config(text=f'Changing the valid/invalid bit a 1')
                salida_archivo += f'Changing the valid/invalid bit a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][1] = 1
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'

            else:
                replacements +=1
                LRU = picola.pop(0)
                m = tabla_pagina[LRU][0]

                bitacora.config(text=f'The least recently used page is the page {LRU}, thus releasing the frame{m}')
                salida_archivo += f'The least recently used page is the page {LRU}, thus releasing the frame{m}\n'
                content.after(speed)
                root.update()
                content.update()

                # SWAP OUT
                if tabla_pagina[LRU][2] == 1:
                    bitacora.config(text='The dirty bit is 1, so there is swap out')
                    salida_archivo += f'The dirty bit is 1, so there is swap out\n'
                    content.after(speed)
                    root.update()
                    content.update()

                    buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                    bd = buttons[LRU]
                    
                    bo = None
                    for button in buttons:
                        if button['text'] == f'Frame {tabla_pagina[LRU][0]}':
                            bo = button
                    
                    root.update()
                    content.update()

                    ro = bo.grid_info()['row']


                    bd.configure(background='red')

                    bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                    bo_copy.grid(row=ro, column=4)

                    while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                        root.update()
                        content.update()

                        content.after(anim_speed2, move, bo_copy, bd, content)
                        content.after(anim_speed)
                    
                    targetLabel = labelsDirLogica[ro-1]
                    targetLabel.config(text=f'         ')
                    bo.configure(background='white')
                    bd.configure(background='white')


                    root.update()
                    content.update()
                    bo_copy.destroy()

  
                else:
                    bitacora.config(text='The dirty bit is 0, so there is NO swap out.')
                    salida_archivo += f'The dirty bit is 0, so there is NO swap out.\n'
                    content.after(speed)
                    root.update()
                    content.update()
                
                #SWAP IN
                bitacora.config(text=f'Swap in page {pag} to the frame {m}')
                salida_archivo += f'Swap in page {pag} to the frame {m}\n'
                content.after(speed)
                root.update()
                content.update()

                buttons = [widget for widget in content.winfo_children() if widget.widgetName == 'button']
                bo = buttons[pag]
                
                bd = None
                for button in buttons:
                    if button['text'] == f'Frame {m}':
                        bd = button

                ro = bo.grid_info()['row']

                bo_copy = Button(content, text=bo['text'], width=10, pady=pady, bg='blue')
                bo_copy.grid(row=ro, column=1)

                bd.configure(background='red')

                while bo_copy.winfo_x() != bd.winfo_x() or bo_copy.winfo_y() != bd.winfo_y():
                    root.update()
                    content.update()

                    content.after(anim_speed2, move, bo_copy, bd, content)
                    content.after(anim_speed)

                rowDestino = bd.grid_info()['row']
                targetLabel = labelsDirLogica[rowDestino-1]
                targetLabel.config(text=f'Page {pag}')

                root.update()
                content.update()
                bo_copy.destroy()

                bitacora.config(text=f'Deleting the page row {LRU} in page table')
                salida_archivo += f'Deleting the page row {LRU} in page table\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[LRU] = [None, 0, 0]
                tabla.config(text=print_tablapag(tabla_pagina))

                tabla_pagina[pag][1] = 1
                tabla_pagina[pag][0] = m
                tabla.config(text=print_tablapag(tabla_pagina))

                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
                
            if instruccion[1] == 'E':
                bitacora.config(text=f'writing on the page {pag}')
                salida_archivo += f'writing on the page {pag}\n'
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Changing the dirty bit of the page {pag} a 1')
                salida_archivo += f'Changing the dirty bit of the page {pag} a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
            else:
                bitacora.config(text=f'reading on page {pag}')
                salida_archivo += f'reading on page {pag}\n'
                content.after(speed)
                root.update()
                content.update()
        else:
            bitacora.config(text=f'The page was already loaded, specifically in the Frame {tabla_pagina[pag][0]}')
            salida_archivo += f'The page was already loaded, specifically in the Frame {tabla_pagina[pag][0]}\n'
            content.after(speed)
            root.update()
            content.update()

            if instruccion[1] == 'E':
                bitacora.config(text=f'writing on the page {pag}')
                salida_archivo += f'writing on the page {pag}\n'
                content.after(speed)
                root.update()
                content.update()

                bitacora.config(text=f'Changing the dirty bit of the page {pag} a 1')
                salida_archivo += f'Changing the dirty bit of the page {pag} a 1\n'
                content.after(speed)
                root.update()
                content.update()

                tabla_pagina[pag][2] = 1
                tabla.config(text=print_tablapag(tabla_pagina))
                salida_archivo += f'\n{print_tablapag(tabla_pagina)}\n'
            else:
                bitacora.config(text=f'reading on page {pag}')
                salida_archivo += f'reading on page {pag}\n'
                content.after(speed)
                root.update()
                content.update()
                
        if pag in picola:
            picola.remove(pag)
            picola.append(pag)
            salida_archivo += f'Deleting the page from the stack {pag} and entering it at the end\n'
            salida_archivo += f'picola: {str(picola)}'
        else:
            picola.append(pag)
            salida_archivo += f'Entering the picola page {pag}\n'
            salida_archivo += f'picola: {str(picola)}'
        salida_archivo+= f'\n{"-"*30+"//"+"-"*30}\n\n'

    bitacora.config(text=f'end of execution, Your log is in the log file.txt')
    salida_archivo += f'end of execution\n'
    labelinstruccion.config(text=f'No. page faults: {fallos},   No. replacements: {replacements}')
    salida_archivo += f'No. page faults: {fallos},   No. replacements: {replacements}'

    content.after(speed)
    root.update()
    content.update()
        # input('Presione cualquier tecla para seguir a la proxima iteracion')
    
    with open('bitacora.txt', 'w') as f:
        print(salida_archivo, file=f)


def tomar_datos():
    clear()
    # a1,a2,a3,a4 = '5','15','70','8'

    frame = ttk.Frame(content, width=800, height=100).pack()

    tam_Frame = Entry(root, width = 60, font=('Helvetica', 14))
    so = Entry(root, width = 60, font=('Helvetica', 14))
    proc = Entry(root, width = 60, font=('Helvetica', 14))
    Frames = Entry(root, width = 60, font=('Helvetica', 14))

    Label(root, text="frame size", font=('Helvetica', 14)).pack()

    tam_Frame.pack(pady=10)
    tam_Frame.insert(0, 'Eg: 16')
    # tam_Frame.insert(0, a1)

    tam_Frame.configure(state='disabled')

    Label(root, text="OS size", font=('Helvetica', 14)).pack()

    so.pack(pady=10)
    so.insert(0, 'Eg: 60')
    # so.insert(0, a2)
    so.configure(state='disabled')

    Label(root, text="process size", font=('Helvetica', 14)).pack()

    proc.pack(pady=10)
    proc.insert(0, 'Eg: 40')
    # proc.insert(0, a3)
    proc.configure(state='disabled')

    Label(root, text="Available frames separated by space", font=('Helvetica', 14)).pack()

    Frames.pack(pady=10)
    Frames.insert(0, 'Eg: 7 9 10, that do not conflict with OS Frames')
    # Frames.insert(0, a4)
    Frames.configure(state='disabled')

    ttk.Frame(content, width=800, height=50).pack()
    Label(root, text="Select your instruction file: ", font=('Helvetica', 14)).pack()

    select_file_button = Button(root, text="Select", command=select_file, pady=2, bg='darkorange', font=('Helvetica', 14)).pack()
    ttk.Frame(content, width=800, height=50).pack()
    ruta = Label(root, text=file_name, font=('Helvetica', 12))
    ruta.pack()    

    ttk.Frame(content, width=800, height=40).pack()
    my_button2 = Button(root, text="Get into", command=check_values, font=("Helvetica", 24), fg="#DDDDDD", bg="darkolivegreen").pack()
    


    warn = Label(root, text="-", font=("Helvetica", 12), pady=30).pack()
    
    tam_Frame_focus_in = tam_Frame.bind('<Button-1>', lambda x: on_focus_in(tam_Frame))
    tam_Frame_focus_out = tam_Frame.bind(
        '<FocusOut>', lambda x: on_focus_out(tam_Frame, 'Eg: 16'))

    so_focus_in = so.bind('<Button-1>', lambda x: on_focus_in(so))
    so_focus_out = so.bind(
        '<FocusOut>', lambda x: on_focus_out(so, 'Eg: 60'))

    proc_focus_in = proc.bind('<Button-1>', lambda x: on_focus_in(proc))
    proc_focus_out = proc.bind(
        '<FocusOut>', lambda x: on_focus_out(proc, 'Eg: 40'))

    Frames_focus_in = Frames.bind('<Button-1>', lambda x: on_focus_in(Frames))
    Frames_focus_out = Frames.bind(
        '<FocusOut>', lambda x: on_focus_out(Frames, 'Eg: 7 9 10, that do not conflict with OS Frames'))

def check_values():
    l = []
    for widget in root.winfo_children():
        if widget.widgetName == 'entry':
            l.append(widget)
    tam_Frame, so, proc, Frames = [widget.get() for widget in l]

    wlabel = root.winfo_children()[-1]
    
    try:
        tam_Frame = int(tam_Frame)
    except Exception as e:
        wlabel.config(text="You must enter a number in the Frame size field")
        return
    
    if tam_Frame <= 0:
        wlabel.config(text="You must enter a positive number in the Frame size field")
        tam_Frame = None
        return

    try:
        so = int(so)
    except Exception as e:
        wlabel.config(text="You must enter a number in the OS size field")
        return
        
    if so <= 0:
        wlabel.config(text="You must enter a positive number in the OS size field")
        return

    try:
        proc = int(proc)
    except Exception as e:
        wlabel.config(text="You must enter a number in the process size field")
        return
    
    if proc <= 0:
        wlabel.config(text="You must enter a positive number in the process size field")
        return

    Frames_so = list(range(mt.ceil(so/tam_Frame)))
    paginas_proc = list(range(mt.ceil(proc/tam_Frame)))

    try:
        temp = Frames.split(' ')
        Frames = [int(s) for s in temp]
        if len(set(Frames)) != len(Frames):
            raise Exception
    except Exception as e:
        wlabel.config(text="You must enter different integers separated by space, Eg: 7 9 10")
        return
    
    a = set(Frames_so)
    b = set(Frames)
    
    if not all(n >= 0 for n in Frames):
        wlabel.config(text="Frame number must be positive")
        return
    
    if a & b:
        wlabel.config(text=f'Free Frames conflict with Frames to be used by the OS that are: {str(Frames_so)}\n')
        return
    
    instructions = []

    try:
        with open(file_name, encoding='utf-8-sig') as f:
            opened_file = csv.reader(f, delimiter=',')
            for row in opened_file:
                instructions.append(row)
                
        instructions = tuple(zip(instructions[0], instructions[1]))
        instructions = [(int(tuple[0]), tuple[1]) for tuple in instructions]
    except Exception as e:
        wlabel.config(text=f'There was a problem with your file, please upload it again')
        return
    
    Frames = sorted(Frames)
    start_iterations(tam_Frame, so, proc, Frames, Frames_so, instructions)


def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')

def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.configure(state='disabled')

def clear():
    for widget in root.winfo_children():
        widget.destroy()

content = ttk.Frame(root, padding=40).pack()
frame = ttk.Frame(content, width=800, height=200).pack()
text = ttk.Label(content, text=" Counter controlled demand paging simulation", padding=5, font=("Helvetica", 16)).pack()
frame2 = ttk.Frame(content, width=800, height=100).pack()
my_button = Button(content, text="Start", command=tomar_datos, font=("Helvetica", 24), fg="#DDDDDD", bg="#FF4C29").pack()

root.update()
root.mainloop()

# if __name__ == '__main__':
#     main()