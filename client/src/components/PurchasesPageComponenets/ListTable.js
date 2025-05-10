import Table from 'react-bootstrap/Table';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_URL } from '../../constants';

function ListTable({ data, setData, searchBarInput }) {
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(API_URL + "/product")
            .then(response => {
                setData(response.data)
                console.log(response.data)
            }).catch(err => {
                console.log(err)
                setError(err.message)
            })
    }, [])

    if (error) return (<div>Error: {error}</div>);
    if (!data) return <div>Loading...</div>;

    return (
        <div className="list-table">
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>List ID</th>
                        <th>Item Name</th>
                        <th>Amount</th>
                        <th>Date Added</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((product, idx) => {
                        if (product.item_name.toLowerCase().includes(searchBarInput.toLowerCase()) 
                            ||product.list === searchBarInput)
                            return (
                                <tr>
                                    <td>{idx + 1}</td>
                                    <td>{product.list}</td>
                                    <td>{product.item_name}</td>
                                    <td>{product.amount}</td>
                                    <td>{product.date_added}</td>
                                </tr>
                            )
                        }
                    )}
                    <tr>
                    </tr>
                </tbody>
            </Table>
        </div>
    );
}

export default ListTable;
