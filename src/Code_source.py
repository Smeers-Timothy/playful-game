#encoding: utf-8
'''
 ============================================================================
 Name        : Code_source.py
 Author      : Timothy_Smeers
 Version     :
 Copyright   : Your copyright notice
 Description : Selon un calcul mathématique avec plusieurs solutions, faire atterir un boulet de canon dans le nuage contenant la solution mathématique exact.
 ============================================================================
'''
import math
import pygame
import random
import operator
from pygame.math import Vector2
            
# Initialisation de pygame
pygame.init()
            
# Initialisation de la fenetre
window = pygame.display.set_mode((640, 480))
            
# Initialisation de la police de caractère globale
FONT = pygame.font.Font(None, 24)
 
# Initialisation de la police de caractère du calcul
CALCUL_FONT = pygame.font.Font(None, 22)
            
# Initialisation de la couleur noir
BLACK = pygame.Color('black')
            
# Créé une surface du boulet de canon pygame dont le format de pixel comprendra un alpha par pixel
BULLET_IMAGE = pygame.Surface((20, 11), pygame.SRCALPHA)
            
# Créé le boulet de canon
pygame.draw.polygon(BULLET_IMAGE, pygame.Color('grey11'), [(0, 0), (20, 5), (0, 11)])
            
# Liste des opérateur 
operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul)]
      
# Ajoutez des boullets à ce groupe.
bullet_group = pygame.sprite.Group()
        
# Liste de position x des nuages
nuages_pos_y =  [(random.randint(60, 130)), (random.randint(200,220)), (random.randint(320, 400))]
                
# Liste des calculs
calcul = []

'le constructeur Bullet permettant de créé un boulet de canon'
class Bullet(pygame.sprite.Sprite):
          
    '''Le paramètre self représente l'objet cible, 
    C'est une variable qui contient une référence vers l'objet qui est en cours de création. 
    Grâce à ce dernier, on va pouvoir accéder aux attributs et fonctionnalités de l'objet cible.'''
    def __init__(self, pos, angle):
          
        # Acces à la classe mère
        super(Bullet, self).__init__()
                    
        # Permet que le boulet suive la même rotation que le canon
        self.image = pygame.transform.rotate(BULLET_IMAGE, -angle)
        self.rect = self.image.get_rect(center=pos)
                    
        # Pour appliquer un décalage à la position de départ,
        # Créer un autre vecteur et le faire pivoter également.
        offset = Vector2(40, 0).rotate(angle)
                    
        # Ajoutez le vecteur de décalage au vecteur de position.
        self.pos = Vector2(pos) + offset  # Centre du sprite.
                    
        # Faites pivoter le vecteur vitesse (9, 0) de l'angle.
        self.velocity = Vector2(9, 0).rotate(angle)
            
            
    'Fonction permettant l update du boullet de canon'
    def update(self):
          
        # Ajoutez de la vitesse à la position pour déplacer le sprite.
        self.pos += self.velocity
        self.rect.center = self.pos
      
      
'le constructeur Cloud permettant d afficher les nuages' 
class Cloud(pygame.sprite.Sprite):
     
    '''Le paramètre self représente l'objet cible, 
    C'est une variable qui contient une référence vers l'objet qui est en cours de création. 
    Grâce à ce dernier, on va pouvoir accéder aux attributs et fonctionnalités de l'objet cible.'''
    def __init__(self, x, y):
               
        # Acces à la classe mère
        super(Cloud, self).__init__()
         
        # Permet d'appeller les variable de calcul_number
        c = calcul_number()
         
        # Image du nuage
        self.image = pygame.image.load("images\cloud.png").convert_alpha(window)
         
        # Permet d'associer un rectangle à l'image
        self.rect = self.image.get_rect(center = (x, y))
         
        print("CLOUD    {} {} {} = {}".format(c.firstNumber, c.operator, c.secondNumber, c.resolve(c.firstNumber, c.secondNumber)))
         
        # Permet d'afficher une solution d'un calcul aléatoir dans l'image du nuage
        self.calcul = FONT.render(("{}".format(c.resolve(c.firstNumber, c.secondNumber))), True, BLACK)
        self.image.blit(self.calcul, [(self.image.get_width()/2 - self.calcul.get_width()/2) , self.image.get_height()/2])
         
         
