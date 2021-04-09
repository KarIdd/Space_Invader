# import des librairies nécessaires au fonctionnement du programme
import pygame,sys
from pygame.locals import *
from random import *
			

pygame.init()
pygame.font.init()
window=pygame.display.set_mode((450,560,),0,32)     	# Taille fenêtre du jeu
pygame.display.set_caption('SpaceInvader')          	# titre de la fenêtre
Texty = pygame.font.Font('SUPERPOI_R.TTF', 10)
Over = pygame.font.Font('SUPERPOI_R.TTF', 30)
Obj_texte = Texty.render('invaders', 0, (0,0,255))
musique=pygame.mixer.Sound('space_invader_music.wav')       # charge la musique dans la variable musique
musique.play(-1)            # joue la musique en boucle

class Unit:

    def __init__(self):
    # initialisation de la classe Unit
        self.invader1=pygame.image.load("invader1.png")         # charge les deux images des cibles
        self.invader2=pygame.image.load("invader2.png")
        self.cible=[]           # liste des cibles
        self.i=0            

        self.ship=pygame.image.load('ship.png')           # charge l'image du vaisseau
        self.xs=20							# coordonnées de départ du vaisseau
        self.ys=500
        self.k=0                # variable servant à définir la cadence des tirs
        self.missile=[]         # stocke la liste des missiles présents à l'écran
        self.point=0            # stocke le nombre de point gagné par le joueur

    def spawn_invader(self, y1, y2):
    # fait apparaître les cibles en haut de l'écran
        for a in range(y1,y2,50):
            for b in range(20,400,50):
                self.cible.append(pygame.Rect(b,a,32,24))

    def show_invader(self):
    # affiche les cibles avec une animation de deux frames
        for c in self.cible:
            self.i+=1
            for c in self.cible:
                if int(self.i/100)%2 ==1:
                    window.blit(self.invader1,c)
                else:
                    window.blit(self.invader2,c)
    
    def move_invader(self):
    # déplace toutes les cibles et les fait réapparaître en cas de destruction totale
        backup=[]
        for c in self.cible:
            if c.top>=560:
                self.cible.remove(c)
            else:
                backup.append(c.move(0,1))
        self.cible=backup
        if self.cible==[]:
            self.spawn_invader(0, 100)
        

    def show_ship(self):
    # affiche le vaisseau aux coordonnées self.xs, self.ys
        window.blit(self.ship,(self.xs,self.ys))

    def left_ship(self):
    # empèche le vaisseau de sortir de l'écran à gauche
        if self.xs>10 : self.xs-=3
        
    def right_ship(self):
    # empèche le vaisseau de sortir de l'écran à droite
        if self.xs<400 : self.xs+=3
        
    def fire(self):
    # ajoute 1 à la variable self.k
        self.k+=1

    def game_stop(self):
    # vérifie le positionnement des cibles et renvoie True, qui indique un "Game Over" si elles sortent de l'écran
        for c in self.cible:
            if c.top>=560:
                return True
        
    def verif_tir(self):
    # lance les missiles à une cadence précise tout en jouant un son à leur envoi
        if self.k%10==1 :
            son_tir=pygame.mixer.Sound('laser_sound_effect.wav')
            son_tir.play(0)
            self.missile.append(pygame.Rect(self.xs+12,self.ys-5,6,16))
            self.k+=1
        
    def tir(self):
    # gère la position des missiles et les détruits en fonction de leur positionnement dans le niveau et des cibles
        for tir in self.missile:					
            tir.top=tir.top-10				
            pygame.draw.rect(window,0xFF0000,tir)		
            if tir.top<=0:				
                self.missile.remove(tir)			
            for c in self.cible:            
                if tir.colliderect(c):          
                    self.missile.remove(tir)            
                    self.cible.remove(c)            
                    self.point+=100             


class Space_invader:

    def __init__(self):
   # initialisation de la classe Space_invader
        self.unit=Unit()         # récupère la classe Unit dans la variable self.unit

    def jeu(self):
    # gère les interactions entre le joueur et la machine
        right = False
        left = False
        shot = False
        self.unit.spawn_invader(0, 100)

        mainclock=pygame.time.Clock()	

        while True:
            window.fill (25)					# rempli l'arrière plan avec la couleur RGB Bleu foncé
            window.blit(Obj_texte,(50,20))			# place le texte
            Score = Texty.render(f'score  {self.unit.point}', 0, (0,0,255))         # stocke l'affichage du score du joueur
            window.blit(Score,(300,20))             # affiche le score



            self.unit.show_ship()           # affiche le vaisseau
            self.unit.show_invader()        # affiche les envahisseurs
            self.unit.move_invader()        # déplace les envahisseurs

            for event in pygame.event.get():			
                if event.type==pygame.QUIT:             # ferme la fenêtre si le joueur appuit sur le bouton fermer
                    continuer=False
                    pygame.quit()
                    sys.exit(0)
                
                # traite les évènements du clavier
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key==K_RIGHT:
                        right = True
                    if event.key==K_LEFT:
                        left = True
                    if event.key==K_SPACE:
                        shot = True

                if event.type==KEYUP:
                    if event.key==K_RIGHT:
                        right = False
                    if event.key==K_LEFT:
                        left = False
                    if event.key==K_SPACE:
                        shot = False

            if right : self.unit.right_ship()       # déplace le vaisseau à droite
            if left : self.unit.left_ship()         # déplace le vaisseau à gauche
            if shot : self.unit.fire()              

            self.unit.verif_tir()
            
            self.unit.tir()             

            # fin de la partie
            if self.unit.game_stop():             
                pygame.mixer.stop()
                game_over=pygame.mixer.Sound('game_over.wav')
                game_over.play(0)
                while True:
                    end = Over.render('GAME OVER', 0, (0,0,255))
                    window.blit(end,(70,240))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                    pygame.display.update()

            pygame.display.update()
            mainclock.tick(60)
            


game=Space_invader()
game.jeu()


