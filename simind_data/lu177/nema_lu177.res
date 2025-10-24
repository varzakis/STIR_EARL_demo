


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: nema_lu177        
 Phantom B : bone      BackScatt.: pmt       OutputFile: nema_lu177        
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: nema_lu177_src    
 Cover.....: al        ScoreRout.: scattwin  DensityImg: nema_lu177_dns    
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 927500         
 EnergyResolution...: 12           Spectra   Activity..........: 11071          
 MaxScatterOrder....: 3            gi-megp   DetectorLenght....: 20             
 DetectorWidth......: 27           SPECT     DetectorHeight....: 0.9525         
 UpperEneWindowTresh: 312          x-rays    Distance to det...: 16.831         
 LowerEneWindowTresh: 104          BScatt    ShiftSource X.....: 0              
 PixelSize  I.......: 0.44167      Random    ShiftSource Y.....: 0              
 PixelSize  J.......: 0.44167      Cover     ShiftSource Z.....: 0              
 HalfLength S.......: 28.266       Phantom   HalfLength P......: 28.266         
 HalfWidth  S.......: 28.266       Resolut   HalfWidth  P......: 28.266         
 HalfHeight S.......: 28.266       Header    HalfHeight P......: 28.266         
 SourceType.........: Integer2Map            PhantomType.......: Integer2Map  
------------------------------------------------------------------------------
 GENERAL DATA
 keV/channel........: 1                      CutoffEnergy......: 0              
 Photons/Bq.........: 0.2264                 StartingAngle.....: 0              
 CameraOffset X.....: 0                      CoverThickness....: 0.1            
 CameraOffset Y.....: 0                      BackscatterThickn.: 10             
 MatrixSize I.......: 128                    IntrinsicResolut..: 0.55           
 MatrixSize J.......: 128                    AcceptanceAngle...: 2.96094        
 Emission type......: 2                      Initial Weight....: 2702.3744      
 NN ScalingFactor...: 1                      Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: nema_lu177.cor
                                                                              
 COLLIMATOR DATA FOR ROUTINE: Analytical          
 CollimatorCode.....: gi-megp                CollimatorType....: Parallel 
 HoleSize X.........: 0.3                    Distance X........: 0.105          
 HoleSize Y.........: 0.34641                Distance Y........: 0.26414        
 CenterShift X......: 0.2025                 X-Ray flag........: T              
 CenterShift Y......: 0.35074                CollimThickness...: 5.8            
 HoleShape..........: Hexagonal              Space Coll2Det....: 0              
 CollDepValue [57]..: 0                      CollDepValue [58].: 0              
 CollDepValue [59]..: 0                      CollDepValue [60].: 0              
                                                                              
 IMAGE-BASED PHANTOM DATA
 RotationCentre.....:  65, 65                Bone definition...: 1170           
 CT-Pixel size......: 0.44167                Slice thickness...: 0.44166        
 StartImage.........: 1                      No of CT-Images...: 128            
 MatrixSize I.......: 128                    CTmapOrientation..: 0              
 MatrixSize J.......: 128                    StepSize..........: 0.44167        
 CenterPoint I......: 65                     ShiftPhantom X....: 0              
 CenterPoint J......: 65                     ShiftPhantom Y....: 0              
 CenterPoint K......: 65                     ShiftPhantom Z....: 0              
                                                                              
------------------------------------------------------------------------------
  Scattwin results: Window file: nema_lu177.win      
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    101.7 - 124.3   1.000
   2       0    187.2 - 228.8   1.000
   3       0    156.4 - 183.6   1.000
   4       0    229.4 - 258.6   1.000
   5       0     67.5 -  82.5   1.000
   6       1     67.5 -  82.5   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.321E+07 0.201E+07 0.120E+07 0.167E+01 0.626E+00 0.241E+01
   2   0.224E+07 0.748E+06 0.149E+07 0.501E+00 0.334E+00 0.169E+01
   3   0.105E+07 0.100E+07 0.509E+05 0.197E+02 0.952E+00 0.793E+00
   4   0.470E+05 0.154E+05 0.316E+05 0.489E+00 0.328E+00 0.354E-01
   5   0.116E+07 0.104E+07 0.117E+06 0.891E+01 0.899E+00 0.871E+00
   6   0.116E+07 0.104E+07 0.117E+06 0.891E+01 0.899E+00 0.871E+00
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   4   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   5   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   6   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   43.9% 33.4% 22.7%
   2   85.1% 13.5%  1.4%
   3   58.5% 33.4%  8.1%
   4   76.2% 20.3%  3.5%
   5   17.1% 36.0% 46.9%
   6   17.1% 36.0% 46.9%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.1728E+06     
 MaxValue projection: 254.9          
 CountRate spectrum.: 0.1220E+06     
 CountRate E-Window.: 0.6672E+05     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.75013        
 Scatter/Total......: 0.63638        
 Scatter order 1....: 52.16 %        
 Scatter order 2....: 32.56 %        
 Scatter order 3....: 15.28 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4941         
 Efficiency spectrum: 0.9038         
 Sensitivity Cps/MBq: 6.0262         
 Sensitivity Cpm/uCi: 13.3781        
                                                                              
 Simulation started.: 2025:10:24 12:46:53
 Simulation stopped.: 2025:10:24 12:50:03
 Elapsed time.......: 0 h, 3 m and 10 s
 DetectorHits.......: 2743268        
 DetectorHits/CPUsec: 14498          
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: nema_lu177.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: nema_lu177 nema_lu177 /NN:1/FI:lu177/CC:GI-MEGP/PX:0.44166998863220214
