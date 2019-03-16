#Alex Lewandowski
#Visible Object Classes for Othello
#Board, Tiles, AgentMenu, and Scoreboard
#2/09/19
#CS405 Homework 1

import arcade
#W = 1000
#H = int(W * 0.75)

W = 1500
H = int(W * 0.48)

BLACK = arcade.color.BLACK
WHITE = arcade.color.WHITE 


            
#####################
##   BOARD CLASS   ##
#####################
class Board:
    def draw(self):
        
        #Point lists for drawing lines on board
      
        point_list_vertical = ((float(int(W/5)), H),(float(int(W/5)), float(int(H - H/40))), (float(int(W/5)), float(int(H- H/40 - H/20))), (float(int(W/5)), float(int(H/2))), (float(int(W/5)), float(int(H/2 - H/20))), (float(int(W/5)), float(int(H/40 + H/20))), 
        (float(int((W - (W/5)))), float(int(H - H/20))),  (float(int((W - (W/5)))), float(int(H/2))),  (float(int((W - (W/5)))), float(int(H/2)-(H/20))), (float(int(W - (W/5))), 0), 
        (float(int(W - (W/5) - (H/40))), float(int(H/40))), (float(int(W - (W/5) - (H/40))), float(int(H - (H/2) - (H/20)))))  
        
        point_list_horizontal = ((float(int(W/5)), float(int((H/40)))), (float(int(W - (W/5) - (H/40))), float(int(H/40)))) #############################################################################################################################################################################################################

        arcade.draw_lines(point_list_vertical, BLACK, 2.0)
        arcade.draw_lines(point_list_horizontal, BLACK, 2.0)

        
       

## end Board class


