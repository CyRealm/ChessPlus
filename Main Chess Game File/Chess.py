import pygame
ASPECT_RATIO = 1
INDEX_TO_GRID = ["A","B","C","D","E","F","G","H"]

def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variables and load all necessary Packages
    """
    # Preload all Packages
    pygame.init()

    # Declaration of Global Variables
    global WHITE
    WHITE = (255, 255, 255)


if __name__ == "__main__":
    init()
    size = (int(800 * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    screen = pygame.display.set_mode(size)
    selectPos = (-1, -1)
    dropPos = (-1, -1)


while True:
    # Check for mouseDown Event
    e = pygame.event.wait()
    if pygame.event.event_name(e.type) == "MouseButtonDown":
        # Identify the row and column of our click
        # Get x and get y
        mouseX = e.pos[0]
        mouseY = e.pos[1]
        rowNum = int(mouseY / (100 * ASPECT_RATIO))
        colNum = int(mouseX / (100 * ASPECT_RATIO))
        # print("Row Clicked: " + str(rowNum + 1))
        # print("Column Clicked: " + str(colNum + 1))


        """
        3 Cases:
            1. First selection (identified by -1 values in selectPos)
            2. Deselctioion (identified by the same position as selectPos)
            3. Final selection (identified by a non-negative selectPos and a negative dropPos)
        """
        if (selectPos[0] < 0): # Case 1
            selectPos = (colNum, rowNum)
            print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
        elif (selectPos[0] >= 0 and selectPos == (colNum, rowNum)): # Case 2
            selectPos = (-1, -1)
            print("Deselected Piece")
        else: # Case 3
            dropPos = (colNum, rowNum)
            print("Moved Piece from " + str(INDEX_TO_GRID[selectPos[0]]) + str(selectPos[1] + 1)\
                  + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
            selectPos = (-1, -1)
            dropPos = (-1, -1)



    # Draw Grid
    for i in range(1, 8, 1): # Start i at 1, reach up to 8, increase i by 1 each loop
        pygame.draw.line(screen, WHITE, (0, i * 100 * ASPECT_RATIO), (screen.get_width(), i * 100 * ASPECT_RATIO)) # Horizontal Lines
        pygame.draw.line(screen, WHITE, (i * 100 * ASPECT_RATIO, 0), (i * 100 * ASPECT_RATIO, screen.get_height())) # Vertical Lines

    pygame.display.flip()