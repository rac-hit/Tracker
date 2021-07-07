from spreadsheet import yt_data
from metabase import meta
from data_entry import entry
from slack_summary_notfinal import summary
from emtryMul import mulclicks


def main():
    # entry()
    yt_data()
    meta()
    mulclicks()
    # summary()
if __name__ == "__main__":
    main()
