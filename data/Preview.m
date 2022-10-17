%% Dumbass function that will plot my shit
function output = Preview(RCS, shift, lim)

    close('all')

    % Shift data
    
    RCS = shiftData(RCS, shift)
    
    % Plot global RCS
    plotGlobalRCS(RCS, 'caxis', lim);

    % Plot RCS cuts
    plotRCS(extractData(RCS, 'frq', 5), 'polar', 'copol', 'caxis', lim);
    plotRCS(extractData(RCS, 'frq', 5), 'copol', 'caxis', lim);

end