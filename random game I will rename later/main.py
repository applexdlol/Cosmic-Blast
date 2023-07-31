import math
import pygame
import sys
import time
import random
import csv
import hashlib
import base64
import threading

pygame.init()

icon = pygame.image.load('extras/icon.png')
pygame.display.set_icon(icon)
game_is_running = True


WIDTH, HEIGHT = 1200, 650 #the game screen

FPS = 60
TITLE = "Beta Cosmic Blast v3"
CREATOR = "created by: applexdlol"
PLAYER_RADIUS = 25
BULLET_RADIUS = 5
BULLET_SPEED = 12
PLAYER_SPEED = 7
BULLET_COOLDOWN = 0.25
ENEMY_RADIUS = 25
ENEMY_SPEED = 1.25
ENEMY_DIRECTION_CHANGE_CHANCE = 0.01  
MISSILE_RADIUS = 5
MISSILE_SPEED = 2.5 
MISSILE_LAUNCH_CHANCE = 0.01
BOSS_SHIP_RADIUS = 50
BOSS_SHIP_SPEED = 1
BOSS_DIRECTION_CHANGE_CHANCE = 0.01
FOLLOW_MISSILE_SPEED = 1.5
FOLLOW_MISSILE_RADIUS = 5
FOLLOW_MISSILE_SPEED = MISSILE_SPEED * 0.8


BOSS_SHIP = pygame.image.load('extras/BOSS MAN.png')
BACKGROUND_IMAGE = pygame.image.load('extras/better space bg2.jpg')
PLAYER_IMAGE = pygame.image.load('extras/bluespaceship.png')
ENEMY_IMAGE = pygame.image.load('extras/redspaceship69.png')
BULLET_IMAGE = pygame.image.load('extras/laserblue.png')
MISSILE_IMAGE = pygame.image.load('extras/missile.png')
FOLLOW_MISSILE_IMAGE = pygame.image.load('extras/following missile.png')

#HEART = pygame.image.load('extras/heart emoji.png')
#HEART = pygame.transform.scale(HEART, (20, 20))
EXPLOSION_FRAMES = [pygame.image.load(f'explosion/{i}.gif') for i in range(26)]


#important
SECRET_KEY = "fer92cB49Q7dk9DWKGbLZAhd1QQapvjW"
SECRET_KEY2 = "xtGWMtBGubcF7mjzh9PpekCKm21ja09x"
SECRET_KEY3 = "sIdnssmIdmslvnUsimxlzIqwErktlqkE"


BACKGROUND_IMAGE_transformed = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
PLAYER_IMAGE_transformed = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
ENEMY_IMAGE_transformed = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_RADIUS * 2, ENEMY_RADIUS * 2))
BULLET_IMAGE_transformed = pygame.transform.scale(BULLET_IMAGE, (BULLET_RADIUS * 3, BULLET_RADIUS * 3))
MISSILE_IMAGE_transformed = pygame.transform.scale(MISSILE_IMAGE, (MISSILE_RADIUS * 5, MISSILE_RADIUS * 5))
BOSS_SHIP_transformed = pygame.transform.scale(BOSS_SHIP, (BOSS_SHIP_RADIUS * 2, BOSS_SHIP_RADIUS * 2))
FOLLOW_MISSILE_IMAGE_transformed = pygame.transform.scale(FOLLOW_MISSILE_IMAGE, (MISSILE_RADIUS * 5, MISSILE_RADIUS * 5))

high_score = 0.0
high_kills = 0 
high_boss = 0


