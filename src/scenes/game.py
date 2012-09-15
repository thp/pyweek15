
from engine.scene import Scene
from logic.level import Level
from logic.player import Player
from logic.enemy import Enemy

from logic.lamemath import shade_color

from pygame.locals import *

WORLD_DEPTH = 10 # fudge factor... works for self.DEPTH @ 15


# XXX: This should be removed once we have proper gfx
colors = {
    #'coin': (255, 255, 0),
    'stone': (0, 0, 255),
    'lanternfish': (0, 255, 0),
    'sixpack': (100, 100, 100),
}

MIN_DEST_X = 0
MAX_DEST_X = 4

# This is not just enemies, but also pick-ups (for whatever reason)
ENEMY_NAMES = [
    'pearl',
    'fishy_rainbow',
    'fishy_red',
    'fishy_deepsea',
    'diver',
    'seaweed',
    'lanternfish',
    'shell',
    'sandboxtoys',
    'oyster_0_pearl',
    'oyster_1_pearl',
    'oyster_2_pearl',
    'oyster_3_pearl',
    'rock_m',
    'rock_l',
    'rock_s',
    'jellyfish_a',
    'jellyfish_b',
    'starfish',
    'shoe',
]

class Game(Scene):
    DEPTH = 15

    MAX_SPEEDUP = 4
    SPEEDUP_STEP = .1

    # keyboard repeat rate (modulo) -> higher value = less repeat
    KEYBOARD_REPEAT_MOD = 7

    def __init__(self, app):
        super(Game, self).__init__(app)

        # health is 9: 3 lives are grouped per 3.
        self._init(self.app.level_nr, score=0, health=9)


    def _init(self, level_nr, score, health):
        self.time = 0.
        self.i = 0
        self.direction = 0
        self.boost = False
        self.speedup = 0

        self.level = Level(self.app.get_filename('levels/level%s.txt' % level_nr))

        self.player = Player(self.app, health=health, coins_collected=score)

        #self.message = None

        self.enemies = {}

        for key in ENEMY_NAMES:
            self.enemies[key] = Enemy(self.app, key)


    def resume(self, arg):
        super(Game, self).resume(self)
        if arg and 'next_level' in arg.keys():
            self._init(arg['next_level'], arg['score'], arg['health'])

    def process(self):
        # it's kind of annoying -> commented out
        #if self.message:
        #    return

        self.i += 1

        step = .01 * self.level.speed
        if self.boost:
            if self.speedup < self.MAX_SPEEDUP:
                self.speedup += self.SPEEDUP_STEP
            if self.speedup > self.MAX_SPEEDUP:
                self.speedup = self.MAX_SPEEDUP
        else:
            if self.speedup > 0:
                self.speedup -= self.SPEEDUP_STEP * 2
            if self.speedup < 0:
                self.speedup = 0

        self.time += step * (1 + self.speedup)

        if self.time > 1.:
            self.time -= 1.
            self.player.y += 1
            #self.message = self.level.get_message(self.player.y)

        if self.level.exceeds_row(self.player.y):
            # animate level end
            self.next_state = ("CutScene", {
                    "score": self.player.coins_collected,
                    "health": self.player.health,
                    "story": self.level.story
                })

        if self.i % self.KEYBOARD_REPEAT_MOD == 0:
            next_x = self.player.dest_x + self.direction
            if next_x >= MIN_DEST_X and next_x <= MAX_DEST_X:
                self.player.dest_x += self.direction

        self.player.step()
        for enemy in self.enemies.values():
            enemy.step()

        if self.player.health <= 0:
            #print 'YOU ARE DEAD!'
            self.next_state = ("GameOver", None)

        return super(Game, self).process()

    def process_input(self, event):
        #if self.message and event.type == KEYUP and event.key == K_RETURN:
        #    rest = self.message.split('\n', 1)
        #    if len(rest) == 2:
        #        self.message = rest[1]
        #    else:
        #        self.message = None

        def go_left():
            self.direction = -1
            self.i = 0
            if self.player.dest_x > MIN_DEST_X:
                self.player.dest_x -= 1

        def go_right():
            self.direction = 1
            self.i = 0
            if self.player.dest_x < MAX_DEST_X:
                self.player.dest_x += 1

        if event.type == QUIT:
            self.next_state = ("GoodBye", None)
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < self.app.screen.height / 2:
                self.boost = True

            if y > self.app.screen.height * 3 / 4:
                self.player.jump()

            if x < self.app.screen.width / 3:
                go_left()
            elif x > self.app.screen.width * 2 / 3:
                go_right()
        elif event.type == MOUSEBUTTONUP:
            self.direction = 0
            self.boost = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                pass
            elif event.key == K_SPACE:
                self.player.jump()
            elif event.key == K_ESCAPE:
                self.next_state = ("GoodBye", None)
            elif event.key == K_LEFT:
                go_left()
            elif event.key == K_RIGHT:
                go_right()
            elif event.key == K_UP:
                self.boost = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.direction = 0
            elif event.key == K_RIGHT:
                self.direction = 0
            elif event.key == K_UP:
                self.boost = False

    def map_coords(self, lane, jump, distance):
        """
        Translate game coordinates to world coordinates.

        lane:     0..5
        jump:     not defined yet
        distance: 0..self.DEPTH+1 (number of rows)

        world coordinates: 1x1xWORLD_DEPTH
        """

        x = (lane + 0.5) / 5.0
        y = (500.0 - jump) / 500.0
        z = WORLD_DEPTH * (distance+0.5) / self.DEPTH

        return (x, y, z)


    def draw(self):
        self.app.screen.clear()
        backgrounds = self.app.resman.get_background(self.level.background)
        pos = int(self.time + self.player.y) % len(backgrounds)
        self.app.screen.display.blit(backgrounds[pos], (0, 0))

        x = self.player.x
        y = self.time
        player_points = self.mkpoints(x, y, self.player.height)
        #draw.polygon(screen, (255, 255, 255), player_points, 1)

        # draw queue for back-to-front drawing of enemies
        draw_queue = [(y, self.player, player_points)]

        for yidx, offset in enumerate(range(self.player.y, self.player.y+self.DEPTH)):
            if offset < len(self.level.rows):
                for xidx, column in enumerate(self.level.rows[offset].items):
                    if column is None:
                        continue

                    color = colors.get(column.name, (0, 0, 0))

                    x = xidx
                    y = yidx

                    if yidx == 1 and xidx == self.player.dest_x and self.player.height < 10:
                        c = column.collide(self.player)
                        if c > 0:
                            # do something when the player collides
                            if self.player.health % 3 == 0:
                                # lost a full life
                                self.next_state = ("CutScene", {
                                    "score": self.player.coins_collected,
                                    "health": self.player.health,
                                    "story": ['you lost a life', 'be careful next time'],
                                    "restart": True,
                                })
                        elif c < 0:
                            # picked up a coin
                            player_points = [self.app.screen.projection(*point)
                                             for point in player_points]

                    points = self.mkpoints(x, y)
                    color = shade_color(color, yidx-self.time, self.DEPTH)
                    if column.name in self.enemies:
                        enemy = self.enemies[column.name]
                        draw_queue.append((y, enemy, points))
                    elif column.name:
                        print '[WARNING] Missing graphic:', column.name
                        self.app.screen.draw_polygon(color, points)

        # Draw all enemies (+player), back-to-front for proper stacking order
        for _, sprite, points in sorted(draw_queue, reverse=True):
            self.app.screen.draw_sprite(sprite, points)

        self.app.screen.draw_stats(self.player.coins_collected,
                                   self.player.health)

        #if self.message:
        #    message = self.message.split('\n', 1)[0]
        #    self.app.screen.draw_message(message)


    def mkpoints(self, x, y, height=0.):
        return [
                self.map_coords(x-.45, height, y-.45 - self.time),
                self.map_coords(x+.45, height, y-.45 - self.time),
                self.map_coords(x+.45, height, y+.45 - self.time),
                self.map_coords(x-.45, height, y+.45 - self.time),
        ]

