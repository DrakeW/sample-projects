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
//
// ADD MORE VARIABLES HERE!!!
//


//---------------------------------------//
//---------- PRELOADING IMAGES ----------//
//---------------------------------------//
// Define images
var bgImg = new Image();
bgImg.src = "imgs/background.jpg";
//
// ADD MORE IMAGES HERE!!!
//

// Ensure all images have loaded before starting the game
var numImages = 1; // CHANGE THIS NUMBER ONCE YOU ADD MORE IMAGES!!!
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
//
// ADD MORE ONLOAD CALLBACKS HERE!!!
//



//-----------------------------------------//
//---------- GAME INITIALIZATION ----------//
//-----------------------------------------//
//
// ADD MORE RESET FUNCTIONS HERE!!!
//
// Initialize game objects and start game loop
var initGame = function() {
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
  //
  // ADD CLICK HANDLING CODE HERE!!!
  //
};
canvas.addEventListener('mousedown', onCanvasMouseDown);

// Code that handles key presses
var onCanvasKeyDown = function(e) {
  // Uncomment this log statement to figure out which keys have which keyCode
  // console.log(e.keyCode);
  //
  // ADD KEYBOARD HANDLING CODE HERE!!!
  //
};
window.addEventListener('keydown', onCanvasKeyDown);



//------------------------------------//
//---------- MAIN GAME LOOP ----------//
//------------------------------------//
var updateGame = function() {
  // Draw the background image
  context.drawImage(bgImg, 0, 0, width, height);

  //
  // ADD GAME LOGIC HERE!!!
  //

  //
  // ADD MORE IMAGE DRAWING HERE!!!
  //

  // Wait 25 milliseconds before starting next game frame
  // This line keeps the game running so it should always run no matter which
  // screen we're looking at
  setTimeout(updateGame, 25);
};
