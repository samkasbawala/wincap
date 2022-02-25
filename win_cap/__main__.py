import argparse
import cv2 as cv
import time
from typing import Optional, Sequence
from win_cap import Window


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Capture screenshots from a window")
    parser.add_argument(
        "--window_title",
        default="",
        type=str,
        help="the window that will be captured. (default: '') to capture entire screen",
    )

    parser.add_argument(
        "--scalar",
        default=1.0,
        type=float,
        help="specify the scalar. (default: %(default)s)",
    )

    # Get window title that is passed in as an arg
    args = parser.parse_args(argv)

    # Get the window we want to capture
    window = Window(args.window_title, args.scalar)

    # Keep track of time so we can capture the number of frames per second
    loop_time = time.time()

    # Loop to capture
    while True:

        ss = window.screen_shot()
        # ss = cv.resize(ss, (window.width // 2, window.height // 2))

        cv.imshow("Computer Vision", ss)

        # Print out the frame rate of our capture
        print("FPS {}".format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        # Press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord("q"):
            cv.destroyAllWindows()
            break

    return 0


if __name__ == "__main__":
    exit(main())
