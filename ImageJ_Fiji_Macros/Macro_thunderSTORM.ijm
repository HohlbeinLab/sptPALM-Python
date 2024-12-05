// Macro for localisation analysis in ImageL/Fiji
// CB 09.04.2021, latest update: 07.09.2021, KS
// latest update: 21.11.2024, JH
// note, this macro requires some additional macros/functions such as thunderSTPORM-phasor and FTM2
// to install all required software: => ImageJ/Fiji => Help => Update... => Manage Update sites => tick the box for HohlbeinLab and restart ImageJ/Fiji


// open file(s) for processing
print("Macro Started");
#@ File[] files
print("Number of files selected:  ", files.length);

// remove some frames to avoid having too many molecules on
remove_frames = true //select true or false
no_frames_remove = 500 // number of initial frames to remove

// check whether to perform Fast Temporal Medium filtering
perform_FTM2 = true //select true or false
window_size = 50 //number of consectutive frames to calculate the median from 

// select fit_option and some parameters (check belopw for further parameters!)
fit_option = "Phasor" // use "Phasor" or "MLE"
pixel_size = 106 // effective camera pixel size in nanometer

for (i = 0; i < files.length; i++) {
	path = files[i];

	open(path); // open the file
	dir = File.getParent(path);
	name = File.getName(path);
	name_reduced = substring(name, 0, lastIndexOf(name, "."));
	print("Path: ", path);
	print("Name: ", name_reduced);
	print("Directory: ", dir);

	if (removeFrames == true){
		print("remove initial frames...");
		run("Slice Remover", "first=1 last="+no_frames_remove+" increment=1");
	}

	if (performFTM2 == true){
		print("run fast temporal median filter...");
		run("Use Opened Image and Run", "window="+window_size+" begin=1 end=0 file=tif show output=[]");
	}

	// run ThunderSTORM to localise the fluorophores
	// JH 2022-10-26: threshold 20 seems to be okay when MedianFilter is off, otherwise use 10 or 12 (now: std(Wave.F1)*1.2)
	print("run ThunderSTORM...");
	run("Camera setup", "readoutnoise=0.0 offset=414.0 quantumefficiency=1.0 isemgain=false photons2adu=3.6 pixelsize="+pixel_size+);

	if(FitOption == "MLE"){
		print("run ...MLE");
		run("Run analysis", "filter=[Difference-of-Gaussians filter] sigma2=8.0 sigma1=2.0 detector=[Local maximum] connectivity=8-neighbourhood threshold=std(Wave.F1)*1.2 estimator=[PSF: Gaussian] sigma=1.5 fitradius=4 method=[Maximum likelihood] full_image_fitting=false mfaenabled=false renderer=[Averaged shifted histograms] pickedlut=CET-L17 magnification=10.0 colorize=false threed=false shifts=2 repaint=50");
		
		// [optional] x,y drift correction
		// run("Show results table", "action=drift magnification=5.0 method=[Cross correlation] ccsmoothingbandwidth=0.25 save=false steps=10 showcorrelations=false");
		
		// Filtering based on width of Gaussfit and intensities
		run("Show results table", "action=filter formula=[sigma <250 & sigma >70 & intensity < 8000 & intensity > 250]");
		}
	else if (FitOption == "Phasor"){
		print("run ...Phasor");
		// Hohlbein lab standard
		// run("Run analysis", "filter=[Difference-of-Gaussians filter] sigma2=8.0 sigma1=2.0 detector=[Local maximum] connectivity=8-neighbourhood threshold=std(Wave.F1)*1.2 estimator=[Phasor-based localisation 2D] fitradius=4 renderer=[Averaged shifted histograms] magnification=10.0 colorize=false threed=false shifts=2 repaint=50");
		// run("Show results table", "action=filter formula=[intensity < 8000 & intensity > 250]");
		run("Run analysis", "filter=[Difference-of-Gaussians filter] sigma2=8.0 sigma1=2.0 detector=[Local maximum] connectivity=8-neighbourhood threshold=std(Wave.F1)*1.5 estimator=[Phasor-based localisation 2D] fitradius=4 renderer=[Averaged shifted histograms] magnification=10.0 colorize=false threed=false shifts=2 repaint=50");
		run("Show results table", "action=filter formula=[intensity < 80000 & intensity > 250]");
		}
	else{
		print("Not running ThunderSTORM: wrong option chosen!");	
		}
 
	// save thunderSTORM CSV table in current folder
	print("save ThunderSTORM data...");
	NewPathTable = dir + File.separator + name_reduced + "_" + FitOption + "_thunder.csv";
	print("NewPathTable: ", NewPathTable);
	run("Export results", "floatprecision=5 filepath=["+NewPathTable+"] fileformat=[CSV (comma separated)] intensity=true offset=true saveprotocol=true x=true sigma2=true y=true sigma1=true z=true bkgstd=true id=true frame=true");

	// save image with localisations in current folder
	selectWindow("Averaged shifted histograms");
	NewPathImage_AveragHisto = dir + File.separator + name_reduced + "_AverageHisto.tif";
	saveAs("png", NewPathImage_AveragHisto);
	
	// close table movie when more than filee was selected
	if(files.length >1){
		//closes all windows
		close("*");
	}
	
}
print("Macro completed!");