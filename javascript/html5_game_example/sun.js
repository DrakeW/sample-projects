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
// Reset button specs
var resetBtnX = 10;
var resetBtnY = 10;
var resetBtnW = 159;
var resetBtnH = 38;
// Ball specs, to be determined when we reset the game
var ballDiam, ballX, ballY, ballVx, ballVy;



//---------------------------------------//
//---------- PRELOADING IMAGES ----------//
//---------------------------------------//
// Define images
var bgImg = new Image();
bgImg.src = "imgs/background.jpg";
var ballImg = new Image();
ballImg.src = "imgs/sun.png";
var resetBtnImg = new Image();
resetBtnImg.src = "imgs/reset_btn.png";

// Ensure all images have loaded before starting the game
var numImages = 3;
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
resetBtnImg.onload = function() {
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
  resetBall();
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

  // Check if we clicked the reset button
  if (x >= resetBtnX && x <= resetBtnX + resetBtnW &&
      y >= resetBtnY && y <= resetBtnY + resetBtnH) {
    // if so, reset game
    resetBall();
  }
  // Check if we clicked the ball
  if (x >= ballX && x <= ballX + ballDiam &&
      y >= ballY && y <= ballY + ballDiam) {
    // If so, reverse its direction
    ballVx = -ballVx;
    ballVy = -ballVy;
  }
};
canvas.addEventListener('mousedown', onCanvasMouseDown);

// Code that handles key presses
var onCanvasKeyDown = function(e) {
  // Uncomment this log statement to figure out which keys have which keyCode
  // console.log(e.keyCode);

  // Reset ball movement when 'r' key is pressed
  if (e.keyCode === 82) {
    resetBall();
  }
};
window.addEventListener('keydown', onCanvasKeyDown);



//------------------------------------//
//---------- MAIN GAME LOOP ----------//
//------------------------------------//
var updateGame = function() {
  // Draw the background image
  context.drawImage(bgImg, 0, 0, width, height);

  // Move game objects (just the ball in this case)
  ballX += ballVx;
  ballY += ballVy;
  if (ballX < 0 || ballX + ballDiam > width) {
    ballVx = -ballVx;
  }
  if (ballY < 0 || ballY + ballDiam > height) {
    ballVy = -ballVy;
  }

  // Draw images corresponding to game objects and button
  context.drawImage(ballImg, ballX, ballY, ballDiam, ballDiam);
  context.drawImage(resetBtnImg, resetBtnX, resetBtnY, resetBtnW, resetBtnH);
  // Write a message on the screen
  context.font = "30px Arial";
  context.fillStyle = "yellow";
  context.fillText("Here comes the sun!", 200, 30);

  // Wait 25 milliseconds before starting next game frame
  setTimeout(updateGame, 25);
};
