activate base;
conda install conda-build anaconda-client;
conda config --set anaconda_upload yes;
Write-Host "Python Version: $args";
conda build --token %CONDA_UPLOAD_TOKEN% --python $args -c usgs-astrogeology recipe;
