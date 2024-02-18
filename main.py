import random
from random import choices
import pygame
import math

## SETUP ##
pygame.init()
from pygame.locals import *

dimensions = "4x4"
width = int(dimensions.split('x')[0])
height = int(dimensions.split('x')[1])

## SINGLETONS (GLOBALS) ##

global matrix
matrix = []

for i in range(width):
  test = []
  for i in range(height):
    test.append('')
  matrix.append(test)

global score
score = 0

# use this to reset the board
originalmatrix = [row[:] for row in matrix]

## PYGAME SETUP ##

# If you change one value and keep the other it will prob break :/
# aka: use the same values
dimensions = (300, 300)
pygame.display.set_caption('  2048')

# Set up the drawing window
screen = pygame.display.set_mode([dimensions[0] + 200, dimensions[1]])
dimensionofsquare = math.floor(dimensions[0] / 6)

# Fill the background with white
screen.fill((255, 255, 255))

colors = {
    # every "newsquare" is gray to indicate its new
    "0": (60, 60, 60),
    "2": (238, 228, 218),
    "4": (237, 224, 200),
    "8": (242, 177, 121),
    "16": (245, 149, 99),
    "32": (246, 124, 95),
    "64": (246, 94, 59),
    "128": (237, 207, 114),
    "256": (237, 204, 97),
    "512": (237, 200, 80),
    "1024": (237, 197, 63),
    "2048": (237, 194, 46),
}


## RENDER FUNCTIONS ##
def renderSquares():
  for column in range(height):
    for row in range(width):
      x = dimensionofsquare * row
      y = dimensionofsquare * column
      typeofsquare = matrix[column][row]

      color = colors[typeofsquare] if typeofsquare != "" else (0, 0, 0)

      # Create a font object
      font = pygame.font.Font(None, 36)

      # Create a text surface
      text = font.render(typeofsquare, True, (0, 0, 0))

      # x, y, w, h
      square = Rect(x, y, dimensionofsquare, dimensionofsquare)

      # Draw a solid blue circle in the center
      button = pygame.draw.rect(screen, color, square)

      # Draw the text onto the button
      text_rect = text.get_rect(center=button.center)
      screen.blit(text, text_rect)

# Grid variables
print(dimensions)
WIDTH, HEIGHT = (width * dimensionofsquare, height * dimensionofsquare)
CELL_SIZE = 50  # size of each cell in the grid
GRID_COLOR = (200, 200, 200)  # color of the grid lines (grey in this case)

def draw_grid():
  print(WIDTH, HEIGHT, 'test')
  for x in range(0, WIDTH, CELL_SIZE):  # for each column
    pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WIDTH))
  for y in range(0, HEIGHT, CELL_SIZE):  # for each row
    pygame.draw.line(screen, GRID_COLOR, (0, y), (HEIGHT, y))

def updateScore():
  # Create a font object
  font = pygame.font.Font(None, 36)

  # Create a text surface
  text = font.render(f"Score {score}", True, (0, 0, 0))
  
  x = dimensionofsquare * width + 20
  screen.blit(text, (x, 10))

def renderBoard():
  screen.fill((255, 255, 255))
  renderSquares()
  draw_grid()
  updateScore()
  pygame.display.update()


## KEY INPUT ##
def check_for_key_input():
  # Did the user click the window close button?
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        return 'u'
        # processMove('u')
      elif event.key == pygame.K_DOWN:
        return 'd'
        # processMove('d')
      elif event.key == pygame.K_LEFT:
        return 'l'
        # processMove('l')
      elif event.key == pygame.K_RIGHT:
        return 'r'
        # processMove('r')
    else:
      return None


## RANDOM SQUARE ##
def add_random_square():
  # finds all empty squares and and it to a tuple
  # help from chatgpt with this line
  empty_squares = [(i, j) for i, row in enumerate(matrix)
                   for j, val in enumerate(row) if val == '']
  if not empty_squares:
    print('You lost!')
    return False
  else:
    # gets random coordinate from tuple
    random_square = random.choice(empty_squares)

    # random.choice([choices], [weights])
    # as score increases, weights start increasing on higher numbers
    # equations:
    # 2 -> y = 2x
    # 4 -> y = x^1.1
    # 16 -> y = x^1.05
    chosen_number = None
    if score == 0:
      chosen_number = '2'
    else:
      print('matrix of choices: ', [score * 100, score ** 1.5, score ** 0.2])
      chosen_number = str(choices([2, 4, 16], [score * 100, score * 1.5, score ** 0.2])[0])

    matrix[random_square[0]][random_square[1]] = chosen_number


## LOGIC ##
def replaceSquare(row, column, replaceWith):
  print(replaceWith)
  matrix[row][column - 1] = replaceWith
  print(matrix[row][column - 1])
  matrix[row][column] = ''

def processMove(key):
  global matrix
  global score
  # if key is any arrow key
  if key in ('u', 'r', 'l', 'd'):
    # help from chatgpt
    if key == 'r':
      matrix = [row[::-1] for row in matrix]
    elif key == 'u':
      matrix = [[matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]) - 1, -1, -1)]
    elif key == 'd':
      matrix = [[matrix[j][i] for j in range(len(matrix) - 1, -1, -1)]
                for i in range(len(matrix[0]))]

    # check to the left of each box
    for row in range(height):
      for column in range(width):
        # matrix[row][column] is current item
        # matrix[row][column - 1] is the item to the left

        ## BEFORE DOING ANYTHING ##
        # TODO: Make sure to remove the gray color from numbers just added
        # if matrix[row][column] == "0":
        #   matrix[row][column] = "2"

        # if item is a number

        if matrix[row][column] != '':
          # print(row, column)
          print('matrix', matrix[row], column)
          # if it's at the end, don't move
          if column == 0:
            pass
          elif matrix[row][column - 1] == matrix[row][column]:
            if matrix[row][column - 1] == matrix[row][column]:
              combined = int(matrix[row][column]) * 2
              score += combined
              print('combined!', combined)
              print(matrix)
              # replace the square in current column
              replaceSquare(row, column, str(combined))
              print(matrix, 'eft')
              # renderBoard()
              # input('TEST')
              # empty the original square
              matrix[row][column] = ''
              # replaceSquare(row, column + 1, 'row', '128')
              # renderBoard()
              # input('TEST2')

          elif matrix[row][column - 1] == '':
            # print('2')
            replaceSquare(row, column, matrix[row][column])
            # input("TEMP")
    # help from chatgpt
    if key == 'r':
      matrix = [row[::-1] for row in matrix]
    elif key == 'u':
      matrix = [[matrix[j][i] for j in range(len(matrix) - 1, -1, -1)]
                for i in range(len(matrix[0]))]
    elif key == 'd':
      matrix = [[matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]) - 1, -1, -1)]

def restartGame():
  global matrix, score
  print(matrix, 'og', originalmatrix)
  matrix = [row[:] for row in originalmatrix]
  score = 0

## UI ##

def start():
  renderBoard()
  return False

## WINNING/LOSING LOOP ##
while True:
  while start == False:
    start()
  ## GAME LOOP ##
  while True:
    addsquare = add_random_square()
    if addsquare == False:
      break
    renderBoard()
    print(matrix)
  
    keyinput = None
    while keyinput == None:
      keyinput = check_for_key_input()
  
    # Make sure all numbers combine and go to empty spaces (bad practice)
    for _ in range(width):
      print('-------------------')
      # When key input comes in now process the move
      processMove(keyinput)
      renderBoard()
  # TODO: Reset board and restart game
  restartGame()