'le constructeur Sun permettant d afficher le soleil '
class Sun(pygame.sprite.Sprite):
     
    '''Le paramètre self représente l'objet cible, 
    C'est une variable qui contient une référence vers l'objet qui est en cours de création. 
    Grâce à ce dernier, on va pouvoir accéder aux attributs et fonctionnalités de l'objet cible.'''
    def __init__(self):
               
        # Acces à la classe mère
        super(Sun, self).__init__()
         
        # Image du soleil
        self.image = pygame.image.load("images\sun.png").convert_alpha(window)
         
        # Permet d'associer un rectangle à l'image
        self.rect = self.image.get_rect(center = (320,120))
         
        # Le calcul aléatoirement choisi dans la liste de calcul
        mon_choix = random.choice(calcul)
         
        gen = (self.id for self.id, x in enumerate(calcul) if x == mon_choix)
        for self.id in gen: break
 
        # Permet d'afficher un calcul aléatoire dont la réponse se trouve dans un des nuages dans le soleil 
        self.calcul = CALCUL_FONT.render(mon_choix, True, BLACK)
        self.image.blit(self.calcul, [(self.image.get_width()/2 - self.calcul.get_width()/2) , 
                                      (self.image.get_height()/2 - self.calcul.get_height()/2)])
         
'Fonction permettant de retournée les variables de la class Sun '
def sun_var():
        return Sun()   
 

'le constructeur calcul_aleatoire permettant de construire un calcul aléatoire ' 
class Calcul_aleatoire:
     
     
    '''Le paramètre self représente l'objet cible, 
    C'est une variable qui contient une référence vers l'objet qui est en cours de création. 
    Grâce à ce dernier, on va pouvoir accéder aux attributs et fonctionnalités de l'objet cible.'''
    def __init__(self): 
         
        # Initialise des nombres aléatoire entre 1 et 50
        self.firstNumber = random.randint(1, 50)
        self.secondNumber = random.randint(1, 50)
         
        #Initialise un opérateur aléatoire 
        self.operator, self.resolve = random.choice(operators) 
         
        # Permet d'ajouter à la liste calcul, un calcul 
        calcul.append("{} {} {} = ?".format(self.firstNumber, self.operator, self.secondNumber, 
                                            self.resolve(self.firstNumber, self.secondNumber)))
        
         
'Fonction permettant de retournée les variables de la class Calcul_aleatoire '
def calcul_number():
        return Calcul_aleatoire()   
     
     
def getSpriteId(group):
    s_v = sun_var()
    valid_cloud = pygame.sprite.Group([group.sprites()[s_v.id]])
    return valid_cloud
 
 
