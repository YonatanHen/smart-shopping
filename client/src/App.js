import './App.css';
import ListTable from './components/PurchasesPage/ListTable';
import Navbar from './components/navbar';
import MainSearchBar from './components/PurchasesPage/mainSearchBar';
import React, { useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [input, setInput] = useState("")

  return (
    <div className="App">
      <Navbar />
      <h1>Smart Shopping App</h1>
      <MainSearchBar input={input} setInput={setInput}/>
      <ListTable data={data} setData={setData} searchBarInput={input} />
    </div>
  );
}

export default App;
