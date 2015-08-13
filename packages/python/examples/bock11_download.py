"""
This script downloads 1GB of the bock11 dataset from OCP.
"""

import ocpaccess.download

downloaded_files, failed_files = \
        ocpaccess.download.get_data(
                            token="bock11",        resolution=4,
                            x_start=3000,           x_stop=3010,
                            y_start=3000,           y_stop=3010,
                            z_start=3100,           z_stop=3150,
                            location="bock11_sample")
