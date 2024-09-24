import '../App.css';
import Table from 'react-bootstrap/Table';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ListTable() {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("http://localhost:5000/products")
            .then(response => {
                setData(response.data)
                console.log(response.data)
            }).catch(err => {
                console.log(err)
                setError(err.message)
            })
    }, [])

    if (error) return (<div>Error: {error}</div> );
    if (!data) return <div>Loading...</div>;

    return (
        <div className="list-table">
            {/* <pre>{JSON.stringify(data, null, 2)}</pre> */}
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>List #</th>
                        <th>#</th>
                        <th>Item Name</th>
                        <th>Amount</th>
                        <th>Date Added</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    </tr>
                </tbody>
            </Table>
        </div>
    );
}

export default ListTable;