def write_fake_hash():
    fake_secret_key = "fer92cB49Q7dk9DWKGbLZAhd1QQapvjW"
    while True:
        with open('extras/game.csv', 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            
        if num_lines < 24:
            fake_high_score = round(random.uniform(100, 10000), 5)
            fake_high_kills = random.randint(1, 100)
            fake_high_boss = random.randint(1, 50)

            encoded_score = base64.b64encode(str(fake_high_score).encode()).decode()
            encoded_kills = base64.b64encode(str(fake_high_kills).encode()).decode()
            encoded_boss = base64.b64encode(str(fake_high_boss).encode()).decode()

            fake_hashed_score = hashlib.sha256((encoded_score + fake_secret_key).encode()).hexdigest()
            fake_hashed_kills = hashlib.sha256((encoded_kills + fake_secret_key).encode()).hexdigest()
            fake_hashed_boss = hashlib.sha256((encoded_boss + fake_secret_key).encode()).hexdigest()

            with open('extras/game.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([encoded_score, fake_hashed_score])
                writer.writerow([encoded_kills, fake_hashed_kills])
                writer.writerow([encoded_boss, fake_hashed_boss])
                
        elif num_lines > 24:
            with open('extras/game.csv', 'w', newline='') as file:
                file.writelines(lines[:24])

        elif num_lines == 24:
            fake_high_score = round(random.uniform(100, 10000), 5)
            fake_high_kills = random.randint(1, 100)
            fake_high_boss = random.randint(1, 50)

            encoded_score = base64.b64encode(str(fake_high_score).encode()).decode()
            encoded_kills = base64.b64encode(str(fake_high_kills).encode()).decode()
            encoded_boss = base64.b64encode(str(fake_high_boss).encode()).decode()

            fake_hashed_score = hashlib.sha256((encoded_score + fake_secret_key).encode()).hexdigest()
            fake_hashed_kills = hashlib.sha256((encoded_kills + fake_secret_key).encode()).hexdigest()
            fake_hashed_boss = hashlib.sha256((encoded_boss + fake_secret_key).encode()).hexdigest()

            new_lines = [','.join([encoded_score, fake_hashed_score]), ','.join([encoded_kills, fake_hashed_kills]), ','.join([encoded_boss, fake_hashed_boss])]

            with open('extras/game.csv', 'w', newline='') as file:
                file.writelines(lines[:3] + new_lines + lines[6:])
        
        time.sleep(1)



def save_high_score(score, ship_kills, boss_kills):
    global high_score
    global high_kills
    global high_boss
    if score > high_score:
        high_score = score
    if ship_kills > high_kills:
        high_kills = ship_kills
    if boss_kills > high_boss:
        high_boss = boss_kills
    with open('extras/game.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        encoded_score = base64.b64encode(str(high_score).encode()).decode()
        encoded_kills = base64.b64encode(str(high_kills).encode()).decode()
        encoded_boss = base64.b64encode(str(high_boss).encode()).decode()
        hashed_score = hashlib.sha256((encoded_score + SECRET_KEY).encode()).hexdigest()
        hashed_kills = hashlib.sha256((encoded_kills + SECRET_KEY2).encode()).hexdigest()
        hashed_boss = hashlib.sha256((encoded_boss + SECRET_KEY3).encode()).hexdigest()
        writer.writerow([encoded_score, hashed_score])
        writer.writerow([encoded_kills, hashed_kills]) 
        writer.writerow([encoded_boss, hashed_boss])

def load_high_score():
    global high_score
    global high_kills
    global high_boss
    try:
        with open('extras/game.csv', 'r') as file:
            reader = csv.reader(file)
            scores = list(reader)
            if len(scores) < 3:
                print("Not enough lines in the high score file, resetting scores...")
                high_score = 0
                high_kills = 0
                high_boss = 0
                return
            try:
                encoded_score, hashed_score = scores[0][0], scores[0][1]
                encoded_kills, hashed_kills = scores[1][0], scores[1][1]
                encoded_boss, hashed_boss = scores[2][0], scores[2][1]
                score = float(base64.b64decode(encoded_score.encode()).decode())
                ship_kills = int(base64.b64decode(encoded_kills.encode()).decode())
                boss_kills = int(base64.b64decode(encoded_boss.encode()).decode())
            except ValueError:
                print("Error decoding values, resetting scores...")
                high_score = 0
                high_kills = 0
                high_boss = 0
                return
            if hashlib.sha256((str(encoded_score) + SECRET_KEY).encode()).hexdigest() != hashed_score or \
               hashlib.sha256((str(encoded_kills) + SECRET_KEY2).encode()).hexdigest() != hashed_kills or \
               hashlib.sha256((str(encoded_boss) + SECRET_KEY3).encode()).hexdigest() != hashed_boss:
                print("High score file has been tampered with!")
                high_score = 0
                high_kills = 0
                high_boss = 0
                cheater_screen()
                return
            else:
                high_score = score
                high_kills = ship_kills
                high_boss = boss_kills
    except FileNotFoundError:
        print("High score file not found, resetting scores...")
        high_score = 0
        high_kills = 0
        high_boss = 0


#ANTI CHEAT SYSTEM
def cheater_screen():
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.Font(None, 32)

    lines = [
        "CHEATER! YOU TAMPERED WITH THE HIGHSCORE FILE!!!",
        "YOUR HIGH SCORE HAS BEEN REVERTED BACK TO 0",
        "SPRITELOL PRO ANTI CHEAT!"
    ]
    texts = [font.render(line, True, (255, 0, 0)) for line in lines]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))

        for i, text in enumerate(texts):
            screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2 + i * 40))

        pygame.display.flip()



