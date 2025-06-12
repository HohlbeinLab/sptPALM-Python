// Towards creating movies showing tracks (localisations obtained with ThunderSTORM) 
// on top of a brightfield-microscopy picture
// LAst chenge: 12.06.2025, JH

// make sure that the coordinates of the brightfield file are given in nm: 
// Fiji => Image => Adjust Coordinates => Image Coordinates:
// multiply 1000 to go from µm to nm, for a specific file:

Pixel_nm = 119; //used to rescale the brightfield images from pixels/µms to nm
nCopies = 10000; //prepare a stack of nCopies of the brightfield image
frame_time = 10; //probably not necessary, frame time in ms between the frames of the stack

// Open processed brightfield files(s)
#@ File[] files
print("Number of files selected:  ", files.length);

for (ii = 0; ii < files.length; ii++) {
	path = files[ii];
	print("file: ", ii, " " , path);

	open(path); // open the file
	dir = File.getParent(path);
	name = File.getName(path);
	print("Path:", path);
	print("Name:", name);
	print("Directory:", dir);
	
	// Fast stack creation of N identical copies of the brightfield image
	// Get original image as ImageProcessor
	original = getImageID();
	width = getWidth();
	height = getHeight();

	// Create a new empty stack
	newImage("Stack", "8-bit black", width, height, nCopies);
	Stack.setDimensions(1, 1, nCopies); // 1 channel, 1 slice, nCopies time frames
	newID = getImageID();

	// Copy pixels only once and reuse them
	selectImage(original);
	run("Select All");
	run("Copy");

	selectImage(newID);
	for (jj = 1; jj <= nCopies; jj++) {
    	Stack.setPosition(1, 1, jj)
    	run("Paste");
	}
	
	// Make sure that the pixel callibration is correct:
	run("Properties...", "unit=nm pixel_width="+Pixel_nm+" pixel_height="+Pixel_nm+" frame=["+frame_time+" ms]");
	
	//Save new stack
	print("save stacked brightfield image...");
	savename_stack = replace(name, ".tif", "_stacked.tif");  // new name for image
	NewPathImage_stack = dir + File.separator + savename_stack;
	print("NewPathImage: ", NewPathImage_stack);
	saveAs("Tiff", NewPathImage_stack);
}

// Fiji alsready contains the plugin -> Tracking -> 'TrackMate'
// make sure the update site 'TrackMate CSV importer' has been selected

 run("TrackMate CSV importer");
// CSV file should be the ThunderStorm output
// target image should be the brightfield stack 
// compute all feature: option not ticked
// import tracks: option not ticked
// Radius: set to 1000 nm (not really sure what it does)
// => press 'import', will take a few seconds
// new window will pop up,
// all locs will be selected unless '+' is pressed to select and filter the data (e.g. for certain frames)
// => press 'next'
// next page: select tracker "Simple LAP tracker"
// => press 'next'
// tracker options (similar to what is used in sptPALM-python: 
//		link max distance: 800 nm
//		gap closing distance: 800 nm
//		gap closing frame: 1
// press 'next' and start tracking (look for 'Found XXX tracks')
// press 'next' and, if required, add additional filters for the tracks (e.g., minimum duration)
// press 'next' and select display options (keep 'display spots' and 'display tracks' checked
// 		=> change 'show entire tracks' into 'show tracks backward in time'
//		=> uncheck 'fade tracks in time'
// press 'next' a few times until you arrive at 'select an action'
// 		=> select 'capture overlay'
//		=> press execute and select a range of frames (computation will take a long time for, say 10000 frames)
// new stack can be saved as *.avi etc.
