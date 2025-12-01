---
title: "Complete Guide to Setting Up a Tauri Project with M1 Mac"
date: 2024-11-12 00:00:00 +0900
categories: [Development, Tauri]
tags: [tauri, react, vue, rust, m1-mac, desktop-app]
author: seoultech
image:
  path: /scitechblog/assets/img/posts/tauri-setup/my_tauri_app.png
  alt: Tauri Application Setup
---

## Prerequisites (One-time Setup)

### 1. Development Environment Setup
```bash
# 1. Install Xcode Command Line Tools
xcode-select --install

# 2. Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 3. Apply environment variables
source $HOME/.cargo/env

# 4. Additional setup for M1 Mac users
rustup target add aarch64-apple-darwin
```

## Project Setup

### 1. Create Project Directory
```bash
# Navigate to your preferred location (e.g., Desktop/CSE)
cd ~/Desktop/CSE

# Create and move into project directory
mkdir my-tauri-app
cd my-tauri-app
```

### 2. Initialize Node.js Project
```bash
# Initialize npm
npm init -y

# Install Tauri CLI and API
npm install --save-dev @tauri-apps/cli
npm install @tauri-apps/api
```

### 3. Frontend Setup
```bash
# Choose either React or Vue

# For React
npm create vite@latest . -- --template react

# Or for Vue
npm create vite@latest . -- --template vue

# ⚠️ Important: Select "Ignore files and continue" when prompted!

# Install dependencies
npm install
```

## Project Structure
Your project should look like this:
```
my-tauri-app/
├── node_modules/
├── src-tauri/
│   ├── capabilities/
│   ├── icons/
│   ├── src/
│   │   └── main.rs
│   ├── build.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
├── package.json
└── package-lock.json
```

## Configuration Files

### 1. package.json
```json
{
  "name": "my-tauri-app",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "tauri": "tauri"
  }
}
```

### 2. src-tauri/tauri.conf.json
```json
{
  "identifier": "com.myapp.dev",
  "productName": "my-tauri-app",
  "version": "0.1.0",
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:3000/",
    "frontendDist": "../dist"
  },
  "app": {
    "security": {
      "csp": null
    },
    "windows": [
      {
        "fullscreen": false,
        "height": 600,
        "resizable": true,
        "title": "My Tauri App",
        "width": 800
      }
    ]
  }
}
```

## Running the Project

### 1. Development Mode
Open two terminal windows:

```bash
# Terminal 1: Start frontend server
npm run dev

# Terminal 2: Start Tauri application
npm run tauri dev
```

![Front Server](/assets/img/posts/tauri-setup/my_tauri_app.png)
![Tauri App](/assets/img/posts/tauri-setup/esbuild.png)

## Common Issues and Solutions

### 1. "cargo not found" Error
```bash
# Reinstall Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### 2. Frontend Server Not Starting
Check if you see this message:
```
Warn Waiting for your frontend dev server to start on http://localhost:3000/
```
Solution: Open a new terminal and run `npm run dev`

### 3. Port Conflicts
If port 3000 is in use, modify vite.config.js:
```javascript
export default defineConfig({
  server: {
    port: 3001  // Change to available port
  }
})
```

## Important Notes

1. **Directory Navigation**
   - All npm commands must be run from the project root (my-tauri-app)
   - Cargo commands should be run from src-tauri directory

2. **File Locations**
   - Frontend code goes in src/
   - Rust backend code goes in src-tauri/src/
   - Configuration files stay in src-tauri/

3. **Development Workflow**
   - Always start both frontend server and Tauri app
   - Changes to Rust code require restart
   - Frontend changes hot-reload automatically

4. **M1 Mac Specific**
   - Don't forget the aarch64-apple-darwin target
   - Use recommended Rust version (1.70+)

## Building for Production
```bash
# From project root
npm run tauri build
```
The built application will be in `src-tauri/target/release`

## Troubleshooting Tips

1. **Clean Build**
```bash
cd src-tauri
cargo clean
cd ..
npm run tauri dev
```

2. **Check Dependencies**
```bash
npm install
cd src-tauri
cargo check
```

3. **Verify File Permissions**
```bash
chmod +x src-tauri/target/release/my-tauri-app
```

Following this guide step by step will help you set up a Tauri project successfully. Remember to check the terminal output for any errors and refer to the troubleshooting section if needed.
