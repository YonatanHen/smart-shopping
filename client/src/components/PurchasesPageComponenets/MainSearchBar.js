import Form from 'react-bootstrap/Form';
import React from 'react';

function MainSearchBar({ input, setInput }) {

    const handleSearchInput = (event) => setInput(event.target.value);

    return (
        <Form>
            <Form.Group>
                <Form.Control type="text" placeholder="Search a product by name or list ID" value={input} onChange={handleSearchInput}/>
            </Form.Group>
        </Form>
    );
}

export default MainSearchBar;