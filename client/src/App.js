import './App.css';
import ListTable from './components/ListTable';
import MainSearchBar from './components/mainSearchBar';
import React, { useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  return (
    <div className="App">
      <h1>Smart Shopping App</h1>
      <MainSearchBar/>
      <ListTable data={data} setData={setData}/>
    </div>
  );
}

export default App;
