#this  will be the file containing most of the gmae objects
import pyglet
import os
import random



key = pyglet.window.key



class Main(pyglet.window.Window):
    def __init__ (self):
        super(Main, self).__init__(1280, 720, fullscreen = False)
        self.x, self.y = 0, 0
        self.active = 1
    def on_draw(self):
        self.render()
    #handle inputs of a window
    #this is really inefficient stuff
    #also, there's way too many nests here, it's hard to read
    def on_key_press(self, symbol, modifiers):
        testgui.equipment = testplayer.pickeditems
        if symbol == key.NUM_1:
            if len(testgui.equipment) >= 1:
                print("tried using the potion")
                testplayer.useitem(testgui.equipment[0])
            else:
                print("no item")
        #check health of every enemy
        for enemy in enemycollidable:
            if enemy[0].health <= 0:
                enemycollidable.remove(enemy)
        
        for item in itemcollidable:
            if item[0].health <= 0:
                itemcollidable.remove(item)
        
        #this function checks for all the collisions, including collisions with items, this is REALLY unreadable, and needs
        #a total rewrite
        if symbol == key.UP:
            if testplayer.detectcollision(collidablelist, 0, -20) or testplayer.detectcollision(enemycollidable, 0, -20):
                return
            else:
                testplayer.detectcollision(itemcollidable, 0, -20)
                testplayer.move(0, 20)
                for enemy in enemycollidable:
                    enemy[0].behaviour(collidablelist,testplayer, 0, -1)
        if symbol == key.DOWN:
            if testplayer.detectcollision(collidablelist, 0, 20) or testplayer.detectcollision(enemycollidable, 0, 20):
                return
            else:
                testplayer.detectcollision(itemcollidable, 0, 20)
                testplayer.move(0, -20)
                for enemy in enemycollidable:
                    enemy[0].behaviour(collidablelist,testplayer, 0, -1)
        if symbol == key.RIGHT:
            if testplayer.detectcollision(collidablelist, -20, 0) or testplayer.detectcollision(enemycollidable, -20, 0):
                return
            else:
                testplayer.detectcollision(itemcollidable, -20, 0)
                testplayer.move(20, 0)
                for enemy in enemycollidable:
                    enemy[0].behaviour(collidablelist,testplayer, -1, 0)
        if symbol == key.LEFT:
            if testplayer.detectcollision(collidablelist, 20, 0) or testplayer.detectcollision(enemycollidable, 20, 0):
                return
            else:
                testplayer.detectcollision(itemcollidable, 20, 0)
                testplayer.move(-20, 0)
                for enemy in enemycollidable:
                    enemy[0].behaviour(collidablelist,testplayer, 1, 0)
    def on_mouse_press(self, x, y, button, modifiers):
        #print(x, y)
        pass
    def on_press(self, x, y, button, modifiers):
        print("here i'm doing button press")
    #this handles enemy turns for now, as they should be done AFTER the player moves
    def on_key_release(self, symbol, modifiers):
        for enemy in enemycollidable:
            if enemy[0].detectcollision([[testplayer]], -20, 0):
                enemy[0].attack(testplayer)
            elif enemy[0].detectcollision([[testplayer]], 20, 0):
                enemy[0].attack(testplayer)
            elif enemy[0].detectcollision([[testplayer]], 0, 20):
                enemy[0].attack(testplayer)
            elif enemy[0].detectcollision([[testplayer]], 0, -20):
                enemy[0].attack(testplayer)

    def render(self):
        self.clear()

        self.pre_render()

        #playerbatch.draw()
        batch.draw()
        testgui.WriteInfo()
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

        self.createtileset()
    def createtileset(self):
        tilelist = []
        for i in range(0, self.height):
            for n in range(0, self.width):
                tilelist.append(Tile(self.image, self.x + (n*20), self.y + (i*20), 0.1, self.batch, self.group))
        self.tilelist = tilelist





#change the name
#playobject inherits from tile because objects are like tiles, just that they can move and interact around.

