# 🎮 Rock Paper Scissors - Computer Vision Edition

<div align="center">
  <img src="Resources/start.png" width="600"/>
</div>

## 📌 Project Overview 
This project is an interactive Rock-Paper-Scissors Game where players can compete against the computer by posing hand gestures. Using image processing techniques, the system captures the user's gesture, processes it to identify whether it's "Rock," "Paper," or "Scissors," and determines the winner based on classic game rules. The application is built with Python and showcases real-time image processing visualization.

## 🛠️ Technologies Used

Programming Language: Python

Libraries: OpenCV

Image Processing Techniques: Greyscale, Thresholding, Background Removal, Contour Detection

Visualization: Matplotlib for step-by-step image transformations

## 🔄 How to Run the Application
1. Clone the repository <br>
   git clone <repository-url>
   
2. Navigate to the project directory <br>
   cd rock-paper-scissors

3. Install the dependencies <br>
   pip install -r requirements.txt

4. Run the application
   python main.py

## Game Screens

<div align="center">
  <img src="Resources/Bg.png" width="250" title="Main Game Background"/>
  <img src="Resources/game_over.jpg" width="250" title="Game Over Screen"/> 
</div>

## How to Play
Position your hand in the right side detection box

Make one of these gestures 

✊ Closed fist = Rock <br>
✋ Open palm = Paper <br>
✌️ Two fingers = Scissors <br>

The computer will automatically respond

First to win 3 rounds wins the match! <br> 

## 🎮 Game Rules
✊ Rock crushes ✌️ Scissors <br>
✌️ Scissors cuts 📄 Paper <br>
📄 Paper covers ✊ Rock <br>
🔄 If both gestures match, it's a 🤝 Tie

## Features
- Real-time ✊✋✌️ detection using webcam
- Interactive score tracking
- Best of 5 rounds system
- Animated countdown timer
- Responsive full screen UI
- User-friendly interface with smooth gameplay.
- Error handling and feedback for better user experience.

## Controls

ESC = Quit game

Mouse = Click buttons on result screen 
