export PATH="$HOME/miniconda/bin:$PATH"                                             # Set up the miniconda path
conda config --set always_yes yes --set changeps1 no                                # Always say yes to questions
while read requirement; do                                                          # read through all the requirements
  conda install --yes $requirement || pip install $requirement;                     # conda install or pip install
  done < requirements.txt                                                           # get the information from requirements.txt