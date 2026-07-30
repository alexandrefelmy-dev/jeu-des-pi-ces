import pygame
import random

pygame.init()
ecran = pygame.display.set_mode((800, 600))
horloge = pygame.time.Clock()

# Variables de jeu
joueur_x = 400
joueur_y = 300
vitesse_joueur = 6
niveau = 1
alpha = 0
liste_malus = []

piece_x = random.randint(15, 785)
piece_y = random.randint(15, 585)

score = 0
temps = 30
compteur_image = 0
etat = "menu"

# Liste pour stocker tous nos bots
liste_bots = []
vitesse_bot = 1

# Chargement du meilleur record
try:
    with open("record.txt", "r") as fichier:
        meilleur_score = int(fichier.read())
except:
    meilleur_score = 0

ma_police = pygame.font.SysFont("yugothicuisemibold", 36)

continuer = True
while continuer:
    horloge.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    # --- ÉTRAN MENU ---
    if etat == "menu":
        ecran.fill((0, 0, 0))
        text_start = "appuyez sur espace pour jouer"
        image_start = ma_police.render(text_start, False, (255, 255, 255))
        ecran.blit(image_start, (100, 250))

        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE]:
            # --- INITIALISATION DU NIVEAU (Exécuté UNE SEULE FOIS) ---
            score = 0
            temps = 30
            joueur_x = 400
            joueur_y = 300

            # On vide la liste puis on génère les bots selon le niveau
            liste_bots.clear()
            for i in range(niveau):
                bx = random.randint(15, 785)
                by = random.randint(15, 150)
                liste_bots.append(pygame.Rect(bx, by, 20, 20))

            etat = "jeu"



    # --- ÉCRAN JEU ---
    if etat == "jeu":
        # Déplacements Joueur
        touches = pygame.key.get_pressed()
        if touches[pygame.K_q]: joueur_x -= vitesse_joueur
        if touches[pygame.K_d]: joueur_x += vitesse_joueur
        if touches[pygame.K_z]: joueur_y -= vitesse_joueur
        if touches[pygame.K_s]: joueur_y += vitesse_joueur

        # Limites Écran
        if joueur_x < 0: joueur_x = 0
        if joueur_x > 750: joueur_x = 750
        if joueur_y < 0: joueur_y = 0
        if joueur_y > 550: joueur_y = 550

        rectjoueur = pygame.Rect(joueur_x, joueur_y, 50, 50)
        rectpiece = pygame.Rect(piece_x - 15, piece_y - 15, 30, 30)

        # Collision avec la pièce
        if rectjoueur.colliderect(rectpiece):
            piece_x = random.randint(15, 785)
            piece_y = random.randint(15, 585)
            score += 1

        # Gestion du Temps
        compteur_image += 1
        if compteur_image == 60:
            compteur_image = 0
            temps -= 1

        if score >= 10:
            etat = "niveau_reussi"
        elif temps <= 0:
            etat = "endgame"

            if niveau > meilleur_score:
                meilleur_score = niveau
                with open("record.txt", "w") as fichier:
                    fichier.write(str(meilleur_score))

        # Rendu Graphique
        ecran.fill((0, 0, 0))

        # 1. Dessiner le joueur et la pièce
        pygame.draw.rect(ecran, (255, 0, 0), rectjoueur)
        pygame.draw.circle(ecran, (150, 0, 255), (piece_x, piece_y), 15)

        # 2. BOUCLE SUR TOUS LES BOTS (Déplacement + Collision + Dessin)
        for bot in liste_bots:
            # IA : Le bot suit le joueur
            if bot.x < joueur_x: bot.x += vitesse_bot
            if bot.x > joueur_x: bot.x -= vitesse_bot
            if bot.y < joueur_y: bot.y += vitesse_bot
            if bot.y > joueur_y: bot.y -= vitesse_bot

            # Collision du joueur avec CE bot
            if rectjoueur.colliderect(bot):
                bot.x = random.randint(15, 785)
                bot.y = random.randint(15, 585)
                score -= 1

            # Dessin de CE bot
            pygame.draw.rect(ecran, (0, 0, 255), bot)
            
        for malus in liste_malus : 
            if rectjoueur.colliderect(bot):
                malus.x = random.randint(15, 785)
                malus.y = random.randint(15, 585)
                
                pygame.draw.rect(ecran, (255, 0, 0), bot)
            

        # 3. Affichage Score & Temps
        image_score = ma_police.render(f"Score : {score}", False, (255, 255, 255))
        image_temps = ma_police.render(str(temps), False, (255, 0, 0))

        ecran.blit(image_score, (10, 10))
        ecran.blit(image_temps, (700, 10))




    if etat == "niveau_reussi" :

        text_niveau_suivant = f"niveau suivant : {niveau + 1}"
        image_niveau_suivant = ma_police.render(text_niveau_suivant, False, (255, 215, 0))
        ecran.blit(image_niveau_suivant, (100, 300))

        voile_noir = pygame.Surface((800, 600))
        voile_noir.fill((0, 0, 0))

        alpha += 5

        voile_noir.set_alpha(alpha)
        ecran.blit(voile_noir, (0, 0))  # On le colle en haut à gauche

        if alpha > 255:
            alpha = 255
            niveau = niveau + 1
            vitesse_bot = min(3, 1 + (niveau * 0.3))
            
            temps = 30
            score = 0
            joueur_x = 400
            joueur_y = 300

            liste_bots.clear()
            for i in range (niveau) :
                bx = random.randint(15, 785)
                by = random.randint(15, 150)
                liste_bots.append(pygame.Rect(bx, by, 20, 20))

            alpha = 0
            etat = "jeu"





    # --- ÉCRAN ENDGAME ---
    if etat == "endgame":
        ecran.fill((0, 0, 0))

        text_record = f"Meilleur record : {meilleur_score}"
        image_record = ma_police.render(text_record, False, (255, 215, 0))
        ecran.blit(image_record, (100, 300))

        text_endgame = f"Your score : {score}"
        image_endgame = ma_police.render(text_endgame, False, (255, 255, 255))
        ecran.blit(image_endgame, (100, 250))

        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE]:
            # Relancer la partie
            score = 0
            temps = 30
            joueur_x = 400
            joueur_y = 300
            niveau = 1
            vitesse_bot = 1

            liste_bots.clear()
            for i in range(niveau):
                bx = random.randint(15, 785)
                by = random.randint(15, 150)
                liste_bots.append(pygame.Rect(bx, by, 20, 20))

            etat = "jeu"


    pygame.display.update()

pygame.quit()
