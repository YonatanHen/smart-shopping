import Table from 'react-bootstrap/Table';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ItemsList({ listData, editList }) {
    const [error, setError] = useState(null);
    
    useEffect(() => {
        axios.get("http://localhost:5000/list/suggest")
            .then(response => {
                editList(response.data)
            }).catch(err => {
                console.log(err)
                setError(err.message)
            })
    }, [])

    if (error) return (<div>Error: {error}</div>);
    if (!listData) return <div>Loading...</div>;

    return (      
    );

}


export default ItemsList;