import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ItemsList from './ItemsList';

function CreateList() {
  const [productInput, setProductInput] = useState("");
  const [amountInput, setAmountInput] = useState("");
  const [currentList, editCurrentList] = useState([])

  const handleProductInput = (event) => setProductInput(event.target.value);
  const handleAmountInput = (event) => setAmountInput(event.target.value);

  return (
    <div>
      <h1>Create List</h1>
      <Form>
        <Form.Group as={Row} className="align-items-center create-list-form">
          <Col xs="auto" className='create-list-label'>Add New Product:</Col>
          <Col xs={4}>
            <Form.Control
              type="text"
              placeholder="Product name"
              value={productInput}
              onChange={handleProductInput}
            />
          </Col>
          <Col xs={3}>
            <Form.Control
              type="text"
              placeholder="Amount"
              value={amountInput}
              onChange={handleAmountInput}
            />
          </Col>
        </Form.Group>
      </Form>
      <ItemsList currentListData={currentList} editCurrentList={editCurrentList}/>
    </div>
  );
}

export default CreateList;