#entities should accept their coordinates in grid coordinates, not real coordinates
class Entity(Tile):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group)
        self.health = health
        self.atkdmg = atkdmg
    def move(self, xchange, ychange):
        self.x += xchange
        self.y += ychange 
    #this class detects colission before it happens, meaning when there's a wall before the entity, it will return true
    def detectcollision(self, tileset, xchange, ychange):
        for n in tileset:
            for i in n:
                if self.x == i.x + xchange and self.y == i.y + ychange:
                    self.checktheinteraction(i)
                    self.checkdelete()
                    return True
        return False
    #this function is made only to be overwritten, as many entities need different checks for different interactions
    def checktheinteraction(self, touched):
        pass
    def checkdelete(self):
        if self.health <= 0:
            self.__del__()
    def attack(self, other):
        other.health -= self.atkdmg
        other.checkdelete()
        print(other.health)
    def RandomizeStats(self):
        self.stats = []
        #stats in a list, starting from index 0 is str, int, wis, dex, con
        for i in range(0, 5):
            self.stats.append(random.randint(10, 20))
        

class Player(Entity):
    def __init__(self, image, x, y, z, batch, group, health,atkdmg):
        super().__init__(image, x, y, z,  batch, group, health, atkdmg)
        self.RandomizeStats()
        self.pickeditems = []
    def attack(self, other):
        other.health -= self.atkdmg
        other.checkdelete()
        #this is a hack so that we will also get dmg when attacked, but this should be done inside Enemy class, not here
        print(other.health)
    def pickup(self, other):
        bruh = -1
        for i in other.stats:
            bruh += 1
            if i > self.stats[bruh]:
                print("can't pick the item because you don't have the stats")
                return
        #this is a hack, all items have nearly 0 hp, so they "die" when picked up
        self.attack(other)
        self.pickeditems.append(other.name)
        print(self.pickeditems)
    def checktheinteraction(self, touched):
        if type(touched)==StairCase:
            print("going next level lol")
        if issubclass(type(touched), Enemy):
            self.attack(touched)    
        if issubclass(type(touched), Item):
            self.pickup(touched)
    def useitem(self, equipment):
        self.pickeditems.remove(equipment)
    


class Enemy(Entity):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
    def checktheinteraction(self, touched):
        pass
    #this is the default behaviour for enemies
    def behaviour(self, collidablelist, player, directionx, directiony):
        pass
#defining enemies
#higher level  of abstraction
#this enemy doesn't move, and only attacks the player when close
class Troll(Enemy):
    def __init__(self, image, x, y, z, batch, group, health = 100, atkdmg = 10):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
    
class Snake(Enemy):
    def __init__(self, image, x, y, z, batch, group, health = 30, atkdmg = 2):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
    def behaviour(self, collidablelist, player, directionx, directiony):
        #test code, it's unreadable, and needs a change
        if self.detectcollision(collidablelist, 20, 0) == False or self.detectcollision(collidablelist, -20, 0) == False or self.detectcollision(collidablelist, 0, -20) == False or self.detectcollision(collidablelist, 0, 20) == False :
            if self.detectcollision([[player]], -60, 0) or self.detectcollision([[player]], 60, 0) or self.detectcollision([[player]], 0, -60) or self.detectcollision([[player]], 0, 60):
                self.move(20 * directionx, 20 * directiony)
        

class StairCase(Entity):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg = 0):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)



#attributes from items should change attributes of player, or have special use cases.
class Item(Entity):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
        self.stats = []
        self.name = "Item"
#defining items, higher level of abstraction
class Sword(Item):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg, strenght):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
        self.stats.append(strenght)
        self.name = "Sword"

class HealthPotion(Item):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg, wisdom):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)
        self.stats.append(wisdom)
        self.name = "Health Potion"

class Antidote(Item):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)

class Bow(Item):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)

class Arrow(Item):
    def __init__(self, image, x, y, z, batch, group, health, atkdmg):
        super().__init__(image, x, y, z, batch, group, health, atkdmg)

#this class should be a child class of batch, as it's just an agregation of different elements, but it works for now
#so im leaving it this way
        
