import ugame
import stage
import constants
import time
import random


def game_scene():

    score = 0

    def show_alien():
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

    image_bank_bg = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    pew_sound = open("pew.wav", "rb")
    boom_sound = open("boom.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    background = stage.Grid(image_bank_bg, 10, 8)
    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))

    ship = stage.Sprite(
        image_bank_sprites,
        5,
        75,
        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE),
    )

    aliens = [
        stage.Sprite(image_bank_sprites, 9,
                constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        for _ in range(constants.TOTAL_NUMBER_OF_ALIENS)
    ]

    lasers = [
        stage.Sprite(image_bank_sprites, 10,
                constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        for _ in range(constants.TOTAL_NUMBER_OF_LASERS)
    ]

    show_alien()

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = lasers + [ship] + aliens + [background]
    game.render_block()

    while True:

        keys = ugame.buttons.get_pressed()

        # Ship movement
        if keys & ugame.K_RIGHT:
            ship.move(
                min(ship.x + constants.SPRITE_MOVEMENT_SPEED,
                    constants.SCREEN_X - constants.SPRITE_SIZE),
                ship.y,
            )

        if keys & ugame.K_LEFT:
            ship.move(
                max(ship.x - constants.SPRITE_MOVEMENT_SPEED, 0),
                ship.y,
            )

        # Fire laser
        if keys & ugame.K_O:
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # Move lasers
        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Move aliens
        for alien in aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)y
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        # Collision detection
        for laser in lasers:
            if laser.x > 0:
                for alien in aliens:
                    if alien.x > 0:
                        if stage.collide(
                            laser.x + 6, laser.y + 2,
                            laser.x + 11, laser.y + 12,
                            alien.x + 1, alien.y,
                            alien.x + 15, alien.y + 15,
                        ):
                            alien.move(constants.OFF_SCREEN_X,
                                    constants.OFF_SCREEN_Y)
                            laser.move(constants.OFF_SCREEN_X,
                                    constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            show_alien()
                            score += 1

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


def splash_scene():
    coin = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin)
    time.sleep(2)
    menu_scene()


def menu_scene():
    image_bank = stage.Bank.from_bmp16("space_aliens_background.bmp")
    background = stage.Grid(image_bank, 10, 8)

    text = stage.Text(
        width=29, height=12, palette=constants.RED_PALETTE
    )
    text.move(20, 50)
    text.text("PRESS START")

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [text, background]
    game.render_block()

    while True:
        if ugame.buttons.get_pressed() & ugame.K_START:
            game_scene()
        game.tick()


if __name__ == "__main__":
    splash_scene()
