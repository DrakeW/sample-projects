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
var resetX = 10;
var resetY = 10;
var resetW = 159;
var resetH = 38;
// Number of balls
var numBalls = 5;
// Make 5 Balls
var resetGame = function() {
  balls = [];
  for (var i = 0; i < numBalls; i++) {
    var diam = Math.floor(Math.random() * 50) + 50;
    var newBall = {
      diam: diam,
      x: width / 2 - diam / 2,
      y: height / 2 - diam / 2,
      vx: Math.floor(Math.random() * 20) - 10,
      vy: Math.floor(Math.random() * 20) - 10,
    };
    balls.push(newBall);
  }
}

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
var numImages = 2;
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



//-----------------------------------------//
//---------- HANDLING USER INPUT ----------//
//-----------------------------------------//
// Code that handles mouse clicks
var onCanvasClick = function(e) {
  var x = e.layerX;
  var y = e.layerY;
  // Check if we clicked the reset button
  if (x >= resetX && x <= resetX + resetW &&
      y >= resetY && y <= resetY + resetH) {
    resetGame();
  }
  // Check if we clicked one of the balls
  for (var i = 0; i < balls.length; i++) {
    var ball = balls[i];
    if (x >= ball['x'] && x <= ball['x'] + ball['diam'] &&
        y >= ball['y'] && y <= ball['y'] + ball['diam']) {
      ball['vx'] = -ball['vx'];
      ball['vy'] = -ball['vy'];
    }
  }
};
canvas.addEventListener('mousedown', onCanvasClick);



//-----------------------------------------//
//---------- GAME INITIALIZATION ----------//
//-----------------------------------------//
// Initialize game objects and start game loop
var initGame = function() {
  resetGame();
  updateGame();
};



//------------------------------------//
//---------- MAIN GAME LOOP ----------//
//------------------------------------//
var updateGame = function() {
  // Move game objects
  for (var i = 0; i < balls.length; i++) {
    var ball = balls[i];
    ball['x'] += ball['vx'];
    ball['y'] += ball['vy'];
    if (ball['x'] < 0 || ball['x'] + ball['diam'] > width) {
      ball['vx'] = -ball['vx'];
    }
    if (ball['y'] < 0 || ball['y'] + ball['diam'] > height) {
      ball['vy'] = -ball['vy'];
    }
  }

  // Draw images corresponding to game objects
  context.drawImage(bgImg, 0, 0, width, height);
  for (var i = 0; i < balls.length; i++) {
    var ball = balls[i];
    context.drawImage(ballImg, ball['x'], ball['y'], ball['diam'],
                      ball['diam']);
  }
  context.drawImage(resetBtnImg, resetX, resetY, resetW, resetH);
  // Write a message on the screen
  context.font = "30px Arial";
  context.fillStyle = "yellow";
  context.fillText("Here come the suns!", 200, 30);

  // Wait 25 milliseconds before starting next game frame
  setTimeout(updateGame, 25);
};
