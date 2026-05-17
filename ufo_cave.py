import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
FPS = 60

DISPLAY_SCALE = 1.5
DISPLAY_W = int(WIDTH * DISPLAY_SCALE)
DISPLAY_H = int(HEIGHT * DISPLAY_SCALE)

screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
canvas = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Cave Flyer - 2 Drivers!")
clock = pygame.time.Clock()

# Colors
BG_COLOR   = (10, 10, 30)
ROCK_COLOR = (30, 50, 35)
ROCK_EDGE  = (60, 180, 80)
SILVER     = (200, 210, 225)
GRAY       = (130, 140, 155)
DOME_COLOR = (160, 220, 255)
CYAN       = (0, 220, 255)
YELLOW     = (255, 225, 0)
ORANGE     = (255, 150, 30)
WHITE      = (255, 255, 255)
RED        = (255, 60, 60)

COL_W        = 8    # terrain column width in pixels
SCROLL_SPEED = 180  # pixels per second

# ---------------------------------------------------------------------------
# Pixel font  (5 wide × 7 tall, uppercase + digits + punctuation)
# Each tuple is 7 rows; each row is a 5-bit integer (MSB = left pixel).
# ---------------------------------------------------------------------------
_F = {
    ' ': (0,0,0,0,0,0,0),
    '!': (0b00100,0b00100,0b00100,0b00100,0b00000,0b00100,0b00000),
    ':': (0b00000,0b00100,0b00000,0b00000,0b00100,0b00000,0b00000),
    '-': (0b00000,0b00000,0b00000,0b11111,0b00000,0b00000,0b00000),
    '.': (0b00000,0b00000,0b00000,0b00000,0b00000,0b00110,0b00110),
    '/': (0b00001,0b00010,0b00100,0b00100,0b01000,0b10000,0b00000),
    '<': (0b00010,0b00100,0b01000,0b10000,0b01000,0b00100,0b00010),
    '>': (0b01000,0b00100,0b00010,0b00001,0b00010,0b00100,0b01000),
    '0': (0b01110,0b10001,0b10011,0b10101,0b11001,0b10001,0b01110),
    '1': (0b00100,0b01100,0b00100,0b00100,0b00100,0b00100,0b01110),
    '2': (0b01110,0b10001,0b00001,0b00110,0b01000,0b10000,0b11111),
    '3': (0b11111,0b00010,0b00100,0b00110,0b00001,0b10001,0b01110),
    '4': (0b00010,0b00110,0b01010,0b10010,0b11111,0b00010,0b00010),
    '5': (0b11111,0b10000,0b11110,0b00001,0b00001,0b10001,0b01110),
    '6': (0b00110,0b01000,0b10000,0b11110,0b10001,0b10001,0b01110),
    '7': (0b11111,0b00001,0b00010,0b00100,0b01000,0b01000,0b01000),
    '8': (0b01110,0b10001,0b10001,0b01110,0b10001,0b10001,0b01110),
    '9': (0b01110,0b10001,0b10001,0b01111,0b00001,0b00010,0b01100),
    'A': (0b01110,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001),
    'B': (0b11110,0b10001,0b10001,0b11110,0b10001,0b10001,0b11110),
    'C': (0b01110,0b10001,0b10000,0b10000,0b10000,0b10001,0b01110),
    'D': (0b11110,0b10001,0b10001,0b10001,0b10001,0b10001,0b11110),
    'E': (0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b11111),
    'F': (0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b10000),
    'G': (0b01110,0b10001,0b10000,0b10111,0b10001,0b10001,0b01111),
    'H': (0b10001,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001),
    'I': (0b01110,0b00100,0b00100,0b00100,0b00100,0b00100,0b01110),
    'J': (0b00111,0b00010,0b00010,0b00010,0b00010,0b10010,0b01100),
    'K': (0b10001,0b10010,0b10100,0b11000,0b10100,0b10010,0b10001),
    'L': (0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b11111),
    'M': (0b10001,0b11011,0b10101,0b10001,0b10001,0b10001,0b10001),
    'N': (0b10001,0b11001,0b10101,0b10011,0b10001,0b10001,0b10001),
    'O': (0b01110,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110),
    'P': (0b11110,0b10001,0b10001,0b11110,0b10000,0b10000,0b10000),
    'Q': (0b01110,0b10001,0b10001,0b10001,0b10101,0b10010,0b01101),
    'R': (0b11110,0b10001,0b10001,0b11110,0b10100,0b10010,0b10001),
    'S': (0b01111,0b10000,0b10000,0b01110,0b00001,0b00001,0b11110),
    'T': (0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100),
    'U': (0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110),
    'V': (0b10001,0b10001,0b10001,0b10001,0b10001,0b01010,0b00100),
    'W': (0b10001,0b10001,0b10001,0b10101,0b10101,0b11011,0b10001),
    'X': (0b10001,0b10001,0b01010,0b00100,0b01010,0b10001,0b10001),
    'Y': (0b10001,0b10001,0b01010,0b00100,0b00100,0b00100,0b00100),
    'Z': (0b11111,0b00001,0b00010,0b00100,0b01000,0b10000,0b11111),
}

