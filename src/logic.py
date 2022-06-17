import random
from typing import List, Dict
import math

def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization
    """
    return {
        "apiversion": "1",
        "author": "artemise",
        "color": "#4ebbd4",
        "head": "all-seeing",
        "tail": "mystic-moon",
    }

def _get_direction(point1, point2) -> str:
  """Get direction FROM point2 TO point1"""
  if point1["x"] > point2["x"]: return "right"
  elif point1["x"] < point2["x"]: return "left"
  elif point1["y"] > point2["y"]: return "up"
  elif point1["y"] < point2["y"]: return "down"

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request
    return: A String, the single move to make. One of "up", "down", "left" or "right".
    """
    food_radius = 3
    my_snake = data["you"]
    my_body = my_snake["body"]
    my_head = my_snake["head"]
    board = data['board']

    # determine possible moves
    last_move = _get_direction(my_head, my_body[1])
    possible_moves = ["up", "down", "left", "right"]
    possible_moves = _avoid_walls(my_body, possible_moves, board)
    for snake in board["snakes"]:
      possible_moves = _avoid_body(snake["body"], my_head, possible_moves)
    
    # find close food
    nearest_food_direction = ""
    food_in_range = _find_food_in_range(food_radius, my_head, board) 
    if food_in_range:
      closest_food = sorted(food_in_range, key=(lambda x: _get_distance(x, my_head)))[0]
      nearest_food_direction = _get_direction(closest_food, my_head)
    
    # select preferred move over random move, cascading order
    if nearest_food_direction and nearest_food_direction in possible_moves:
        move = nearest_food_direction
    
    # prefer straight lines
    elif last_move in possible_moves: 
      move = last_move
    
    # random if no preffered choice is possible
    elif possible_moves: 
      move = random.choice(possible_moves)
    else:
      move = None

    print(f"MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    return move


def _get_distance(point1, point2) -> float:
  return math.sqrt(pow((point1["x"] - point2["x"]), 2) + pow((point1["y"] - point2["y"]), 2))

def _find_food_in_range(food_radius: int, my_head: dict, board) -> List[dict]:
  """return: The list of food disks inside radius"""
  food_in_range = []
  for food in board["food"]:
    if (food["x"] >= my_head["x"]-food_radius) and (food["x"] <= my_head["x"]+food_radius) and \
    (food["y"] >= my_head["y"]-food_radius) and (food["y"] <= my_head["y"]+food_radius):
      food_in_range.append(food)
  return food_in_range

def _avoid_body(body: dict, my_head: dict, possible_moves: List[str]) -> List[str]:
    """return: The list of remaining possible_moves, avoiding any snake bodies"""
    for segment in body:
      if ("left" in possible_moves) and (segment["x"] == my_head["x"]-1) and (segment["y"] == my_head["y"]):
        possible_moves.remove("left")
      elif ("right" in possible_moves) and (segment["x"] == my_head["x"]+1) and (segment["y"] == my_head["y"]):
        possible_moves.remove("right")
      elif ("down" in possible_moves) and (segment["y"] == my_head["y"]-1) and (segment["x"] == my_head["x"]):
        possible_moves.remove("down")
      elif ("up" in possible_moves) and (segment["y"] == my_head["y"]+1) and (segment["x"] == my_head["x"]):
        possible_moves.remove("up")
    return possible_moves

def _avoid_walls(my_body: dict, possible_moves: List[str], board) -> List[str]:
    """return: The list of remaining possible_moves, avoiding any walls"""
    my_head = my_body[0]  # The first body coordinate is always the head
    if ("left" in possible_moves) and my_head["x"] == 0:
        possible_moves.remove("left")
    if ("right" in possible_moves) and my_head["x"] == board["width"] - 1:
        possible_moves.remove("right")
    if ("down" in possible_moves) and my_head["y"] == 0:
        possible_moves.remove("down")
    if ("up" in possible_moves) and my_head["y"] == board["height"] -1:
        possible_moves.remove("up")

    return possible_moves
