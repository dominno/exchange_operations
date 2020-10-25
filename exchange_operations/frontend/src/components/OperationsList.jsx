import React from 'react';
import PropTypes from "prop-types";

const OperationsList = (props) => {
  return (
    <div>
      <table className="table">
        <thead>
          <tr>
            <th>currency</th>
            <th>amount requested</th>
            <th>exchange price</th>
            <th>final amount</th>
            <th>date</th>
          </tr>
        </thead>
        <tbody>
           {
        props.operations.map(function(operation, index) {
          return (
            <tr
              key={index}
            >
              <td>{ operation.currency }</td>
              <td>{ operation.amount_requested }</td>
              <td>{ operation.exchange_price }</td>
              <td>{ operation.final_amount }</td>
              <td>{ operation.date }</td>
            </tr>
          )
        })
      }
        </tbody>
      </table>
    </div>
  )
};

OperationsList.propTypes = {
  operations: PropTypes.array.isRequired,
};


export default OperationsList;