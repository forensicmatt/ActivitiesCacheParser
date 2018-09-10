import re
import sys
import ujson
import pytsk3
import logging
import argparse
sys.path.append("..")
from winactivities.activities import ActivitiesDb
from winactivities.helpers import CustomStringFormatter
from winactivities.logical import VolumeProcessor

VALID_DEBUG_LEVELS = ["ERROR", "WARN", "INFO", "DEBUG"]
__VERSION__ = "0.0.1"


def set_debug_level(debug_level):
    if debug_level in VALID_DEBUG_LEVELS:
        logging.basicConfig(
            level=getattr(logging, debug_level)
        )
    else:
        raise (Exception("{} is not a valid debug level.".format(debug_level)))


def get_arguments():
    usage = u"""Interface to parse Windows Timeline - ActivitiesCache.db.
Run this tool on the database file, or on a logical volume to process records for all users.

(default location - \\Users\\%USERNAME%\\AppData\\Local\\ConnectedDevicesPlatform\\L.%USERNAME%)

version: {}
""".format(__VERSION__)

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    arguments.add_argument(
        "-s", "--source",
        dest="source",
        action="store",
        required=True,
        help="The activities database or a logical volume (logical volume: \\\\.\\C:)."
    )
    arguments.add_argument(
        "-t", "--temp_dir",
        dest="temp_dir",
        action="store",
        required=False,
        default=None,
        help="The template directory for extractions if source is a logical volume."
    )
    arguments.add_argument(
        "--sequence",
        dest="sequence",
        action="store",
        type=int,
        required=False,
        default=0,
        help="Only display sequences above this value. (default: 0)"
    )
    arguments.add_argument(
        "-o", "--output_template",
        dest="output_template",
        action="store",
        required=False,
        default=None,
        help="Output template format."
    )
    arguments.add_argument(
        "--dump_db",
        dest="dump_db",
        action="store_true",
        required=False,
        default=False,
        help="Dump the entire ActivitiesCache.db database, not just the Activity table."
    )
    arguments.add_argument(
        "--debug",
        dest="debug",
        action="store",
        default="ERROR",
        choices=VALID_DEBUG_LEVELS,
        help="Debug level [default=ERROR]"
    )

    return arguments


def parse_file(options, formatter):
    activities_db = ActivitiesDb(
        options.source
    )
    if options.dump_db:
        for record in activities_db.iter_records():
            formatted_record = record.as_ordered_dict()
            formatted_record["_table"] = record._table
            if formatter:
                output = formatter.format(
                    options.output_template, **formatted_record
                )
                print(output)
            else:
                print(ujson.dumps(
                    formatted_record
                ))
    else:
        sequence = activities_db.get_activity_sequence()
        logging.info("Activity Sequence: {}".format(sequence))

        for record in activities_db.iter_activities(options.sequence):
            formatted_record = record.as_ordered_dict()
            if formatter:
                output = formatter.format(
                    options.output_template, **formatted_record
                )
                print(output)
            else:
                print(ujson.dumps(
                    formatted_record
                ))


def parse_logical(options):
    tsk_img = pytsk3.Img_Info(
        options.source
    )
    processor = VolumeProcessor(
        tsk_img, description=options.source,
        temp_location=options.temp_dir,
        output_template=options.output_template,
        dump_db=options.dump_db
    )
    processor.process()


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    formatter = None
    if options.output_template:
        formatter = CustomStringFormatter()

    set_debug_level(options.debug)

    if re.match('\\\\\\\.\\\[a-zA-Z]:', options.source):
        parse_logical(options)
    else:
        parse_file(options, formatter)


if __name__ == "__main__":
    main()
