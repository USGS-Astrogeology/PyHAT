travis-sphinx -v deploy -b dev
echo "Python version: $1"
conda deactivate
conda install conda-build anaconda-client
conda config --set anaconda_upload yes
conda build --token $CONDA_UPLOAD_TOKEN --python $1 -c usgs-astrogeology recipe
