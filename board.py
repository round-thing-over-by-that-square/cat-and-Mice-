#Alex Lewandowski
#Cat and mice board
#2/09/19
#CS405 Homework 1

import arcade
#W = 1000
#H = int(W * 0.75)

W = 1500
H = int(W * 0.48)

BLACK = arcade.color.BRIGHT_LAVENDER #arcade.color.BLACK
WHITE = arcade.color.WHITE 


            
#####################
##   BOARD CLASS   ##
#####################
class Board:
    def draw(self):
        
        #Point lists for drawing lines on board
      
        cheeseWall = ((float(int(W/5)), float(int(H- ((3*H)/40)))), (float(int(W/5)), float(int(H/2))), (float(int(W/5)), float(int(H/2 - H/20))), (float(int(W/5)), float(int((H/10) + (H/40)))))
        waterWall = ((float(int((W - (W/5)))), float(int(H - H/20))),  (float(int((W - (W/5)))), float(int(H/2))),  (float(int((W - (W/5)))), float(int(H/2)-(H/20))), (float(int(W - (W/5))), 0))
        passageWallVert = ((float(int(W - (W/5) - (H/30))), float(int(H/20))), (float(int(W - (W/5) - (H/30))), float(int(H - (H/2) - (H/20)))))  
        
        passageWallHoriz = ((float(int(W/5)), float(int((H/20)))), (float(int(W - (W/5) - (H/30))), float(int(H/20)))) #############################################################################################################################################################################################################

        arcade.draw_lines(cheeseWall, BLACK, 2.0)
        arcade.draw_lines(waterWall, BLACK, 2.0)
        arcade.draw_lines(passageWallVert, BLACK, 2.0)
        arcade.draw_lines(passageWallHoriz, BLACK, 2.0)

        
       

## end Board class


