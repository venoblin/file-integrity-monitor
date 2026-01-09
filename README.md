<br/>
<div align="center">
<a href="https://github.com/user/repo">
<img src=".readme-images/project-logo.svg" alt="Logo" height="128px">
</a>
<h3 align="center">File Integrity Checker</h3>
<p align="center">
Keep track of any file changes made to your files! 
<br/>
<br/>
</div>

Table of Contents

- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)

## About The Project

About the project, include images here too.

### Built With

This project was built with the following technologies:

- <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" alt="Python" />

## Getting Started

Instructions of setting up project on your local machine.

### Prerequisites

Describe prerequisites and how to complete them, this example we're installing nodemon. To install nodemon do the following:

- Install Nodemon:
  ```sh
  npm install -g nodemon
  ```
  Make sure NPM is installed.
- Verify installation:
  ```sh
  nodemon --version
  ```

### Installation

1. **Clone the repository**

   ```sh
   git clone --recurse-submodules https://github.com/venoblin/scripts
   ```

2. **Create settings file (for [ezdownloadsorter](https://github.com/venoblin/download-file-sorter))**

   ```sh
   cd scripts
   touch settings.json
   ```

3. **Modify `settings.json`**

   ```json
   {
     "downloads": "/path/to/Downloads",
     "destinations": {
       ".file-extension": "/path/to/destination",
       ".file-extension": "/path/to/destination",
       ".file-extension": "/path/to/destination"
     }
   }
   ```

4. **Install scripts**
   ```sh
   ./install.sh
   ```

## Usage

Put usage examples here