class GUI(pyglet.shapes.BorderedRectangle):
    def __init__(self, x, y, width, height, border, color, equipment:list, player, border_color=..., batch=None, group=None):
        super().__init__(x, y, width, height, border, color, border_color, batch, group)
        self.equipment = equipment
        self.player = player
        self.guibatch = pyglet.graphics.Batch()
        #need the image because pyglet buttons need images for some reason
        self.buttonimage = tileset[43]
        
        self.WriteInfo()
    def WriteInfo(self):
        equipmentlistlabel = []
        healthlabel = pyglet.text.Label(str(self.player.health),
                          font_name='Times New Roman',
                          font_size=12,
                          x=self.x + 20, y=self.y + 700,
                          anchor_x='center', anchor_y='center', batch=self.guibatch, group=bestground)
        
        characternamelabel = pyglet.text.Label(str(self.player.atkdmg),
                          font_name='Times New Roman',
                          font_size=12,
                          x=self.x + 20, y=self.y + 680,
                          anchor_x='center', anchor_y='center', batch=self.guibatch, group=bestground)
        bruh = -1
        
        for i in self.equipment:
            bruh += 1
            equipmentlistlabel.append(pyglet.text.Label(str(i) + " [Use key '" + str(bruh + 1) + "']",
                          font_name='Times New Roman',
                          font_size=12,
                          x=(self.x + 20), y=(self.y + 500) + (bruh * 20),
                          anchor_x='left', anchor_y='bottom', batch=self.guibatch, group=bestground))

            
        self.draw()
        self.guibatch.draw()

#this class, and also the Tunnel class need a total rewrite, because it's really messy.
#also, they probably should inherit from tileset
class Room():
    def __init__(self, x, y, width, height, batch, group, exitdirection, tilenum):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.batch = batch
        self.group = group
        self.CreateRoom()
        
        self.exitdirection = exitdirection
        self.tilenum = tilenum
        self.CreateOpening()

        #calculate corners, starting from downward left, going counterclockwise 
        self.x1 = self.x
        self.y1 = self.y

        self.x2 = self.x + (self.width*20)
        self.y2 = self.y

        self.x3 = self.x + (self.width*20) 
        self.y3 = self.y + (self.height*20)

        self.x4 = self.x
        self.y4 = self.y + (self.height*20)

    def CreateRoom(self):
        bottomwall = TileSet(tileset[66], self.x, self.y, self.width, 1, self.batch, self.group)
        floor = TileSet(tileset[249], bottomwall.x + 20, bottomwall.y + 20, self.width - 2, self.height - 2, self.batch, self.group)
        leftwall = TileSet(tileset[66], bottomwall.x4, bottomwall.y4, 1, self.height - 2, self.batch, self.group)
        rightwall = TileSet(tileset[66], bottomwall.x3-20, bottomwall.y3, 1, self.height - 2, self.batch, self.group)
        topwall = TileSet(tileset[66], leftwall.x4 , leftwall.y4, self.width, 1, self.batch, self.group)

        self.collidable = [bottomwall.tilelist, rightwall.tilelist, leftwall.tilelist, topwall.tilelist]
        self.noncollidable = floor.tilelist
    #we know the position of the walls inside our list, which means that we can easily access it. We can delete the tile we want
    #because we know that every tile inside list has it's own "grid position"
    def CreateOpening(self):
        bruh = -1
        for i in self.exitdirection:
            bruh += 1
            if i == "up":
                del self.collidable[3][self.tilenum[bruh]]
            if i == "left":
                del self.collidable[2][self.tilenum[bruh]]
            if i == "down":
                del self.collidable[0][self.tilenum[bruh]]
