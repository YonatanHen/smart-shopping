import './App.css';
import Navbar from './components/navbar';
import React, { useState } from 'react';
import { Outlet } from "react-router-dom";


function App() {
  const [data, setData] = useState(null);
  const [input, setInput] = useState("")

  return (
    <div className="App">
      <Navbar />
      {/* <h1>Smart Shopping App</h1> */}
      <Outlet />
    </div>
  );
}

export default App;
