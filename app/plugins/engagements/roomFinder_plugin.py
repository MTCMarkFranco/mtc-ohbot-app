import os
import requests
from semantic_kernel.functions import kernel_function
import webbrowser

class RoomFinderPlugin:
    @kernel_function(name="show_RoomDirections", description="Play the room specific video for the room you are looking for.")
    def show_RoomDirections(self, room_name: str) -> str:
        """
           Play the room specific video for the room you are looking for.
           
        Returns:
            void: returns nothing
            
        """
       
        print(room_name)
        # C:\Projects\new-oh-bot\mtc-ohbot-app\video\Great-Bear.mp4
        webbrowser.open(f"C:\\Projects\\new-oh-bot\\mtc-ohbot-app\\video\\{room_name}.mp4")
                 
        return 