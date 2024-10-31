import Form from 'react-bootstrap/Form';
import React, { useEffect, useState } from 'react';

function MainSearchBar({ input, setInput }) {

    const handleSearchInput = (event) => {
        setInput(event.target.value)
    }

    return (
        <Form>
            <Form.Group>
                <Form.Label>Serach</Form.Label>
                <Form.Control type="text" placeholder="Enter item name or List ID" value={input} onChange={handleSearchInput}/>
            </Form.Group>
        </Form>
    )
}

export default MainSearchBar