# Mix-up Analysis Web App

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

A web app to more easily create [mix-up analyses](https://wavu.wiki/t/Template:Mixup) for [Wavu Wiki](https://wavu.wiki/t/Main_Page). 
Based on the work done by [RodgerDodger](https://wavu.wiki/t/User:RogerDodger).

## Installation

Requires [Node.js](https://nodejs.org/en) and [Python 3](https://www.python.org/) be installed on your system.

```bash
git clone TODO:
cd mixup-analysis-app

# Start backend server at http://localhost:8000/
cd backend
python3 -m pip install -r requirements.txt
python3 main.py

# Build frontend
cd frontend
npm install
npm run build

# Preview frontend
npm run preview
```

You should be able to view the website at [http://localhost:4173/](http://localhost:4173/).