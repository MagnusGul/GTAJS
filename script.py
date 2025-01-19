from engine import *

def script(game):
    game.character = load_character("girl")
    game.character.physics_engine = arcade.PhysicsEngineSimple(game.character, game.tile_map_manager.wall_list)
    game.tile_map_manager.load_map(game, "testmap", 2)