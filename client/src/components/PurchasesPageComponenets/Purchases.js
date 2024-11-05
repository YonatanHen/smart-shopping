import ListTable from './ListTable';
import MainSearchBar from './MainSearchBar';
import React, { useState } from 'react';

function PurchasesPage() {
  const [data, setData] = useState(null);
  const [input, setInput] = useState("")

  return (
    <div>
      <MainSearchBar input={input} setInput={setInput}/>
      <ListTable data={data} setData={setData} searchBarInput={input} />
    </div>
  );
}

export default PurchasesPage;