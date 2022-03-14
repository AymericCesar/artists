N&lD multitrack player - NDMT
===========
This project is based on MT5 - A multitrack HTML5 Player, see [README_old.md](README_old).

It runs on a Python flask server, eventually in a Docker container.
The tracks are not tracked in the repository.

The dirty work of managing the GUI, events, etc is done in `sound.js`... the main clock is in there too. We use requestAnimationFrame in order to measure time by intervals of about 1/60th of a second. Deltas are measured there in order to know "where we are in a song", and be able to jump or restart after a stop or a pause.

Web audio pausing or jumping in a song is way unnatural as the AudioBufferSource nodes can be started and stopped only once. This "fire and forget" approach chosen in web audio for these particular nodes means that we need to rebuild partially the web audio graph at each pause or jump. The play/pause/jump and building of the audio graph is done in the song.js file.
