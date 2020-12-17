# plot_monthly_gifs

Python xarray plotting routine for producing a contact sheet of animated GIFs from ERA5 netCDFs using total precipitation as an example.

* monthly gif generator
* xarray plotting routine
* converted GIF --> MP4 recording

## Contents

* `quickplot_nc.py` - netcdf reader and GIF plotting routine
* `quickplot_nc_monthly.py` - xarray plotting routine for producing a contact sheet of animated GIFs

The first step is to clone the latest plot_monthly_gifs code and step into the check out directory: 

    $ git clone https://github.com/patternizer/plot_monthly_gifs.git
    $ cd plot_monthly_gifs

### Using Standard Python

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested 
in a conda virtual environment running a 64-bit version of Python 3.8.3.

plot_monthly_gifs scripts can be run from sources directly, once the dependencies are resolved. You will need to download the ERA5 datasets from the Copernicus Climate Data Store (C3S CDS): 

ERA5 1950-1978: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means-preliminary-back-extension?tab=overview
ERA5 1979-2020: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=overview

For each dataset you will need to run:

    $ python quickplot_nc.py

then:

    $ python quickplot_nc_monthly.py

To convert the animated GIF contact sheet to MP4 use ffmpeg at the command line as follows:

$ ffmpeg -i tp.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" tp.mp4

## License

plot_monthly_gifs.py is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)