#typing animation stuff both of those functions
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font('extras/Roboto-Black.ttf', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def typing_text(surface, text, size, x, y):
    delay = 50
    size = int(size * 0.4)
    font = pygame.font.Font('extras/Roboto-Black.ttf', size)
    display_text = ""
    for character in text:
        display_text += character
        text_surface = font.render(display_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        pygame.draw.rect(surface, (0, 0, 0), text_rect)
        surface.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(delay)
    pygame.time.wait(200)



#main menu or starting screen
def main_menu():
    background = pygame.image.load('extras/better space bg2.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    is_text_typed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not is_text_typed:
            typing_text(screen, TITLE, 100, WIDTH / 2, HEIGHT / 4)
            typing_text(screen, CREATOR, 60, WIDTH / 2, HEIGHT / 3 + 50)
            typing_text(screen, "PRESS   S   TO START", 36, WIDTH / 2, HEIGHT / 2 + 50)
            is_text_typed = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            main()
            

def rotate_image(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def rotate_following_missile(missile, angle):
    orig_rect = missile.get_rect()
    rot_missile = pygame.transform.rotate(missile, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_missile.get_rect().center
    rot_missile = rot_missile.subsurface(rot_rect).copy()
    return rot_missile

def get_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    rads = math.atan2(-dy,dx)
    rads %= 2*math.pi
    return math.degrees(rads)


def main():
    explosions = []
    LIVES = 1
    dead_bosses = []
    player_pos = [WIDTH / 2, HEIGHT - PLAYER_RADIUS]
    bullets = []
    bullet_last_shot_time = 0
    bullet_kills = 0
    enemies = [[WIDTH / 2, ENEMY_RADIUS, ENEMY_SPEED]]
    enemies_to_spawn = []  
    missiles = []
    following_missiles = []  # New line: add a list to store the following missiles
    ship_kills = 0 
    game_start_time = time.time() 
    last_enemy_spawn_time = game_start_time
    running = True
    game_over = False
    game_over_reason = ""
    DROP_MISSILE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(DROP_MISSILE_EVENT, random.randint(1000, 1200))
    shake_duration = 0  
    BOSS_HEALTH = 5
    bosses = [[random.uniform(BOSS_SHIP_RADIUS, WIDTH - BOSS_SHIP_RADIUS), BOSS_SHIP_RADIUS, BOSS_SHIP_SPEED, time.time(), BOSS_HEALTH, time.time()]]
    boss_spawn_time = time.time()
    boss_death_time = None
    boss_kills = 0
    boss_death_times = []
    boss_spawn_times = []
    boss_spawn_times.append(time.time() + 60)
    MAX_LIVES = 10
    MANA = 100
    last_attempted_shoot_time = -3
    bullet_pierce = 1
    boss_health_increase_time = time.time()
    pierce_increase_time = time.time()
    TURN_RATE = 0.05
    
    while running:

        mouse_pos = pygame.mouse.get_pos()
        angle = get_angle(mouse_pos, player_pos)
        player_image_rotated = rotate_image(PLAYER_IMAGE_transformed, angle + 90)

        dx, dy = mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
        vec_len = math.hypot(dx, dy)
        if vec_len > 0:
            dx, dy = dx / vec_len, dy / vec_len

        dt = clock.tick(FPS) / 1000
        if time.time() - boss_health_increase_time > 180:
            BOSS_HEALTH += 1
            boss_health_increase_time = time.time() 
        if time.time() - pierce_increase_time > 300: 
            bullet_pierce += 1
            pierce_increase_time = time.time()

        if time.time() - last_attempted_shoot_time > 3 and MANA < 100:
            MANA += 20 * dt
            MANA = min(100, MANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == DROP_MISSILE_EVENT:
                for enemy in enemies:
                    missiles.append([enemy[0], enemy[1], random.uniform(0.2, 0.6)])

        for death_time in boss_death_times[:]:
            if time.time() - death_time >= 10:
                bosses.append([random.uniform(BOSS_SHIP_RADIUS, WIDTH - BOSS_SHIP_RADIUS), BOSS_SHIP_RADIUS, BOSS_SHIP_SPEED, time.time(), BOSS_HEALTH, time.time()])
                boss_death_times.remove(death_time)

        for spawn_time in boss_spawn_times[:]:
            if time.time() >= spawn_time:
                bosses.append([random.uniform(BOSS_SHIP_RADIUS, WIDTH - BOSS_SHIP_RADIUS), BOSS_SHIP_RADIUS, BOSS_SHIP_SPEED, time.time(), BOSS_HEALTH, time.time()])
                boss_spawn_times.remove(spawn_time) 

        for spawn in enemies_to_spawn[:]:  
            if time.time() >= spawn[0]:  
                enemies.append(spawn[1:]) 
                enemies_to_spawn.remove(spawn)  

        if not game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                last_attempted_shoot_time = time.time()
                if time.time() - bullet_last_shot_time >= BULLET_COOLDOWN and MANA > 0:
                    bullets.append([player_pos[0], player_pos[1], dx, dy])
                    bullet_last_shot_time = time.time()
                    MANA -= 1
 

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_pos[0] -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_pos[0] += PLAYER_SPEED
            player_pos[0] = max(PLAYER_RADIUS, min(player_pos[0], WIDTH - PLAYER_RADIUS))

            for bullet in bullets[:]:
                bullet[0] += bullet[2] * BULLET_SPEED
                bullet[1] += bullet[3] * BULLET_SPEED
                if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                    bullets.remove(bullet)

            for enemy in enemies:
                if random.random() < ENEMY_DIRECTION_CHANGE_CHANCE:
                    enemy[2] = -enemy[2]
                enemy[0] += enemy[2]
                if enemy[0] - ENEMY_RADIUS < 0 or enemy[0] + ENEMY_RADIUS > WIDTH:
                    enemy[2] = -enemy[2]    
                if time.time() - last_enemy_spawn_time > 15:
                    last_enemy_spawn_time = time.time()
                    spawn_time = time.time() + 3
                    enemies_to_spawn.append([spawn_time, random.uniform(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS), ENEMY_RADIUS, ENEMY_SPEED])
                if random.random() < MISSILE_LAUNCH_CHANCE:
                    missiles.append([enemy[0], enemy[1], MISSILE_SPEED])

            for boss in bosses:
                if player_pos[0] > boss[0]:
                    boss[0] += boss[2]
                else:
                    boss[0] -= boss[2]
                if time.time() - boss[3] > random.uniform(1, 1.7):
                    boss[3] = time.time()
                    missiles.append([boss[0], boss[1], MISSILE_SPEED])
                    following_missiles.append([boss[0], boss[1], FOLLOW_MISSILE_SPEED])

            for missile in missiles:
                missile[1] += MISSILE_SPEED
                if missile[1] > HEIGHT:
                    missiles.remove(missile)
                elif (missile[0] - player_pos[0])**2 + (missile[1] - player_pos[1])**2 < (MISSILE_RADIUS + PLAYER_RADIUS)**2:
                    LIVES -= 1
                    missiles.remove(missile)
                    missiles.clear()
                    following_missiles.clear()
                    shake_duration = 0.5  
                    if LIVES == 0:
                        game_over = True
                        game_over_reason = "You ran out of lives you were hit by a missile :("
                        break

            # New: handle collision between following missiles and player
            for missile in following_missiles[:]:
                if (missile[0] - player_pos[0])**2 + (missile[1] - player_pos[1])**2 < (FOLLOW_MISSILE_RADIUS + PLAYER_RADIUS)**2:
                    LIVES -= 1
                    following_missiles.remove(missile)
                    following_missiles.clear()
                    shake_duration = 0.5  # add screen shake effect here
                    if LIVES == 0:
                        game_over = True
                        game_over_reason = "You ran out of lives you were hit by a following missile :("
                        break


            # New: update positions of following missiles
                        # Update positions of following missiles
            for missile in following_missiles:
                dx, dy = player_pos[0] - missile[0], player_pos[1] - missile[1]
                vec_len = math.hypot(dx, dy)
                if vec_len > 0:
                    dx, dy = dx / vec_len, dy / vec_len
                missile[0] += dx * FOLLOW_MISSILE_SPEED
                missile[1] += dy * FOLLOW_MISSILE_SPEED
                if missile[0] < 0 or missile[0] > WIDTH or missile[1] < 0 or missile[1] > HEIGHT:
                    following_missiles.remove(missile)

            # Draw following missiles
            for missile in following_missiles:
                dx, dy = player_pos[0] - missile[0], player_pos[1] - missile[1]
                angle = get_angle(missile[:2], player_pos)
                missile_image_rotated = rotate_following_missile(FOLLOW_MISSILE_IMAGE_transformed, angle + 90)
                screen.blit(missile_image_rotated, (int(missile[0] - FOLLOW_MISSILE_RADIUS + shake_offset_x), int(missile[1] - FOLLOW_MISSILE_RADIUS + shake_offset_y)))




            for bullet in bullets:
                pierces_left = bullet_pierce
                for missile in missiles[:]:
                    if (missile[0] - bullet[0])**2 + (missile[1] - bullet[1])**2 < (MISSILE_RADIUS + BULLET_RADIUS)**2:
                        missiles.remove(missile)
                        bullet_kills += 1
                        pierces_left -= 1
                        if pierces_left <= 0:
                            bullets.remove(bullet)
                            break

            for bullet in bullets:
                pierces_left = bullet_pierce
                for missile in following_missiles[:]:  # iterate over following missiles
                    if (missile[0] - bullet[0])**2 + (missile[1] - bullet[1])**2 < (FOLLOW_MISSILE_RADIUS + BULLET_RADIUS)**2:
                        following_missiles.remove(missile)  # remove the hit following missile
                        bullet_kills += 1
                        pierces_left -= 1
                        if pierces_left <= 0:
                            bullets.remove(bullet)
                            break

            for bullet in bullets[:]:  
                pierces_left = bullet_pierce
                for enemy in enemies[:]:
                    if (enemy[0] - bullet[0])**2 + (enemy[1] - bullet[1])**2 < (ENEMY_RADIUS + BULLET_RADIUS)**2:
                        enemies.remove(enemy)
                        ship_kills += 1
                        spawn_time = time.time() + 3
                        enemies_to_spawn.append([spawn_time, random.uniform(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS), ENEMY_RADIUS, ENEMY_SPEED])
                        explosions.append({
                            'frame': 0, 
                            'pos': enemy[:2],
                            'end_time': time.time() + 0.5
                        })
                        pierces_left -= 1
                        if pierces_left <= 0:
                            bullets.remove(bullet)
                            break

            for bullet in bullets:
                try:
                    for boss in bosses[:]:
                        if (boss[0] - bullet[0])**2 + (boss[1] - bullet[1])**2 < (BOSS_SHIP_RADIUS + BULLET_RADIUS)**2:
                            boss[4] -= 1
                            bullets.remove(bullet)
                            if boss[4] <= 0:
                                bosses.remove(boss)
                                boss_kills += 1
                                if LIVES < MAX_LIVES:
                                    LIVES += 1
                                explosions.append({
                                    'frame': 0,
                                    'pos': boss[:2],
                                    'end_time': time.time() + 0.5
                                })
                                boss_death_time = time.time()
                                dead_bosses.append([boss[0], boss[1], boss[2], boss[3], boss[4], boss_death_time])
                                break
                except ValueError:
                    pass

            if boss_death_time is not None and time.time() - boss_death_time >= 10:
                boss_death_time = None
                bosses.append([random.uniform(BOSS_SHIP_RADIUS, WIDTH - BOSS_SHIP_RADIUS), BOSS_SHIP_RADIUS, BOSS_SHIP_SPEED, time.time(), BOSS_HEALTH])

        if shake_duration > 0:
            shake_amount = int(shake_duration * 20)  
            shake_offset_x = random.randint(-shake_amount, shake_amount)
            shake_offset_y = random.randint(-shake_amount, shake_amount)
            shake_duration -= dt
        else:
            shake_offset_x = 0
            shake_offset_y = 0

        screen.blit(BACKGROUND_IMAGE_transformed, (0 + shake_offset_x, 0 + shake_offset_y))
        screen.blit(player_image_rotated, (player_pos[0] - player_image_rotated.get_width() // 2 + shake_offset_x, player_pos[1] - player_image_rotated.get_height() // 2 + shake_offset_y))


        for bullet in bullets:
            screen.blit(BULLET_IMAGE_transformed, (int(bullet[0] - BULLET_RADIUS + shake_offset_x), int(bullet[1] - BULLET_RADIUS + shake_offset_y)))

        for missile in missiles:
            screen.blit(MISSILE_IMAGE_transformed, (int(missile[0] - MISSILE_RADIUS + shake_offset_x), int(missile[1] - MISSILE_RADIUS + shake_offset_y)))

        for enemy in enemies:
            screen.blit(ENEMY_IMAGE_transformed, (enemy[0] - ENEMY_IMAGE_transformed.get_width() // 2 + shake_offset_x, enemy[1] - ENEMY_IMAGE_transformed.get_height() // 2 + shake_offset_y))

        for boss in bosses:
            screen.blit(BOSS_SHIP_transformed, (boss[0] - BOSS_SHIP_transformed.get_width() // 2 + shake_offset_x, boss[1] - BOSS_SHIP_transformed.get_height() // 2 + shake_offset_y))


        for missile in following_missiles:
                screen.blit(FOLLOW_MISSILE_IMAGE_transformed, (int(missile[0] - FOLLOW_MISSILE_RADIUS + shake_offset_x), int(missile[1] - FOLLOW_MISSILE_RADIUS + shake_offset_y)))
        for explosion in explosions[:]:
            frame_image = EXPLOSION_FRAMES[explosion['frame']]
            frame_image_transformed = pygame.transform.scale(frame_image, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
            screen.blit(frame_image_transformed, (explosion['pos'][0] - frame_image_transformed.get_width() // 2 + shake_offset_x, explosion['pos'][1] - frame_image_transformed.get_height() // 2 + shake_offset_y))
            explosion['frame'] += 1
            if explosion['frame'] >= len(EXPLOSION_FRAMES) or time.time() > explosion['end_time']:
                explosions.remove(explosion)

        survival_time = time.time() - game_start_time if not game_over else survival_time
        left_margin = 60 

        draw_text(screen, f"Survival Time: {survival_time:.2f}s", 12, WIDTH / 2, 10)
        draw_text(screen, f"High Score: {high_score:.2f}s", 12, WIDTH - 100, 10)
        draw_text(screen, f"Highest Kill Count: {high_kills}", 12, WIDTH - 100, 30)
        draw_text(screen, f"Most Bosses Killed: {high_boss}", 12, WIDTH -100, 50)
        draw_text(screen, f"Enemies: {len(enemies)}", 12, left_margin, 10)
        draw_text(screen, f"Kills: {ship_kills}", 12, left_margin, 30)
        draw_text(screen, f"Enemy Missiles: {len(missiles)}", 12, left_margin, 50)
        draw_text(screen, f"Bosses: {len(bosses)}", 12, left_margin, 70)
        draw_text(screen, f"Bosses Killed: {boss_kills}", 12, left_margin, 90)
        draw_text(screen, f"Lives: {LIVES}", 12, left_margin, 110)
        draw_text(screen, f"Mana: {int(MANA)}%", 12, left_margin, 130)
        draw_text(screen, f"Bullet Pierce: {bullet_pierce}", 12, left_margin, 150)
        #draw_text(screen, f"FPS {int(FPS)}", 12, left_margin, 170)

        if game_over:
            draw_text(screen, "GAME OVER", 40, WIDTH / 2, HEIGHT / 2 - 25)
            draw_text(screen, game_over_reason, 30, WIDTH / 2, HEIGHT / 2 + 10)
            draw_text(screen, f"Survival Time: {survival_time:.2f}s", 30, WIDTH / 2, HEIGHT / 2 + 50)
            draw_text(screen, "Press  R  to Restart", 30, WIDTH / 2, HEIGHT / 2 + 105)
            draw_text(screen, "Press  M  to go to the Main Menu", 30, WIDTH / 2, HEIGHT / 2 + 150)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
            if keys[pygame.K_m]:
                main_menu()

        if survival_time > high_score or ship_kills > high_kills or boss_kills > high_boss:
            save_high_score(survival_time, ship_kills, boss_kills) 

        pygame.display.flip()
        clock.tick(FPS)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
load_high_score()
threading.Thread(target=write_fake_hash).start()
main_menu()
