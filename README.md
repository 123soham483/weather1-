# WeatherNow Application

A full-stack weather application built with React (Vite) frontend and FastAPI backend. Get real-time weather data, 6-day forecasts, and air quality information for any city worldwide.

## 🚀 Getting Started

Follow these steps to run the project in VS Code.

### Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** and npm - [Download Node.js](https://nodejs.org/)
- **VS Code** - [Download VS Code](https://code.visualstudio.com/)
- **MongoDB Atlas Account** - [Sign up for MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

---

## 📋 Step-by-Step Setup Instructions

### 1. Open the Project in VS Code

1. Open VS Code
2. Click `File` → `Open Folder`
3. Navigate to and select the project folder (`New folder (9)`)
4. Click `Select Folder`

### 2. Configure MongoDB Connection

1. Navigate to the `backend` folder
2. Open the `.env` file (or create one if it doesn't exist)
3. Add your MongoDB credentials:
   ```env
   MONGO_URL=your_mongodb_connection_string_here
   DB_NAME=your_database_name_here
   ```
   
   **Example:**
   ```env
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=weather_db
   ```

### 3. Set Up the Backend

#### 3.1. Open a New Terminal in VS Code
- Click `Terminal` → `New Terminal` (or press `` Ctrl+` ``)
- Make sure you're in the root directory of the project

#### 3.2. Create a Python Virtual Environment
```bash
python -m venv venv
```

#### 3.3. Activate the Virtual Environment
```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate

# On Windows (Command Prompt)
.\venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt.

#### 3.4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages including FastAPI, uvicorn, motor, etc.

#### 3.5. Navigate to the Backend Folder
```bash
cd backend
```

#### 3.6. Start the Backend Server
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Keep this terminal running!** The backend server needs to stay active.

### 4. Set Up the Frontend

#### 4.1. Open a Second Terminal
- Click the `+` button in the terminal panel to open a new terminal
- Or click `Terminal` → `New Terminal`

#### 4.2. Navigate to the Frontend Folder
```bash
cd frontend
```

#### 4.3. Install Node Dependencies
```bash
npm install
```

This will install React, Vite, axios, and other frontend dependencies.

#### 4.4. Start the Frontend Dev Server
```bash
npm run dev
```

You should see output like:
```
  VITE v5.1.4  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 5. Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:5173`
3. You should see the WeatherNow application!

---

## 🎯 Quick Commands Reference

### Backend Commands
```bash
# From project root, activate virtual environment
.\venv\Scripts\Activate  # Windows PowerShell
source venv/bin/activate  # macOS/Linux

# Navigate to backend and start server
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Commands
```bash
# From project root, navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🛠️ Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── server.py           # Main server file
│   └── .env                # Environment variables (MongoDB config)
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: "MONGO_URL not found"**
- Solution: Make sure you've created the `.env` file in the `backend` folder with your MongoDB connection string

**Problem: "Port 8000 already in use"**
- Solution: Find and kill the process using port 8000, or use a different port:
  ```bash
  uvicorn server:app --reload --port 8001
  ```

**Problem: "Module not found" errors**
- Solution: Make sure your virtual environment is activated and run:
  ```bash
  pip install -r requirements.txt
  ```

### Frontend Issues

**Problem: "EADDRINUSE: port 5173 already in use"**
- Solution: Vite will automatically try the next available port (5174, 5175, etc.)

**Problem: "Cannot connect to backend"**
- Solution: Make sure the backend server is running on `http://localhost:8000`

**Problem: Dependencies not installing**
- Solution: Delete `node_modules` and `package-lock.json`, then run `npm install` again

---

## 📱 Features

- 🌡️ **Real-time Weather Data** - Current temperature, humidity, wind speed, and more
- 📅 **6-Day Forecast** - Plan ahead with accurate weather predictions
- 💨 **Air Quality Index (AQI)** - Monitor air quality with PM2.5 and PM10 levels
- 🌍 **Global Coverage** - Search weather for any city worldwide
- 🎨 **Modern UI** - Beautiful, responsive design built with React

---

## 🔗 API Endpoints

The backend provides the following API endpoints:

- `GET /api/` - API status check
- `GET /api/weather?city={city_name}` - Get current weather for a city
- `GET /api/forecast?city={city_name}` - Get 6-day forecast for a city
- `POST /api/status` - Create a status check
- `GET /api/status` - Get all status checks

---

## 📄 License

Copyright © 2025 Soham. All rights reserved.

---

## 👤 Author

Created by **Soham**

---

## 🆘 Need Help?

If you encounter any issues:

1. Make sure both terminals are running (backend and frontend)
2. Check that MongoDB connection is configured correctly
3. Verify all dependencies are installed
4. Check the terminal output for error messages

Happy Coding! 🎉
