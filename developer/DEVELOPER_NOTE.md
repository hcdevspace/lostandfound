This is the developer folder for testing and demo purposes.

## Recording Commands

Instructions are stored in `instructions.json` as an array under the `instructions` key.

### click
```json
{ "type": "click", "start": { "x": 0, "y": 0 }, "end": { "x": 0, "y": 0 }, "target": "tag#id.cls \"text\"" }
```
Recorded on mouseup. `start` is the position of mousedown, `end` is the position of mouseup. `target` describes the element that received mousedown: tag name, id, up to 3 CSS classes, and up to 50 characters of visible text.

### type
```json
{ "type": "type", "text": "hello\n" }
```
Recorded when inside a text input or textarea. Characters accumulate until the mouse moves away from the element or Enter is pressed. If Enter triggered the commit, a `\n` is appended to the text. Backspace removes the last character from the accumulation buffer.

### scroll
```json
{ "type": "scroll", "amount": 120, "position": { "x": 0, "y": 0 } }
```
Recorded after scrolling stops (debounced 250ms). `amount` is pixels scrolled since the last scroll instruction. `position` is the final scroll offset of the window. Always preceded by a `move` instruction capturing the mouse position at scroll start.

### move
```json
{ "type": "move", "position": { "x": 0, "y": 0 } }
```
Recorded automatically just before a scroll sequence begins. Captures where the mouse cursor was at the moment scrolling started. Not emitted for any other reason.

## Stopping a Recording

Press **Esc** at any time to stop recording. The current instructions are saved to `instructions.json` immediately. Alternatively click the **■ Stop** button on the toolbar.

## Textbox Mode

After clicking a text input or textarea, the recorder enters textbox mode. While in this mode, mouse movement does **not** produce a new click instruction. The recorder waits for either a real mouse click (exits textbox mode) or a keypress (begins accumulating a type instruction).

