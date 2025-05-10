import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';
import { API_URL } from '../../constants';

function ItemsList({ currentListData, editCurrentList }) {
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(API_URL + "/list/suggest")
            .then(response => {
                editCurrentList(response.data)
            }).catch(err => {
                console.log(err)
                setError(err.message)
            })
    }, [])

    const handleDelete = (itemName) => {
        const updatedList = {...currentListData};
        delete updatedList[itemName];
        editCurrentList(updatedList);
    };

    if (error) return (<div>Error: {error}</div>);
    if (!currentListData) return <div>Loading...</div>;

    return (
        <div>
            <ul>
                {Object.keys(currentListData).length > 0 && Object.entries(currentListData).map(([item_name, amount], idx) => { 
                    return <li>{item_name} | {amount} <Button variant="danger" onClick={() => handleDelete(item_name)}>Delete</Button></li> })}
            </ul>
        </div>
    );

}


export default ItemsList;