import ugame
import stage
import constants

def game_scene():
    # This function is the main game scene

    # image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)


    # sets the background to image in the image bank
    # and the size (10x8 tiles of size 16x16)
    background = stage.Grid(
        image_bank_background, 10,8)
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )
    alien= stage.sprite(image_bank_sprites,9,int(constants.SCREEN_X/2 - constants.SPRITE_SIZE/2),16)
    # create a stage for the background to show up on
    # and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [ship] + [alien]+[background]

    # render the background and initial location of sprite list

    # most likely you will only render blocks
    game.render_block()

    # repeat forever, game loop
    while True:

        # get user input
        keys = ugame.buttons.get_pressed()

        # A button to fire
    if keys & ugame.K_O != 0:
        if a_button == constants.button_state["button_up"]:
        a_button = constants.button_state["button_just_pressed"]
        elseif a_button == constants.button_state["button_just_pressed"]:
        a_button = constants.button_state["button_still_pressed"]
    else:
        if a_button == constants.button_state["button_still_pressed"]:
            a_button = constants.button_state["button_released"]
        else:
            a_button = constants.button_state["button_up"]

        if keys & ugame.K_X != 0 :
            pass
        
        if keys & ugame.K_START != 0 :
            print("Start")
        if keys & ugame.K_SELECT != 0 :
            print("Select")
        if keys & ugame.K_RIGHT != 0 :
            if ship.x <( constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                ship.move((constants.SCREEN_X - constants.SPRITE_SIZE),ship.y)

        if keys & ugame.K_LEFT != 0:
            if ship.x > 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP != 0 :
            pass
        if keys & ugame.K_DOWN != 0:
            pass

        # update game logic
        # redraw sprites
        if a_button == constants.button_state["buttons_just_pressed"]:
            sound.play(pew_sound)

        # redraw sprites
    

        game.render_sprites([ship]+[alien])
        game.tick()


if __name__ == "__main__":
    game_scene()