CHAR_W = 5
CHAR_H = 7
CHAR_GAP = 1  # pixels between characters


def draw_text(surface, text, x, y, color, scale=2):
    cx = x
    for ch in text.upper():
        rows = _F.get(ch)
        if rows is None:
            cx += (CHAR_W + CHAR_GAP) * scale
            continue
        for ry, row in enumerate(rows):
            for rx in range(CHAR_W):
                if row & (0b10000 >> rx):
                    pygame.draw.rect(surface, color,
                                     (cx + rx * scale, y + ry * scale, scale, scale))
        cx += (CHAR_W + CHAR_GAP) * scale
    return cx - x  # total width drawn


def text_w(text, scale=2):
    return len(text) * (CHAR_W + CHAR_GAP) * scale


def draw_text_centered(surface, text, cx, y, color, scale=2):
    x = cx - text_w(text, scale) // 2
    draw_text(surface, text, x, y, color, scale)


# ---------------------------------------------------------------------------

class Terrain:
    def __init__(self):
        self.cols = []
        self.x_offset  = 0.0
        self.gap_center = float(HEIGHT // 2)
        self.gap_half   = 130

        # Directional drift state
        self.direction  = random.choice([-1, 1])
        self.angle_deg  = random.uniform(30, 60)
        self.col_count  = 0
        self.next_turn  = random.randint(20, 50)

        for _ in range(WIDTH // COL_W + 20):
            self._add_col()

    def _add_col(self):
        # Drift the tunnel center at the current angle (30-60° from horizontal)
        dy = self.direction * math.tan(math.radians(self.angle_deg)) * COL_W
        self.gap_center += dy

        # Extra bumpiness: medium-sized random jolts
        self.gap_center += random.gauss(0, 4)

        # Bounce off ceiling/floor margins
        margin = self.gap_half + 35
        if self.gap_center < margin:
            self.gap_center = margin
            self.direction  = 1
            self.angle_deg  = random.uniform(30, 60)
        elif self.gap_center > HEIGHT - margin:
            self.gap_center = HEIGHT - margin
            self.direction  = -1
            self.angle_deg  = random.uniform(30, 60)

        # Periodically flip direction and pick a new angle
        self.col_count += 1
        if self.col_count >= self.next_turn:
            self.col_count = 0
            self.next_turn = random.randint(15, 45)
            self.angle_deg = random.uniform(30, 60)
            if random.random() < 0.55:
                self.direction *= -1

        # Per-wall surface bumps for a rough cave texture
        gc = int(self.gap_center)
        gh = self.gap_half
        top_bump = random.randint(-7, 7)
        bot_bump = random.randint(-7, 7)
        self.cols.append((gc - gh + top_bump, gc + gh + bot_bump))

    def update(self, dt, difficulty):
        self.x_offset += SCROLL_SPEED * dt
        while self.x_offset >= COL_W:
            self.x_offset -= COL_W
            if self.cols:
                self.cols.pop(0)
            self.gap_half = max(55, int(130 - difficulty * 55))
            self._add_col()

    def walls_at(self, screen_x):
        col_idx = int((screen_x + self.x_offset) / COL_W)
        if 0 <= col_idx < len(self.cols):
            return self.cols[col_idx]
        return (0, HEIGHT)

    def draw(self, surface):
        for i, (top_y, bot_y) in enumerate(self.cols):
            x = i * COL_W - int(self.x_offset)
            if x + COL_W < 0 or x > WIDTH:
                continue
            if top_y > 0:
                pygame.draw.rect(surface, ROCK_COLOR, (x, 0, COL_W, top_y))
                pygame.draw.rect(surface, ROCK_EDGE,  (x, top_y - 4, COL_W, 5))
            if bot_y < HEIGHT:
                pygame.draw.rect(surface, ROCK_COLOR, (x, bot_y, COL_W, HEIGHT - bot_y))
                pygame.draw.rect(surface, ROCK_EDGE,  (x, bot_y - 1, COL_W, 5))


INVINCIBLE_SECS = 3.0
SHIELD_SECS     = 7.0
DIAMOND_INTERVAL = 10.0


class Diamond:
    R = 12  # half-size of diamond shape

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.collected = False
        self.anim = random.uniform(0, 360)

    def update(self, dt):
        self.x -= SCROLL_SPEED * dt
        self.anim = (self.anim + dt * 140) % 360

    def on_screen(self):
        return self.x > -30

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.R
        # Pulsing glow
        pulse = int(50 + 35 * math.sin(math.radians(self.anim)))
        gs = pygame.Surface((r * 5, r * 5), pygame.SRCALPHA)
        pygame.draw.ellipse(gs, (80, 200, 255, pulse), (0, 0, r * 5, r * 5))
        surface.blit(gs, (x - r * 2 - r // 2, y - r * 2 - r // 2))
        # Diamond facets (top lighter, bottom darker)
        top_pts = [(x, y - r), (x + r, y), (x - r, y)]
        bot_pts = [(x, y + r), (x + r, y), (x - r, y)]
        pygame.draw.polygon(surface, (160, 235, 255), top_pts)
        pygame.draw.polygon(surface, (40,  140, 220), bot_pts)
        pygame.draw.polygon(surface, WHITE, [(x, y-r),(x+r,y),(x,y+r),(x-r,y)], 2)
        # Sparkle
        if int(self.anim / 45) % 2 == 0:
            pygame.draw.line(surface, WHITE, (x, y - r - 5), (x, y - r - 1), 1)
            pygame.draw.line(surface, WHITE, (x - r - 5, y), (x - r - 1, y), 1)


class UFO:
    def __init__(self):
        self.x          = float(WIDTH // 3)
        self.y          = float(HEIGHT // 2)
        self.vx         = 0.0
        self.vy         = 0.0
        self.crashed    = False
        self.anim       = 0.0
        self.age        = 0.0   # seconds since spawn
        self.shield_time = 0.0  # seconds of diamond-shield remaining

    def update(self, dt, keys):
        if self.crashed:
            return
        accel = 1050.0
        damp  = 0.87
        if keys[pygame.K_q]:     self.vy -= accel * dt
        if keys[pygame.K_a]:     self.vy += accel * dt
        if keys[pygame.K_LEFT]:  self.vx -= accel * dt
        if keys[pygame.K_RIGHT]: self.vx += accel * dt
        self.vx *= damp
        self.vy *= damp
        top_speed = 660.0
        spd = math.hypot(self.vx, self.vy)
        if spd > top_speed:
            self.vx = self.vx / spd * top_speed
            self.vy = self.vy / spd * top_speed
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = max(45.0, min(WIDTH  - 45.0, self.x))
        self.y = max(30.0, min(HEIGHT - 20.0, self.y))
        self.anim        = (self.anim + dt * 200) % 360
        self.age        += dt
        self.shield_time = max(0.0, self.shield_time - dt)

    def invincible(self):
        return self.age < INVINCIBLE_SECS or self.shield_time > 0

    def check_collision(self, terrain):
        if self.crashed or self.invincible():
            return
        pts = [
            (self.x,       self.y - 28),
            (self.x - 14,  self.y - 20),
            (self.x + 14,  self.y - 20),
            (self.x - 38,  self.y - 2),
            (self.x + 38,  self.y - 2),
            (self.x,        self.y + 14),
            (self.x - 20,  self.y + 14),
            (self.x + 20,  self.y + 14),
        ]
        for px, py in pts:
            top, bot = terrain.walls_at(px)
            if py < top or py > bot:
                self.crashed = True
                return

    def draw(self, surface):
        # Blink during spawn invincibility (8 Hz) or shield (12 Hz)
        if self.shield_time > 0 and int(self.shield_time * 12) % 2 == 1:
            return
        if self.age < INVINCIBLE_SECS and self.shield_time <= 0 and int(self.age * 8) % 2 == 1:
            return
        x, y = int(self.x), int(self.y)
        # Shield ring
        if self.shield_time > 0:
            pulse = int(120 + 80 * math.sin(math.radians(self.anim * 2)))
            rs = pygame.Surface((110, 110), pygame.SRCALPHA)
            pygame.draw.ellipse(rs, (0, 200, 255, pulse), (0, 15, 110, 80))
            pygame.draw.ellipse(rs, (0, 200, 255, 200),   (0, 15, 110, 80), 2)
            surface.blit(rs, (x - 55, y - 55))
        if not self.crashed:
            # Tractor beam
            beam_pts = [(x-18,y+13),(x+18,y+13),(x+30,y+65),(x-30,y+65)]
            bs = pygame.Surface((70, 55), pygame.SRCALPHA)
            local = [(p[0]-(x-35), p[1]-(y+13)) for p in beam_pts]
            pygame.draw.polygon(bs, (255,255,120,38), local)
            surface.blit(bs, (x-35, y+13))
            # Glow
            alpha = int(55 + 35 * math.sin(math.radians(self.anim)))
            gs = pygame.Surface((110, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(gs, (*CYAN, alpha), (0, 10, 110, 40))
            surface.blit(gs, (x-55, y-20))
        # Saucer
        body_col = RED if self.crashed else SILVER
        pygame.draw.ellipse(surface, body_col, (x-38, y-9,  76, 26))
        pygame.draw.ellipse(surface, GRAY,     (x-38, y-9,  76, 26), 2)
        # Dome
        dome_col = (180,70,70) if self.crashed else DOME_COLOR
        pygame.draw.ellipse(surface, dome_col, (x-16, y-28, 32, 26))
        pygame.draw.ellipse(surface, CYAN,     (x-16, y-28, 32, 26), 1)
        # Lights
        cycle = int(self.anim / 67) % 3
        colors = [YELLOW, CYAN, ORANGE]
        for j, lx in enumerate([-20, 0, 20]):
            lc = RED if self.crashed else colors[(j + cycle) % 3]
            pygame.draw.circle(surface, lc, (x + lx, y + 13), 5)


class Game:
    def __init__(self):
        self.state = "start"
        self._init()

    def _init(self):
        self.terrain        = Terrain()
        self.ufo            = UFO()
        self.score          = 0.0
        self.time_alive     = 0.0
        self.diamonds       = []
        self.diamond_timer  = random.uniform(8, 12)

    def reset(self):
        self._init()
        self.state = "playing"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.state in ("start", "crashed"):
                self.reset()

    def update(self, dt):
        if self.state != "playing":
            return
        difficulty = min(1.0, self.time_alive / 90.0)
        keys = pygame.key.get_pressed()
        self.ufo.update(dt, keys)
        self.terrain.update(dt, difficulty)
        self.ufo.check_collision(self.terrain)
        if self.ufo.crashed:
            self.state = "crashed"
        else:
            self.time_alive += dt
            self.score      += dt

        # Diamonds
        for d in self.diamonds:
            d.update(dt)
        self.diamonds = [d for d in self.diamonds if d.on_screen() and not d.collected]

        for d in self.diamonds:
            if math.hypot(self.ufo.x - d.x, self.ufo.y - d.y) < 28:
                d.collected = True
                self.ufo.shield_time = SHIELD_SECS

        self.diamond_timer -= dt
        if self.diamond_timer <= 0:
            self.diamond_timer = random.uniform(8, 13)
            self._spawn_diamond()

    def _spawn_diamond(self):
        spawn_x = WIDTH + 50
        top, bot = self.terrain.walls_at(spawn_x)
        gap = bot - top
        if gap < 90:
            return  # too narrow, skip this one
        # Place near top or bottom wall, margin accounts for ±7 surface bumps
        margin = 42
        if random.random() < 0.5:
            y = top + margin
        else:
            y = bot - margin
        self.diamonds.append(Diamond(spawn_x, y))

    def draw(self):
        canvas.fill(BG_COLOR)

        if self.state in ("playing", "crashed"):
            self.terrain.draw(canvas)
            self.ufo.draw(canvas)
            for d in self.diamonds:
                d.draw(canvas)
            draw_text(canvas, f"Score: {int(self.score)}", 10, 10, YELLOW, 3)
            draw_text(canvas, "P1: Q up  A down",       WIDTH - text_w("P1: Q up  A down", 2) - 8, 8,  CYAN,   2)
            draw_text(canvas, "P2: < left  > right",    WIDTH - text_w("P2: < left  > right", 2) - 8, 26, ORANGE, 2)
            if self.ufo.shield_time > 0:
                draw_text(canvas, f"Shield: {self.ufo.shield_time:.1f}s", 10, HEIGHT - 30, CYAN, 2)

        if self.state == "start":
            self._draw_overlay()
            self._draw_start()
        elif self.state == "crashed":
            self._draw_overlay()
            self._draw_crashed()

        screen.blit(pygame.transform.scale(canvas, (DISPLAY_W, DISPLAY_H)), (0, 0))
        pygame.display.flip()

    def _draw_overlay(self):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 165))
        canvas.blit(ov, (0, 0))

    def _draw_start(self):
        draw_text_centered(canvas, "UFO CAVE FLYER", WIDTH//2, 90,  CYAN,   4)
        draw_text_centered(canvas, "Two pilots  one saucer  cooperate or crash", WIDTH//2, 180, WHITE,  2)
        draw_text_centered(canvas, "Driver 1:  Q up   A down",   WIDTH//2, 240, CYAN,   2)
        draw_text_centered(canvas, "Driver 2:  < left  > right", WIDTH//2, 270, ORANGE, 2)
        draw_text_centered(canvas, "Score rises every second.  One life.",  WIDTH//2, 330, WHITE,  2)
        draw_text_centered(canvas, "Press space to launch",      WIDTH//2, 410, YELLOW, 3)

    def _draw_crashed(self):
        draw_text_centered(canvas, "Crashed!",                    WIDTH//2, 150, RED,    5)
        draw_text_centered(canvas, f"Final score: {int(self.score)}", WIDTH//2, 270, YELLOW, 3)
        draw_text_centered(canvas, "Press space to try again",   WIDTH//2, 370, WHITE,  2)


def main():
    game = Game()
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        game.update(dt)
        game.draw()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
