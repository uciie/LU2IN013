# interface_graph.py:
import tkinter as tk

class Interface:
    def __init__(self, name, width, height, color):
        """
        """
        self.root = tk.Tk()
        self.root.title(name)
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)
        self.canvas.pack()

    def draw_obj(self, Objet):
        """
        """
        self.canvas.create_rectangle( 
            Objet.posX - Objet.width/2, Objet.posY - Objet.length/2, 
            Objet.posX+Objet.width/2, Objet.posY+Objet.length/2, fill=Objet.color)
        
        if hasattr(Objet, 'vectDir') :
            self.canvas.create_line(Objet.posX, Objet.posY, Objet.posX + Objet.vectDir.x*Objet.length,Objet.posY+Objet.vectDir.y*Objet.length, arrow=tk.LAST)

    def draw_roue(self, Roue):
        """
        """
        self.canvas.create_line(Roue.posX, Roue.posY, Roue.posX + Roue.vectDir.x*5,Roue.posY+Roue.vectDir.y*5, arrow=tk.LAST)

    def delete_draw(self, Objet):
        """
        """
        if Objet:
            self.canvas.delete(Objet)
    
    def creer_button(self, name, command): 
        """
        """
        return tk.Button(self.root, text=name, command=command)
