import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function CreateList() {
  const [productInput, setProductInput] = useState("");
  const [amountInput, setAmountInput] = useState("");

  const handleProductInput = (e) => setProductInput(e.target.value);
  const handleAmountInput = (e) => setAmountInput(e.target.value);

  return (
    <div>
      <h1>Create List</h1>
      <Form>
        <Form.Group as={Row} className="align-items-center">
          <Col>
            <Form.Control
              type="text"
              placeholder="Enter product name"
              value={productInput}
              onChange={handleProductInput}
            />
          </Col>
          <Col>
            <Form.Control
              type="text"
              placeholder="Enter amount"
              value={amountInput}
              onChange={handleAmountInput}
            />
          </Col>
        </Form.Group>
      </Form>
    </div>
  );
}

export default CreateList;
