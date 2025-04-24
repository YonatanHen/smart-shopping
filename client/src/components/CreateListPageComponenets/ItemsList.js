import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ItemsList({ currentListData, editCurrentList }) {
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("http://localhost:5000/list/suggest")
            .then(response => {
                editCurrentList(response.data)
            }).catch(err => {
                console.log(err)
                setError(err.message)
            })
    }, [])

    if (error) return (<div>Error: {error}</div>);
    if (!currentListData) return <div>Loading...</div>;

    return (
        <div>
            <ul>
                {currentListData.length > 0 && currentListData.map((listItem, key) => { return <li>{listItem.item_name} | {listItem.amount}</li> })}
                <li>Creola Katherine Johnson: mathematician</li>
                <li>Mario José Molina-Pasquel Henríquez: chemist</li>
                <li>Mohammad Abdus Salam: physicist</li>
                <li>Percy Lavon Julian: chemist</li>
                <li>Subrahmanyan Chandrasekhar: astrophysicist</li>
            </ul>
        </div>
    );

}


export default ItemsList;