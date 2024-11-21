//// Macro for cell segmentation in ImageL/Fiji
//JH 28.01.2021, latest update: 21-11-2024: now allows to select different images to peerform segmentation
//note, this macro requires some macros/functions that come with an SCF installation
//to install SCF: => ImageJ/Fiji => Help => Update... => Manage Update sites => tick the box for SCF MPI CBG and restart ImageJ/Fiji

////////////////////////////////
//// open file for processing

print("Macro Started");
#@ File[] files

print("Number of files selected:  ", files.length);

for (i = 0; i < files.length; i++) {
	path = files[i];
	print("file: ", i, " " , path);

	open(path); // open the file
	dir = File.getParent(path);
	name = File.getName(path);
	print("Path:", path);
	print("Name:", name);
	print("Directory:", dir);

////////////////////////////////
////run function for z-projection, averaging over all frames to reduce noise
	print("run z-projection");
	run("Z Project...", "projection=[Average Intensity]");

////////////////////////////////
//// KS added for stability of segmentation and pre-processing the brightield image
	print("run some image processing...");
	getStatistics(area, mean, min, max, std, histogram);
	//print(min);
	run("Subtract...", "value="+min);
	run("Median...", "radius=0.5");
	run("Enhance Contrast...", "saturated=0.1 normalize");
	run("8-bit");

////////////////////////////////
//// save processed brightield image in current folder
	savename_procBrightfield = replace(name, ".tif", "_procBrightfield.tif");  // new name for image
	NewPathImage_procBrightfield = dir + File.separator + savename_procBrightfield;
	print("NewPathImage: ", NewPathImage_procBrightfield);
	saveAs("Tiff", NewPathImage_procBrightfield);

////////////////////////////////
//// run macro for the interactive watershed (cell segmentation)
	print("run cell segmentation...");
// OPTION A: run interactive watershed
//run("Interactive H_Watershed")

//OPTION B: if good seed values are known, run
	hMin = 47.0;		// values are ~40-55 // standard 47
	thresh = 0.0;
	peakFlooding = 100.0;
	run("H_Watershed", "impin=["+getTitle()+"] hmin="+hMin+" thresh="+thresh+" peakflooding="+peakFlooding + " displaystyle=Image outputmask=false allowsplitting=true");

////////////////////////////////
//// save segmented image in current folder
	print("save segmented image...");
	savename_segm = replace(savename_procBrightfield, ".tif", "_segm.tif");  // new name for image
	NewPathImage_segm = dir + File.separator + savename_segm;
	print("NewPathImage: ", NewPathImage_segm);
	saveAs("Tiff", NewPathImage_segm);

////////////////////////////////
//// Identify and export labels of the individual segmentations in current folder
	print("export segmentation data...");
	run("Label analyser (2D, 3D)", "label=[NewPathImage_segm] image=[NewPathImage_segm] area_volume center_of_mass bounding_box eigenvalues aspect_ratio sphericity number_of_touching_neighbors average_distance_of_n_closest_neighbors n_=5 number_of_neighbors_closer_than_distance_d d_=100 table");
	savename_table = replace(savename_segm, ".tif", "_Table.csv");  // new name for table
	NewPathTable = dir + File.separator + savename_table;
	print("NewPathTable: ", NewPathTable);
	saveAs("Results", NewPathTable);
}
	print("Macro Completed");