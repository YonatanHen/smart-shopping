import './App.css';
import ListTable from './components/ListTable';
import MainSearchBar from './components/mainSearchBar';
import React, { useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [input, setInput] = useState("")

  return (
    <div className="App">
      <h1>Smart Shopping App</h1>
      <MainSearchBar input={input} setInput={setInput}/>
      <ListTable data={data} setData={setData} searchBarInput={input} />
    </div>
  );
}

export default App;
