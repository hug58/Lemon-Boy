import pygame
import pytmx
from script import Player
from script import Enemies
from script import Element

pygame.display.init()

WIDTH = 420
HEIGHT = 420

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Project Lemon 0.4.0")


class TileMap:
	def __init__(self,filename):
		tm = pytmx.load_pygame(filename,pixelaplha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm
	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x,y,gid in layer:
					tile = ti(gid)
					if tile:
						surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
	def make_map(self):
		temp_surface = pygame.Surface((self.width,self.height))
		self.render(temp_surface)
		return temp_surface

class Camera:
	def __init__(self,width,height):
		self.camera = pygame.Rect((0,0),(width,height))
		self.width = width
		self.height = height
	def apply(self,entity):
		return entity.rect.move(self.camera.topleft)
	def apply_rect(self,rect):
		return rect.move(self.camera.topleft)
	def update(self,target):
		#Targe en negativo para que en caso de llegar al extremo left (positivo) , el movimiento sea 0
		x =-target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)
		#print(x)
		#limit scrolling to map size
		x = min(0,x) #left
		y = min(0,y) #top
		#print(self.width)
		#lógica inversa
		#Si -(self.width - WIDTH) es menor que X, X seguira avanzando, en caso contrario X se mantendrá fijo
		x = max(-(self.width - WIDTH),x)#right
		y = max(-(self.height-HEIGHT),y)
		self.camera = pygame.Rect(x,y,self.width,self.height)

class Plataform(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y

class Game:
	def __init__(self):
		self.maps= ["map/map1.tmx","map/map2.tmx"]
		self.map = TileMap(self.maps[0])
		self.Mapimage = self.map.make_map()
		self.Maprect = self.Mapimage.get_rect()
		self.camera = Camera(self.map.width,self.map.height)
		
	def collided(self):
		if pygame.sprite.spritecollide(self.player,self.enemies,False,False):
			pass
			#self.player.lifes -=1

						
	
	def load(self):
		
		#self.group = pygame.sprite.Group()
		self.plataform = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.objs = pygame.sprite.Group()
		
		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "Player":
				self.player = Player.Player(tile_object.x,tile_object.y,self.plataform)
				#self.player.lifes = lifes
			elif tile_object.name == "plataform":
				self.plataform.add(Plataform(tile_object.x,tile_object.y,tile_object.width,tile_object.height))

				#self.objs.add(Element.)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "Door":
				if tile_object.type == "YELLOW":
					self.objs.add(Element.Door(tile_object.x,tile_object.y,self.player,"YELLOW"))
			elif tile_object.name == "Skull":
				self.enemies.add(Enemies.Skull(tile_object.x,tile_object.y,self.plataform,self.player.rect))
			elif tile_object.name == "Dog":
				if tile_object.type == "left":
					self.enemies.add(Enemies.Dog(tile_object.x,tile_object.y,self.plataform,"left"))
				elif tile_object.type == "right":
					self.enemies.add(Enemies.Dog(tile_object.x,tile_object.y,self.plataform,"right"))
			elif tile_object.name == "Key":
				self.objs.add(Element.Key(tile_object.x,tile_object.y,self.player))

		
	def update(self):
		self.camera.update(self.player)
		self.enemies.update()
		for objs in self.objs:
			objs.update()
			try:
				if objs.next == True:
					self.map =  TileMap(self.maps[1])
					self.Mapimage = self.map.make_map()
					self.Maprect = self.Mapimage.get_rect()
					self.camera = Camera(self.map.width,self.map.height)
					self.load()
					
			except:
				pass

		self.player.update()
		#self.collided()

	def draw(self):
		
		SCREEN.blit(self.Mapimage,self.camera.apply_rect(self.Maprect))
		for enemies in self.enemies:
			SCREEN.blit(enemies.image,self.camera.apply(enemies))
		for objs in self.objs:
			SCREEN.blit(objs.image,self.camera.apply(objs))
		SCREEN.blit(self.player.image,self.camera.apply(self.player))
		
	
def Main():

	exit = False
	clock = pygame.time.Clock()
	game = Game()
	game.load()

	while exit == False:
		clock.tick(40)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					game.player.vly = -14.5 if game.player.cont_jump > 0 else game.player.vly
					game.player.cont_jump -=1

			if event.type == pygame.KEYUP:
				game.player.detener = True




		game.update()
		game.draw()
		pygame.display.flip()




if __name__ == "__main__":
	Main()
	pygame.quit()