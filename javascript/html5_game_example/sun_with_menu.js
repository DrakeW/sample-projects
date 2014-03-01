// Get access to canvas in HTML file
var canvas = document.getElementById('game_canvas');
var context = canvas.getContext('2d');



//-------------------------------------------//
//---------- GAME GLOBAL VARIABLES ----------//
//-------------------------------------------//
// Game dimensions
var width = 1000;
var height = 600;
// Set canvas dimensions to correct width and height
canvas.width = width;
canvas.height = height;
// Back button specs
var backBtnX = 10;
var backBtnY = 10;
var backBtnW = 175;
var backBtnH = 39;
// Play button specs
var playBtnX = 467;
var playBtnY = 280;
var playBtnW = 87;
var playBtnH = 39;
// Ball specs, to be determined when we reset the game
var ballDiam, ballX, ballY, ballVx, ballVy;
// Game state to keep track of which game screen we're on
var gameState = 0;
// Message color for menu
var msgColor = "yellow";
var msgColorCount = 0;



//---------------------------------------//
//---------- PRELOADING IMAGES ----------//
//---------------------------------------//
// Define images
var bgImg = new Image();
bgImg.src = "imgs/background.jpg";
var ballImg = new Image();
ballImg.src = "imgs/sun.png";
var backBtnImg = new Image();
backBtnImg.src = "imgs/back_btn.png";
var playBtnImg = new Image();
playBtnImg.src = "imgs/play_btn.png";

// Ensure all images have loaded before starting the game
var numImages = 4;
var numLoaded = 0;
var imageLoaded = function() {
  numLoaded++;
  if (numLoaded === numImages) {
    initGame();
  }
};
bgImg.onload = function() {
  imageLoaded();
};
ballImg.onload = function() {
  imageLoaded();
};
backBtnImg.onload = function() {
  imageLoaded();
};
playBtnImg.onload = function() {
  imageLoaded();
};



//-----------------------------------------//
//---------- GAME INITIALIZATION ----------//
//-----------------------------------------//
// Code to reset ball
var resetBall = function() {
  ballDiam = Math.floor(Math.random() * 50) + 50;
  ballX = width / 2 - ballDiam / 2;
  ballY = height / 2 - ballDiam / 2;
  ballVx = Math.floor(Math.random() * 20) - 10;
  ballVy = Math.floor(Math.random() * 20) - 10;
}
// Initialize game objects and start game loop
var initGame = function() {
  // In this case, no initialization needed, so just
  // start game loop
  updateGame();
};



//-----------------------------------------//
//---------- HANDLING USER INPUT ----------//
//-----------------------------------------//
// Code that handles mouse clicks
var onCanvasMouseDown = function(e) {
  // Find the mouse x and y relative to the top-left corner of the canvas
  var x = e.layerX;
  var y = e.layerY;

  // Do different things depending on what screen we're looking at
  if (gameState === 0) {
    // This is the menu screen
    // Check if we clicked the play button
    if (x >= playBtnX && x <= playBtnX + playBtnW &&
        y >= playBtnY && y <= playBtnY + playBtnH) {
      // If so, move to gameplay state
      resetBall();
      gameState = 1;
    }
  } else if (gameState === 1) {
    // This is the gameplay screen
    // Check if we clicked the back button
    if (x >= backBtnX && x <= backBtnX + backBtnW &&
        y >= backBtnY && y <= backBtnY + backBtnH) {
      // If so, move to menu
      gameState = 0;
    }
    // Check if we clicked the ball
    if (x >= ballX && x <= ballX + ballDiam &&
        y >= ballY && y <= ballY + ballDiam) {
      // If so, reverse its direction
      ballVx = -ballVx;
      ballVy = -ballVy;
    }
  }
};
canvas.addEventListener('mousedown', onCanvasMouseDown);

// Code that handles key presses
var onCanvasKeyDown = function(e) {
  // Uncomment this log statement to figure out which keys have which keyCode
  // console.log(e.keyCode);

  if (gameState === 1) {
    // Reset ball movement when 'r' key is pressed
    if (e.keyCode === 82) {
      resetBall();
    }
  }
};
window.addEventListener('keydown', onCanvasKeyDown);



//------------------------------------//
//---------- MAIN GAME LOOP ----------//
//------------------------------------//
var updateGame = function() {
  // Draw the background image no matter what screen we're looking at
  context.drawImage(bgImg, 0, 0, width, height);

  // Do different things depending on what screen we're looking at
  if (gameState === 0) {
    // This is the menu screen
    // Move game objects (just the color of the message in this case)
    // Change the color of the message every forty frames (one second)
    if (msgColorCount === 40) {
      if (msgColor === "yellow") {
        msgColor = "blue";
      } else if (msgColor === "blue") {
        msgColor = "yellow";
      }
      msgColorCount = 0;
    } else {
      msgColorCount++;
    }
    // Write a message on the screen
    context.font = "30px Arial";
    context.fillStyle = msgColor;
    context.fillText("Here comes the sun!", 200, 30);
    // Draw play button
    context.drawImage(playBtnImg, playBtnX, playBtnY, playBtnW, playBtnH);
  } else if (gameState === 1) {
    // This is the gameplay screen
    // Move game objects (just the ball in this case)
    ballX += ballVx;
    ballY += ballVy;
    if (ballX < 0 || ballX + ballDiam > width) {
      ballVx = -ballVx;
    }
    if (ballY < 0 || ballY + ballDiam > height) {
      ballVy = -ballVy;
    }
    // Draw images corresponding to game objects
    context.drawImage(ballImg, ballX, ballY, ballDiam, ballDiam);
    context.drawImage(backBtnImg, backBtnX, backBtnY, backBtnW, backBtnH);
  }

  // Wait 25 milliseconds before starting next game frame
  // This line keeps the game running so it should always run no matter which
  // screen we're looking at
  setTimeout(updateGame, 25);
};
