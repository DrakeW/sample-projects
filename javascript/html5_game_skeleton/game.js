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
// Create mapping from image names to objects
var imgs = {};
var addImg = function(name, src) {
  imgs[name] = new Image();
  imgs[name].src = src;
  imgs[name].onload = function() {
    imageLoaded();
  }
  numImages++;
};
// Ensure all images have loaded before starting the game
var numImages = 0;
var numLoaded = 0;
var imageLoaded = function() {
  numLoaded++;
  if (numLoaded === numImages) {
    initGame();
  }
};
// Define images
addImg('bg', 'imgs/background.jpg');
//
// ADD MORE IMAGES HERE!!!
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
  context.drawImage(imgs['bg'], 0, 0, width, height);

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
