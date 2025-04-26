import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ItemsList from './ItemsList';

function CreateList() {
  const [productInput, setProductInput] = useState("");
  const [amountInput, setAmountInput] = useState(0);
  const [currentList, editCurrentList] = useState([])

  const handleProductInput = (event) => setProductInput(event.target.value);
  const handleAmountInput = (event) => setAmountInput(event.target.value);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (productInput.trim() !== "" && amountInput.trim() !== "") {
      editCurrentList(prevList => [
        ...prevList,
        { item_name: productInput.trim(), amount: amountInput.trim() }
      ]);

      setProductInput("");
      setAmountInput("");
    }
  }

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
            <Form.Select
              value={amountInput}
              onChange={handleAmountInput}
            >
              <option value={amountInput}>Amount</option>
              {Array.from({ length: 20 }, (_, i) => i + 1).map(number => (
                <option key={number} value={number}>
                  {number}
                </option>
              ))}
            </Form.Select>
          </Col>
          <Col xs={1}><Button onClick={(event) => handleSubmit(event)} variant="secondary" size='lg' disabled={productInput.trim() === "" || amountInput === 0}>+</Button></Col>
        </Form.Group>
      </Form>
      <ItemsList currentListData={currentList} editCurrentList={editCurrentList} />
    </div>
  );
}

export default CreateList;
