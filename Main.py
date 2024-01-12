#this  will be the file containing most of the gmae objects
import pyglet
import os
#importing pyglet classes
from pyglet import font

key = pyglet.window.key



class Main(pyglet.window.Window):
    def __init__ (self):
        super(Main, self).__init__(1280, 720, fullscreen = False)
        self.x, self.y = 0, 0
        self.active = 1
    def on_draw(self):
        self.render()
    #handle inputs of a window
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if testplayer.detectcollision(testwall, 0, -20):
                return
            else:
                testplayer.move(0, 20)
        if symbol == key.DOWN:
            if testplayer.detectcollision(testwall, 0, 20):
                return
            else:
                testplayer.move(0, -20)
        if symbol == key.RIGHT:
            if testplayer.detectcollision(testwall, -20, 0):
                return
            else:
                testplayer.move(20, 0)
        if symbol == key.LEFT:
            if testplayer.detectcollision(testwall,20, 0):
                return
            else:
                testplayer.move(-20, 0)
    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)
    def render(self):
        self.clear()

        self.pre_render()

        #playerbatch.draw()
        batch.draw()
        self.flip()

    def run(self):
        while self.active == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
    def pre_render(self):
        pass  

#a bit of a syntactic sugar, but makes it way easier to define which sprite is doing what
class Tile(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, z, batch, group):
        super().__init__(img, x, y, z, batch = batch, group=group)
      

class TileSet():
    def __init__(self, image, x, y, width, height, batch, group):
        self.image = image
        
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height

        self.batch = batch
        self.group = group

        #calculate corners, starting from downward left, going counterclockwise
        self.x1 = self.x
        self.y1 = self.y

        self.x2 = self.x + (self.width*20)
        self.y2 = self.y

        self.x3 = self.x + (self.width*20) 
        self.y3 = self.y + (self.height*20)

        self.x4 = self.x
        self.y4 = self.y + (self.height*20)
    
    def createtileset(self):
        tilelist = []
        for i in range(0, self.height):
            for n in range(0, self.width):
                tilelist.append(Tile(self.image, self.x + (n*20), self.y + (i*20), 0.1, self.batch, self.group))
        self.tilelist = tilelist
        return




#change the name
#playobject inherits from tile because objects are like tiles, just that they can move and interact around.


class Entity(Tile):
    def __init__(self, image, x, y, z, batch, group, health, speed, atkspeed):
        super().__init__(image, x, y, z, batch, group)
    def move(self, xchange, ychange):
        self.x += xchange
        self.y += ychange 
    #this class detects colission before it happens, meaning when there's a wall before the char, it will return true
    def detectcollision(self, tileset, xchange, ychange):
        for i in tileset.tilelist:
            if self.x == i.x + xchange and self.y == i.y + ychange:
                return True
        return False



class Player(Entity):
    def __init__(self, image, x, y, z, batch, group, health, speed, atkspeed):
        super().__init__(image, x, y, z,  batch, group, health, speed, atkspeed)
    def attack(self, other):
        pass
    def pickup(self, other):
        pass


tilegrid = pyglet.resource.image("curses_800x600.png")
tilerows = 16
tilecols = 16
tileset = pyglet.image.ImageGrid(tilegrid, 16, 16)
print(tileset[255])




x = Main()

batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)


#playerbatch = pyglet.graphics.Batch()
testfloor = TileSet(tileset[249], 200, 200, 10, 10, batch, background)
testwall = TileSet(tileset[66], 400, 200, 1, 10, batch, foreground)
testfloor.createtileset()
print(testfloor.x2, testfloor.y2)
testwall.createtileset()
#testsprite = pyglet.sprite.Sprite(tileset[255], 200, 200)
testplayer = Player(tileset[100],200, 680, 1, batch, foreground, 1, 1, 1)
#testtile = Tile(tileset[244], 200, 200)

x.run()

