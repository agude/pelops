
import collections
import os

import pelops.datasets.chip as chip
import pelops.utils as utils

# ================================================================================
#  STR_SA Dataset
# ================================================================================


class StrDataset(chip.ChipDataset):
    # define paths to files and directories
    filenames = collections.namedtuple(
        "filenames",
        [
            "dir_all"
        ]
    )
    filepaths = filenames (
        "crossCameraMatches"
    )

    def __init__(self, dataset_path, set_type=None):
        super().__init__(dataset_path, set_type)
        self.__set_filepaths()  # set self.__filepaths
        self.__set_chips()
        # STR does not differentiate the set type

    def __set_filepaths(self):
        self.__filepaths = StrDataset.filenames(
            os.path.join(self.dataset_path, StrDataset.filepaths.dir_all)
        )

    def __set_chips(self):
        directory = self.__filepaths.dir_all
        for file in os.listdir(directory):
            path = os.path.join(directory, file)

            # Only interested in certain files
            is_valid = os.path.isfile(path)
            is_png = path.endswith(".png")
            is_mask = "mask" in path
            if not is_valid or not is_png or is_mask:
                continue

            # Set all Chip variables
            car_id = get_sa_car_id(path)
            cam_id = get_sa_cam_id(path)

            time = None    # No timestamp information
            misc = None    # No miscellaneous information

            # Make chip
            current_chip = chip.Chip(
                path,
                car_id,
                cam_id,
                time,
                misc
            )

            self.chips[path] = current_chip


def int_from_string(string, start_chars, int_len):
    # We only want to use the filename, not the directory names
    base_string = os.path.basename(string)
    loc = base_string.find(start_chars)

    # Not found
    if loc < 0:
        return None

    start = loc + len(start_chars)
    end = start + int_len
    str_num = base_string[start:end]
    return int(str_num)


def get_sa_cam_id(string):
    return int_from_string(string, start_chars="_cam", int_len=2)


def get_sa_car_id(string):
    return int_from_string(string, start_chars="match", int_len=5)
