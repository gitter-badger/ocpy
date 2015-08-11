"""
This script downloads 1GB of the bock11 dataset from OCP.
"""

import ocpaccess.download

downloaded_files = ocpaccess.download.get_data(
                            token="kasthuri11",     resolution=1,
                            x_start=4000,           x_stop=6000,
                            y_start=4000,           y_stop=6000,
                            z_start=3200,           z_stop=3450,
                            location="bock11_sample")
