import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import CadAutomation from './pages/CadAutomation';
import MachineHealth from './pages/MachineHealth';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <Toaster 
        position="top-right"
        toastOptions={{
          className: '',
          style: {
            background: '#192235',
            color: '#f8fafc',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
          },
        }}
      />
      <div className="app-container">
        <nav className="navbar">
          <div className="logo">CNC Hub</div>
          <div className="nav-links">
            <NavLink to="/cad" className={({ isActive }) => isActive ? "active" : ""}>CAD Automation</NavLink>
            <NavLink to="/health" className={({ isActive }) => isActive ? "active" : ""}>Machine Health</NavLink>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={
              <div className="module-container" style={{textAlign: 'center', padding: '64px 32px'}}>
                <h2 style={{fontSize: '32px', marginBottom: '16px'}}>Welcome to CNC Hub</h2>
                <p style={{color: 'var(--text-muted)', fontSize: '18px'}}>
                  Intelligent predictive maintenance and automatic G-Code extraction.<br/> 
                  Select a module from the top navigation to begin.
                </p>
              </div>
            } />
            <Route path="/cad" element={<CadAutomation />} />
            <Route path="/health" element={<MachineHealth />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;