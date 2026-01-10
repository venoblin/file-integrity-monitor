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
- [Usage](#usage)

## About The Project

This File Integrity Checker automates the process of validating file integrity within a target directory. It functions by calculating the MD5 checksum of files and storing them in a persistent SQLite3 database.

On subsequent scans, the tool compares the current file state against the stored baseline. If a discrepancy is found (indicating a file modification), the user is alerted and presented with the option to update the baseline, effectively "accepting" the new changes. This tool is designed to demonstrate core concepts of Blue Team defense, including integrity verification, baselining, and database interactions.

### Built With

This project was built with the following technologies:

- <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" alt="Python" />
- <img src="https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white" alt="SQLite" />

## Usage

Put usage examples here
