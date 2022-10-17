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
cd(dir_DATA);

RCS_CLIM = [-60,20];


%% Load the FEKO data

cd("G:\Rofrano_Thesis\Project\data"); % From main drive
MSL1 = readFeko('MSL-1.ffe');

% Rotate negative 90 to match the radar inputs
MSL1 = shiftData(MSL1, 90)

%% Testing the output for the correct angles

tar_true_10 = extractData(MSL1, 'frq', 5);
plotRCS(tar_true_10, 'polar', 'copol', 'caxis', RCS_CLIM);


%% Save the thing

cd("G:\Rofrano_Thesis\Project\data")
filename = strcat('MSL-1_s');
save(filename, 'MSL1');


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