'Fonction principale'
def main():
    

    'Focntion permettant la détection de collision entre deux groupe'
    def collision_test(first_group, second_group):
        gets_hit = pygame.sprite.groupcollide(first_group, second_group, True, True, collided = None)
        if gets_hit:
            return gets_hit
     
    # Initialisation du groupe de nuage à des position y aléatoire 
    cloud_group = pygame.sprite.Group([
        Cloud(80, nuages_pos_y[0]),
        Cloud(80, nuages_pos_y[1]),
        Cloud(80, nuages_pos_y[2]),
        Cloud(540, nuages_pos_y[0]),
        Cloud(540, nuages_pos_y[1]),
        Cloud(540, nuages_pos_y[2]),
    ])
     
    # Initialisation du groupe de soleil 
    sun_group = pygame.sprite.Group([Sun()])
                      
    # Créer un objet pour aider à suivre le temps
    clock = pygame.time.Clock()
       
    # Créé l'image du canon et rect dont Le format de pixel comprendra un alpha par pixel
    canon_img = pygame.Surface((60, 22), pygame.SRCALPHA)
    pygame.draw.rect(canon_img, pygame.Color('grey19'), [0, 0, 35, 22])
    pygame.draw.rect(canon_img, pygame.Color('grey19'), [35, 6, 35, 10])
                
    # Stockez l'image d'origine pour préserver la qualité.
    orig_canon_img = canon_img  
                
    # Le canon est centré au milieu de la page 
    canon = canon_img.get_rect(center=(320, 240))
                
    # L'angle est prédéfini sur 0
    angle = 0
            
    # Le score est défini sur 0
    score = 0
                
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            # Le bouton gauche tire une balle du centre du canon avec l' angle actuel.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Ajoutez le boullet au bullet_group.
                    bullet_group.add(Bullet(canon.center, angle))
                    break
                      
        # Mis à jour du group de boulet
        bullet_group.update()
                
        # Trouver l'angle de la cible (position de la souris).
        x, y = Vector2(pygame.mouse.get_pos()) - canon.center
        angle = math.degrees(math.atan2(y, x))
                    
        # Faites pivoter l'image du canon.
        canon_img = pygame.transform.rotate(orig_canon_img, -angle)
        canon = canon_img.get_rect(center=canon.center)
            
        # La couleur de fond de la fentre est "darkseagreen4"
        window.fill(pygame.Color('darkseagreen4'))
                    
        # Ajouter le dessin du groupe de boulet sur l'écran
        bullet_group.draw(window)
         
        # Ajouter le dessin du groupe de nuage sur l'écran
        cloud_group.draw(window)
         
        # Ajouter le dessin du groupe de soleil sur l'écran
        sun_group.draw(window)
                       
        # Dessine l'image du canon sur le canon
        window.blit(canon_img, canon)
                  
        # Initialisation de l'angle en degré sur la fenetre 
        # L'angle à été inversé de sorte à ce que le positif, soit situé sur la partie supérieur de la fenetre 
        txt = FONT.render('angle {:.1f}'.format(-angle), True, BLACK)
                    
        # Initialisation de mon propre nom
        myName = FONT.render('Smeers Timothy', True, BLACK)
                    
        # Initialisation de mon identifiant
        myIdent = FONT.render('S200930', True, BLACK)
                
        # Initialisation du score
        myScore = FONT.render('score :  {}'.format(score), True, BLACK)
                    
        # Affichage des zone de texte (txt, myName, myIdent) sur les position supérieur de la fenetre
        window.blit(txt, (10, 10))
        window.blit(myName,(514,10))
        window.blit(myIdent,(514,25))
        window.blit(myScore ,(285, 10))

        if collision_test(bullet_group, cloud_group):
            
            # Supprime la liste calcul
            del calcul[:]
             
            # Initialise le groupe de nuage à une nouvelle position et de nouveaux calcul
            cloud_group = pygame.sprite.Group([
                Cloud(80, random.randint(60, 130)),
                Cloud(80, random.randint(200,220)),
                Cloud(80, random.randint(320, 400)),
                Cloud(540, random.randint(60, 130)),
                Cloud(540,  random.randint(200,220)),
                Cloud(540, random.randint(320, 400)),
            ])
            
            # Initialise le groupe de soleil avec un nouveaux calcul
            sun_group= pygame.sprite.Group([Sun()])

            # Incrémente le score à chaque colisions 
            score  += 1
                
        # Afichage de la ligne de direction du canon 
        pygame.draw.line(window, pygame.Color(150, 60, 20),canon.center, pygame.mouse.get_pos(), 2)
                    
        # Mettre à jour des parties de l'écran pour les affichages logiciels
        pygame.display.update()
                
        # Signifie que pour chaque seconde, au plus 40 images doivent passer.
        clock.tick(40)          
      
if __name__ == '__main__':
    
    main()
    pygame.quit()