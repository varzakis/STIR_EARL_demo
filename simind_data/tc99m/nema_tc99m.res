


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: nema_tc99m        
 Phantom B : bone      BackScatt.: pmt       OutputFile: nema_tc99m        
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: nema_tc99m_src    
 Cover.....: al        ScoreRout.: scattwin  DensityImg: nema_tc99m_dns    
------------------------------------------------------------------------------
 PhotonEnergy.......: 140          tc99m     PhotonsPerProj....: 7458500        
 EnergyResolution...: 12           Spectra   Activity..........: 4877.8         
 MaxScatterOrder....: 3            gi-megp   DetectorLenght....: 20             
 DetectorWidth......: 27           SPECT     DetectorHeight....: 0.9525         
 UpperEneWindowTresh: 210          x-rays    Distance to det...: 16.825         
 LowerEneWindowTresh: 70           BScatt    ShiftSource X.....: 0              
 PixelSize  I.......: 0.22077      Random    ShiftSource Y.....: 0              
 PixelSize  J.......: 0.22077      Cover     ShiftSource Z.....: 0              
 HalfLength S.......: 28.258       Phantom   HalfLength P......: 28.258         
 HalfWidth  S.......: 28.258       Resolut   HalfWidth  P......: 28.258         
 HalfHeight S.......: 28.258       Header    HalfHeight P......: 28.258         
 SourceType.........: Integer2Map            PhantomType.......: Integer2Map  
------------------------------------------------------------------------------
 GENERAL DATA
 keV/channel........: 0.5                    CutoffEnergy......: 0              
 Photons/Bq.........: 0.88524                StartingAngle.....: 0              
 CameraOffset X.....: 0                      CoverThickness....: 0.1            
 CameraOffset Y.....: 0                      BackscatterThickn.: 10             
 MatrixSize I.......: 256                    IntrinsicResolut..: 0.55           
 MatrixSize J.......: 256                    AcceptanceAngle...: 2.96094        
 Emission type......: 2                      Initial Weight....: 578.9409       
 NN ScalingFactor...: 1                      Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: nema_tc99m.cor
                                                                              
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
 RotationCentre.....: 129,129                Bone definition...: 1170           
 CT-Pixel size......: 0.22077                Slice thickness...: 0.22077        
 StartImage.........: 1                      No of CT-Images...: 256            
 MatrixSize I.......: 256                    CTmapOrientation..: 0              
 MatrixSize J.......: 256                    StepSize..........: 0.44167        
 CenterPoint I......: 129                    ShiftPhantom X....: 0              
 CenterPoint J......: 129                    ShiftPhantom Y....: 0              
 CenterPoint K......: 129                    ShiftPhantom Z....: 0              
                                                                              
------------------------------------------------------------------------------
  Scattwin results: Window file: nema_tc99m.win      
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    114.0 - 126.0   1.000
   2       0    126.5 - 154.6   1.000
   3       1    126.5 - 154.6   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.380E+07 0.353E+07 0.273E+06 0.129E+02 0.928E+00 0.649E+01
   2   0.121E+08 0.467E+07 0.742E+07 0.629E+00 0.386E+00 0.207E+02
   3   0.121E+08 0.467E+07 0.742E+07 0.629E+00 0.386E+00 0.207E+02
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   58.2% 33.3%  8.6%
   2   81.3% 16.6%  2.2%
   3   81.3% 16.6%  2.2%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.2929E+06     
 MaxValue projection: 219.1          
 CountRate spectrum.: 0.2433E+06     
 CountRate E-Window.: 0.2339E+06     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 2.3914         
 Scatter/Total......: 0.70514        
 Scatter order 1....: 44.09 %        
 Scatter order 2....: 34.16 %        
 Scatter order 3....: 21.75 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.9062         
 Efficiency spectrum: 0.9426         
 Sensitivity Cps/MBq: 47.9554        
 Sensitivity Cpm/uCi: 106.461        
                                                                              
 Simulation started.: 2025:10:24 14:13:04
 Simulation stopped.: 2025:10:24 14:37:31
 Elapsed time.......: 0 h, 24 m and 27 s
 DetectorHits.......: 21961545       
 DetectorHits/CPUsec: 14977          
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: nema_tc99m.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: nema_tc99m nema_tc99m /NN:1/FI:tc99m/CC:GI-MEGP/PX:0.220770001411438
