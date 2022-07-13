import pygame
ASPECT_RATIO= 0.7
INDEX_TO_GRID = ["A", "B", "C", "D", "E", "F", "G", "H"]

def init():
    """
    This is an initialization function
    :return: Null
    Establish the paramters / Variable and load all necessary packages
    :param init:
    :return:
    """
    #Preload all pacakges
    pygame.init()

    #Declaration of global variables

    global WHITE
    WHITE = (255, 255, 255)

if __name__ == "__main__":
    init()
    size = (int(800 * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    screen = pygame.display.set_mode(size)
    selectPos = (-1, -1)
    dropPos = (-1, -1)

while True:
    #Check for mouse click event
    e = pygame.event.wait()
    if pygame.event.event_name(e.type) == "MouseButtonDown":
    #Identify the row and column of our click
    #Get x and get y
        mouseX = e.pos[0]
        mouseY = e.pos[1]
        rowNum = int(mouseY / (100 * ASPECT_RATIO))
        colNum = int(mouseX / (100 * ASPECT_RATIO))
        # print("Row clicked: " + str(rowNum + 1))
        # print("Column clicked: " + str(colNum + 1))



        """
        3 cases: 
            1. First selection (Identified by -1 values by selectPos)
            2. Reselection (Identified by the same position as in the selectPos)
            3. Final selection (Identified by a non-negative selectPos and negativePos)
        """

        if (selectPos[0] < 0): # Case 1
            selectPos = (colNum, rowNum)
            print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
        elif (selectPos[0] >= 0 and selectPos == (colNum, rowNum)): # Case 2
            selectPos = (-1, -1)
            print("Deselected Piece ")
        else: # Case 3
            dropPos = (colNum, rowNum)
            print("Moved Piece from " + str(INDEX_TO_GRID[selectPos[0]]) + str(selectPos[1] + 1) \
                  + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
            selectPos = (-1, -1)
            dropPos = (-1, -1)

    #Draw Grid
    #Horizontal lines

    for i in range(1,8,1): #Start at 1, reach up to 8, increase by 1
        pygame.draw.line(screen, WHITE, (0, i * 100 * ASPECT_RATIO), (screen.get_width(), i * 100 * ASPECT_RATIO))
        pygame.draw.line(screen, WHITE, (i * 100 * ASPECT_RATIO, 0), (i * 100 * ASPECT_RATIO, screen.get_height()))

    #Vertical lines
    pygame.display.flip()

    pass
