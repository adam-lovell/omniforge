# OmniForge Business Website

I coded my first basic business website by hand with the help of a partner. I am putting this on display to illustrate the progress I've made.

## How to View the Website

### 🌐 Live Website
The website is hosted online and can be accessed at:
**https://omniforgeai.com**

### 📱 Website Features & Navigation

The main website includes several key pages:

1. **Home Page** (`index.html`) - The main landing page featuring:
   - OmniForge branding and mission
   - "THE FUTURE OF AUTOMATED PRODUCTIVITY" tagline
   - Access to the VETRA task optimization tool

2. **VETRA - Task Management** (`vetra.html`) - 
   - Click "OPTIMIZE YOUR TASKS" from the home page
   - Advanced task management using the Eisenhower Matrix
   - Organize tasks by urgency and importance

3. **Learning/Tutoring Services** (`lts/tutoring.html`) - 
   - Professional tutoring services
   - Contact information and payment portal
   - Social media links

4. **Account System** (`login/account.html`) - 
   - User account management

5. **Additional Tools**:
   - **CALYXO** (`calyxo.html`) - Health and calorie tracking
   - **Network Security** - Cybersecurity services

### 🖥️ Local Development

To run the website locally:

1. Clone this repository
2. Open `index.html` in your web browser, or
3. Use a local web server (recommended for full functionality):
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server
   
   # Using PHP
   php -S localhost:8000
   ```
4. Navigate to `http://localhost:8000` in your browser

### 🚀 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6 modules)
- **Hosting**: Firebase Hosting
- **Database**: Google Firestore
- **Domain**: Custom domain (omniforgeai.com)
