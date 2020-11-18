# 🔊 Play sounds while and after shell jobs complete

`onhold` is a command-line utility that allows you to play music while a long job completes.

[`ding`](https://github.com/alexdelorenzo/ding) is command-line utility that will play a sound after a long job completes.

Both utilities will take data that is piped into their standard inputs and pipe it to standard output. That is to say that data piped into `onhold` and [`ding`](https://github.com/alexdelorenzo/ding) will be piped right back out.

```bash
$ echo "Hello!" | onhold
Hello!
```

As a result, you can build pipelines with `onhold` and [`ding`](https://github.com/alexdelorenzo/ding).

For example, you can download an ISO with [`http`](https://httpie.org/), visualize the progress with [`pv`](http://www.ivarch.com/programs/pv.shtml), play music with `onhold` while writing to `/dev/null`, and when it's finished, play a sound with [`ding`](https://github.com/alexdelorenzo/ding).

```bash
$ export URL="https://releases.ubuntu.com/20.04.1/ubuntu-20.04.1-desktop-amd64.iso"
$ http "$URL" | pv | onhold | ding > /dev/null
```

This project uses [`play_sounds`](https://github.com/alexdelorenzo/play_sounds), a wrapper over [`playsound`](https://pypi.org/project/playsound/) and [`boombox`](https://pypi.org/project/boombox/).

## `onhold`

You can either set the `$ONHOLD` environment variable to the song you'd like to play, or supply the song with the `-s` flag.

```bash
$ export ONHOLD="~/Music/song.mp3"
$ pv /dev/zero | onhold > /dev/null
```

This allows you to set `$ONHOLD` in your `~/.bashrc`.

You can also specify it with a flag.

```bash
$ pv /dev/zero | onhold -s song.mp3 > /dev/null
```

`onhold` comes with a default song that will play if neither `$ONHOLD` or `-s` are set. You can use the `-w` flag to show warnings if `$ONHOLD` or `-s` are not set.

```bash
$ echo "Hello!" | onhold
Hello!
```

## [`ding`](https://github.com/alexdelorenzo/ding)

You can either set the `$DING` environment variable to the sound you'd like to play, or supply the sound with the `-s` flag.

```bash
# You can run ding after a command or as part of a pipeline
$ export DING="~/Music/ding.ogg"
$ sleep 5; ding
$ echo "Hello!" | ding
Hello!
```

This allows you to set `$DING` in your `~/.bashrc`.

You can also specify it with a flag.

```bash
$ echo "Hello!" | ding -s ding.ogg
Hello!
```

[`ding`](https://github.com/alexdelorenzo/ding) comes with a default sound that will play if neither `$DING` or `-s` are set. You can use the `-w` flag to show warnings if `$DING` or `-s` are not set.

```bash
$ echo "Hello!" | ding
Hello!
```

### [`ding`](https://github.com/alexdelorenzo/ding) is its own package, too
You can install [`ding`](https://github.com/alexdelorenzo/ding) by itself. Future versions of `onhold` will not ship with [`ding`](https://github.com/alexdelorenzo/ding). [Click here to visit `ding`'s project page with installation instructions.](https://github.com/alexdelorenzo/ding)

# Installation
## Dependencies
 - A Unix shell like Bash
 - Python 3.6+
 - `requirements.txt`

### Linux
You'll need to install GStreamer on Linux, or the `play` binary from `sox`.
 
#### Ubuntu
On Ubuntu, you will need to install `PyGObject`, `gstreamer1.0-python3-plugin-loader` and `python3-gst-1.0`.

```bash
$ sudo apt install python3-gi gstreamer1.0-python3-plugin-loader python3-gst-1.0
```

#### Arch
On Arch, you can install `onhold` and its prerequisites [directly from the AUR](https://aur.archlinux.org/packages/onhold/). Thanks, [@jfrcom](https://github.com/jfrcom)!

```bash
$ yay -S onhold # replace yay with your aur helper
```

## PyPI
```bash
$ python3 -m pip install onhold
```

## GitHub
```bash
$ python3 -m pip install -r requirements.txt
$ python3 setup.py install
```

# Help
## `onhold`
```bash
$ onhold --help
Usage: onhold [OPTIONS]

  Play the specified sound file while data is passed in through standard
  input and passed through standard output.

Options:
  -s, --sound_path PATH  Path to sound to play.
  -w, --warn             Show warnings.
  --help                 Show this message and exit.
```

## `ding`
```bash
$ ding --help
Usage: ding [OPTIONS]

  Play specified sound after job is complete.

Options:
  -s, --sound_path PATH  Path to sound to play.
  -w, --warn             Show warnings.
  --help                 Show this message and exit.
```

# License
See `LICENSE`. If you'd like to use this project with a different license, please get in touch.