class Tunnel():
    def __init__(self, xstart, ystart, xend, yend, batch, group, start:str):
        self.xstart = xstart
        self.ystart = ystart
        
        #these coordinates are tile coordinates, meaning that when given x = 1 and y =1 there should only be one tile 
        self.xend = xend
        self.yend = yend
        
        
        self.start = start
        self.batch = batch
        self.group = group
        




        self.GenerateTunnel()
    #really messy code, needs a rewrite
    #actually scratch that, this code is worse then messy, it's nearly unreadable
    def GenerateTunnel(self):
        tilelistfloor = []
        tilelistwall = []
        if self.yend < 0 and self.xend > 0:
            self.yend = abs(self.yend)
            for i in range(0, self.yend):
                tilelistwall.append(Tile(tileset[67],self.xstart, self.ystart  - (i * 20), 0.1, self.batch, self.group))
                tilelistfloor.append(Tile(tileset[248],self.xstart + 20, self.ystart  - (i * 20), 0.1, self.batch, self.group))
                tilelistwall.append(Tile(tileset[67],self.xstart + 40, self.ystart  - (i * 20), 0.1, self.batch, self.group))
            for i in range(0, self.xend):
                tilelistwall.append(Tile(tileset[67],self.xstart + (i*20), self.ystart - (self.yend*20) + 20, 0.1, self.batch, self.group))
                #essentialy what this if does is that it doesn't allow the first wall to be spawned, because it was already here from the first for loop 
                if i != 0:
                    tilelistfloor.append(Tile(tileset[248],self.xstart + (i*20), self.ystart - (self.yend*20) + 40, 0.1, self.batch, self.group))
                if i != 1:
                    tilelistwall.append(Tile(tileset[67],self.xstart + (i*20), self.ystart - (self.yend*20) + 60, 0.1, self.batch, self.group))
        elif self.yend > 0 and self.xend > 0:
            for i in range(0, self.yend):
                tilelistwall.append(Tile(tileset[67],self.xstart, self.ystart  + (i * 20), 0.1, self.batch, self.group))
                tilelistfloor.append(Tile(tileset[248],self.xstart + 20, self.ystart  + (i * 20), 0.1, self.batch, self.group))
                if i != self.yend - 2:
                    tilelistwall.append(Tile(tileset[67],self.xstart + 40, self.ystart  + (i * 20), 0.1, self.batch, self.group))
            for i in range(0, self.xend):
                tilelistwall.append(Tile(tileset[67],self.xstart + (i*20), self.ystart + (self.yend*20) - 20, 0.1, self.batch, self.group))
                #essentialy what this if does is that it doesn't allow the first wall to be spawned, because it was already here from the first for loop 
                if i != 0:
                    tilelistfloor.append(Tile(tileset[248],self.xstart + (i*20), self.ystart + (self.yend*20) - 40, 0.1, self.batch, self.group))
                if i != 1:
                    tilelistwall.append(Tile(tileset[67],self.xstart + (i*20), self.ystart + (self.yend*20) - 60, 0.1, self.batch, self.group))
        
        self.collidable = tilelistwall
        self.noncollidable = tilelistfloor
    def CreateOpening(self):
        pass
tilegrid = pyglet.resource.image("curses_800x600.png")
tilerows = 16
tilecols = 16
tileset = pyglet.image.ImageGrid(tilegrid, 16, 16)





x = Main()

batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)
bestground = pyglet.graphics.Group(order=2)

#test
backpack = []
testplayer = Player(tileset[100],220, 220, 1, batch, foreground, 10, 10)
# creating GUI
testgui = GUI(960, 0, 320, 720, 10, (0, 0, 0),backpack, testplayer, (255, 0, 0), batch, foreground)
#creating a testlevel

startroom = Room(200, 200, 10, 10, batch, background, ["up"], [1])
tunnelstartto2nd = Tunnel(startroom.x4, startroom.y4, 20, 10, batch, background, "s")
scndndroom = Room(startroom.x4 + (20* 20), startroom.y4 + (10*10), 10, 10, batch, background, ["left", "down"], [2, 1])
tunnel2ndtoend = Tunnel(scndndroom.x1, scndndroom.y1 - 20, 1, -14, batch, background, "s")
lastroom = Room(scndndroom.x1, scndndroom.y1 - (20*20), 6, 6, batch, background, ["up"], [1])

#populating with entities
testtroll = Troll(tileset[255], lastroom.x4 + 20, lastroom.y4 - 20, 0.1, batch, foreground)
testsnake = Snake(tileset[255], scndndroom.x4 + 40, scndndroom.y4 - 40, 0.1, batch, foreground)

testitem = HealthPotion(tileset[238], startroom.x4 +20 , startroom.y4 - 20, 0.1, batch, foreground,1, 0, 10)
teststaircase = StairCase(tileset[239], lastroom.x4 + 40, lastroom.y4 - 40, 0.1, batch, foreground, None)


#aggregate collidables into one big array so we can detect collisions
#ofc this will need optimization, but not needed for the tests

collidablelist = []


#this list is special, because it will be checked for destroyed enemies, this way we can easily del them
enemycollidable = []

#same here but with items
itemcollidable = []


for i in startroom.collidable:
    collidablelist.append(i)

for i in scndndroom.collidable:
    collidablelist.append(i)

for i in lastroom.collidable:
    collidablelist.append(i)

collidablelist.append(tunnelstartto2nd.collidable)
collidablelist.append(tunnel2ndtoend.collidable)
collidablelist.append([teststaircase])

itemcollidable.append([testitem])

enemycollidable.append([testtroll])
enemycollidable.append([testsnake])

#remove all the entities that are appended to the table
del testtroll
del testsnake
del testitem


#testbutton.

x.run()


