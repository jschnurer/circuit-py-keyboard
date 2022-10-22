# circuit-py-keyboard
A circuit python script to read buttons as keypresses
The script (`code.py`) reads in a file named `keys.txt`.

# Keys.txt format
Each line should have up to 4 keys in it separated by commas.
There should be a comma at the end as well.
The currently active profile should have ! at the start of the line.

The keys should appear in this order:
1. BackLeft button
2. BackRight button
3. FrontLeft button
4. FrontRight button

Example: 

!R,F,S,L,

If you want to skip one of the buttons, put _ in its place.
There should be no whitespace of any kind on the line.

Also, define which pins the buttons are connected to.
Example:

:14,15,13,

See `keys.txt` for an example file.
