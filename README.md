# Win Cap
A simple library that can capture an image from a window,
Designed to be used with OpenCV so that a steady stream of capture material can be fed.
Useful if you are trying to use template matching.
**THIS PROJECT IS ONLY FOR WINDOWS**

## Usage
```python
from win_cap import Window

# Get window object, if window cannot be found, then use entire screen
window = Window(window_title="Task Manager", scalar=1.25)

# Returns an image in the form of a numpy array so it can be fed into cv2
window.screen_shot()

# Returns a list of tuples containing the hex code and the window title
window_titles = Window.get_window_titles()
```
The `Window` class takes in two parameters, `window_title` and a `scalar`.
`window_title` is used to find the window that is trying to be captured.
Looks through the available windows on the system and attempts to attach to them.
If no window titles match the passed in value, then the entire screen is captured.
The `scalar` parameter is needed for users that have a high resolution display.
For example, I have a 1440p display and in the windows settings, my text is scaled up by 25% (125%) in the windows settings.
In order for the window to be captured properly, I would need to pass in a scalar value of 1.25.
By default, the `scalar` = 1.0.

You can also run the command line tool. This is used to simply the image that is being captured by the `Window` class.
It repeatedly calls the `screen_shot()` method and displays in that in a window.
To the user, it will look like a live video of the application that was specified.
```
win_cap -h
usage: win_cap [-h] [--window_title WINDOW_TITLE] [--scalar SCALAR]

Capture screenshots from a window

options:
  -h, --help            show this help message and exit
  --window_title WINDOW_TITLE
                        the window that will be captured. (default: '') to capture entire screen
  --scalar SCALAR       specify the scalar. (default: 1.0)
```

To capture the Task Manager for example, you would run the following in the command line to get an idea of the image that is being captured.
Notice that a value of `1.25` is being passed in as well.
```
win_cap --window "Task Manager" --scalar 1.25
```

## Credits
Original code can be found [here](https://learncodebygaming.com/blog/tutorial/opencv-object-detection-in-games).
Ben did an amazing job in his tutorials. I modified his window capture code slightly so
that it can work for my needs