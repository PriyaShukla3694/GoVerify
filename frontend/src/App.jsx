import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Upload from './pages/Upload';
import OfficerDashboard from './pages/OfficerDashboard';
import Status from './pages/Status';
import Payment from './pages/Payment';
import Verification from './pages/Verification';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
        <nav className="bg-white shadow-sm border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xl leading-none">V</div>
                <Link to="/" className="font-bold text-xl tracking-tight text-gray-800 hover:text-blue-600 transition">GovVerify</Link>
            </div>
            <div className="flex space-x-6 text-sm font-medium">
              <Link to="/" className="text-gray-600 hover:text-blue-600 transition">📝 Submit Application</Link>
              <Link to="/officer" className="text-gray-600 hover:text-indigo-600 transition mt-0">🛡️ Officer Dashboard</Link>
            </div>
          </div>
        </nav>

        <main className="pb-12">
            <Routes>
                <Route path="/" element={<Upload />} />
                <Route path="/payment/:id" element={<Payment />} />
                <Route path="/verification/:id" element={<Verification />} />
                <Route path="/status/:id" element={<Status />} />
                <Route path="/officer" element={<OfficerDashboard />} />
            </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
