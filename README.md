# Community Models & LoRAs

This repository maintains the source material and publish mechanism for "Community" section of Models and LoRAs in the Draw Things app.

# How to Contribute

You are welcome to put up Pull Requests to add new models and LoRAs to the "Community" section within the app. To add a new model, first create a directory under either `./models` or `./loras` and add the following files:

 1. a `LICENSE` file that contains the license the model was distributed at;

 2. a `metadata.json` file contains the metadata for both the source link (must be public-available) and enough metadata to be used within the app. There are some examples in the directory;

 3. a `assets` directory contains example images for a given model / LoRA.

# How It Works

Once a Pull Request merged into the repository, an automatic process will be kicked off to download model from the source link, convert them into models available to Draw Things the app. A new json list will be generated so the model will be available to everyone use the app upon a refresh.

# License

All materials in this repository are published under [CC0 1.0 Universal](https://creativecommons.org/public-domain/cc0/) otherwise known as "Public Domain".
