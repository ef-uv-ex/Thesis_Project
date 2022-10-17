%% Load the data from the active data folder

clc;
clear all;
close all;

% Grab data time
format = 'yyyymmdd';
t = datestr(now, format);


% Move directory
dir_CODE = "G:\Rofrano_Thesis\Project\code";
dir_FIG = "G:\Rofrano_Thesis\Project\figures";
dir_DATA = "G:\Rofrano_Thesis\Project\data";
% dir_CODE = "C:\Users\mattr\OneDrive\Desktop\Target_Boost_with_ML\code";
% dir_FIG = "C:\Users\mattr\OneDrive\Desktop\Target_Boost_with_ML\figures";
% dir_DATA = "C:\Users\mattr\OneDrive\Desktop\Target_Boost_with_ML\data";
cd(dir_DATA);

RCS_CLIM = [-60,20];

%% Import and organize data

% Load exact data
cyl_750_ex = load('cyl750.mat').cyl750;

% Load measured data
% Morning measurements
cyl_750_cal_1 = readLintek('cyl_750.cal');
cyl_900_cal_1 = readLintek('cyl_900.cal');
cyl_mount_1 = readLintek('cyl_mount.cbk');

% Afternoon measurements
cyl_750_cal_2 = readLintek('cyl_750_2.cal');
cyl_900_cal_2 = readLintek('cyl_900_2.cal');
cyl_mount_2 = readLintek('cyl_mount_3.cbk');

% Target measurements
tar_mount = readLintek('tar_mount.bkg');
tar_arrow = readLintek('tar_arrow.tar');
tar_msl_nose1 = readLintek('tar_msl_nose1.tar');
tar_msl_nose2 = readLintek('tar_msl_nose2.tar');
tar_msl_nose3 = readLintek('tar_msl_nose3_2.tar');
tar_msl_nose4 = readLintek('tar_msl_nose4.tar');
tar_msl_nose5 = readLintek('tar_msl_nose5.tar');

%% Save uncalibrated measurements

save('r_cyl750_1', 'cyl_750_cal_1');
save('r_cyl750_exact', 'cyl_750_ex');
save('r_cyl900_1', 'cyl_900_cal_1');
save('r_cyl_mount_1', 'cyl_mount_1');
save('r_cyl750_2', 'cyl_750_cal_2');
save('r_cyl900_2', 'cyl_900_cal_2');
save('r_cyl_mount_2', 'cyl_mount_2');

save('r_tar_mount', 'tar_mount');
save('r_tar_arrow', 'tar_arrow');
save('r_tar_msl_n1', 'tar_msl_nose1');
save('r_tar_msl_n2', 'tar_msl_nose2');
save('r_tar_msl_n3', 'tar_msl_nose3');
save('r_tar_msl_n4', 'tar_msl_nose4');
save('r_tar_msl_n5', 'tar_msl_nose5');

%% Calibrate

tar_arrow = calibrateRCS(tar_arrow, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);
tar_msl_nose1 = calibrateRCS(tar_msl_nose1, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);
tar_msl_nose2 = calibrateRCS(tar_msl_nose2, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);
tar_msl_nose3 = calibrateRCS(tar_msl_nose3, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);
tar_msl_nose4 = calibrateRCS(tar_msl_nose4, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);
tar_msl_nose5 = calibrateRCS(tar_msl_nose5, tar_mount, cyl_750_cal_1, cyl_mount_1, cyl_750_ex);


%% CAll the dumbass preview function

tar_arrow = shiftData(tar_arrow, 3);
tar_msl_nose1 = shiftData(tar_msl_nose1, -42);
tar_msl_nose2 = shiftData(tar_msl_nose2, -37);
tar_msl_nose3 = shiftData(tar_msl_nose3, -32);
tar_msl_nose4 = shiftData(tar_msl_nose4, -33);
tar_msl_nose5 = shiftData(tar_msl_nose5, -32);


%% Save calibrated values

save('c_tar_arrow', 'tar_arrow');
save('c_tar_msl_n1', 'tar_msl_nose1');
save('c_tar_msl_n2', 'tar_msl_nose2');
save('c_tar_msl_n3', 'tar_msl_nose3');
save('c_tar_msl_n4', 'tar_msl_nose4');
save('c_tar_msl_n5', 'tar_msl_nose5');



%% Produce Plots
close('all')

% Plot global RCS
plotGlobalRCS(tar_cal, 'caxis',RCS_CLIM);
plotGlobalRCS(tar_cal, 'caxis',RCS_CLIM);

% Plot RCS cuts in polar format
tar_cal_7 = extractData(tar_cal, 'frq', 10);
plotRCS(tar_cal_7, 'polar', 'copol', 'caxis',RCS_CLIM);
plotRCS(tar_cal_7, 'copol', 'caxis',RCS_CLIM);


%% Load the FEKO data

% cd("G:\Rofrano_Thesis\RCS_Targets\Prolate_Spheroid");
% tar_true = readFeko('mini_arrow_20220823.ffe')

%% Plot the FEKO results
% close('all')
% 
% % Plot global RCS
% plotGlobalRCS(tar_true, 'caxis',RCS_CLIM);
% plotGlobalRCS(tar_true, 'caxis',RCS_CLIM);
% 
% % Plot RCS cuts in polar format
% tar_true_7 = extractData(tar_true, 'frq', 7);
% plotRCS(tar_true_7, 'polar', 'copol', 'caxis',RCS_CLIM);
% plotRCS(tar_true_7, 'copol', 'caxis',RCS_CLIM);
% 
% filename = strcat(t, '_prolate_true');
% save(filename, 'prolate_true');



