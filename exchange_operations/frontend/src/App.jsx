import React, { Component } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";
import Modal from "react-modal";

import OperationsList from "./components/OperationsList";
import AddOperation from "./components/AddOperation";
import Message from "./components/Message";
import FilterByCurrency from "./components/FilterByCurrency";

const modalStyles = {
  content: {
    top: "0",
    left: "0",
    right: "0",
    bottom: "0",
    border: 0,
    background: "transparent"
  }
};

Modal.setAppElement(document.getElementById("root"));

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      operations:[],
      currencies: [],
      url: `${process.env.REACT_APP_EXCHANGE_OPERATIONS_SERVICE_URL}/exchange_operations/last/10`,
      last: 10,
      currency_code: "",
      title: "test",
      messageType: null,
      messageText: null,
      showModal: false
    };
  }

  componentDidMount = () => {
    this.getOperations();
  };

  getOperations() {
    axios.get(this.state.url)
   .then((res) => { this.setState({ operations: res.data });})
   .catch((err) => { console.log(err);});
  };

  addOperation = data => {
    axios
      .post(`${process.env.REACT_APP_EXCHANGE_OPERATIONS_SERVICE_URL}/exchange_operations/add`, data)
      .then(res => {
        this.setState(
          { currency_code: "", amount: "" },
          function () {
            this.updateUrl();
            this.getOperations();
            this.createMessage("success", "Operation added.");
          }
        );
        this.handleCloseModal();

      })
      .catch(err => {
        this.createMessage("success", err.response.data.message);
        console.log(err);
        this.handleCloseModal();
      });
  };

  createMessage = (type, text) => {
    this.setState({
      messageType: type,
      messageText: text
    });
    setTimeout(() => {
      this.removeMessage();
    }, 9000);
  };

  removeMessage = () => {
    this.setState({
      messageType: null,
      messageText: null
    });
  };

  handleOpenModal = () => {
    this.setState({ showModal: true });
  };

  handleCloseModal = () => {
    this.setState({ showModal: false });
  };

  updateUrl = () => {
    let url;
    if (this.state.currency_code !== "") {
      url = `${process.env.REACT_APP_EXCHANGE_OPERATIONS_SERVICE_URL}/exchange_operations/last/${this.state.currency_code}/${this.state.last}`
    } else {
      url = `${process.env.REACT_APP_EXCHANGE_OPERATIONS_SERVICE_URL}/exchange_operations/last/${this.state.last}`
    }
    this.setState(
      { url: url },
      function () {
        this.getOperations();
      }
    );
  }

  handleLastFilter = (lastOperations) => {
     this.setState(
    { last: lastOperations },
    function () {
      this.updateUrl()
    });

  }

  handleCurrencyFilter = (currency_code) => {
    this.setState(
    { currency_code: currency_code },
    function () {
      this.updateUrl()
    });
  };

  render() {
    return (
      <div>

        <section className="section">
          <div className="container">
            {this.state.messageType && this.state.messageText && (

              <Message
                messageType={this.state.messageType}
                messageText={this.state.messageText}
                removeMessage={this.removeMessage}
              />
            )}
            <div className="columns">
              <div className="column">
                <br />
                <Switch>
                  <Route
                    exact
                    path="/"
                    render={() => (
                      <div>
                        <h1 className="title is-1">Operations</h1>
                        <hr />
                        <br />
                          <div className="field is-grouped">
                            <button
                              onClick={this.handleOpenModal}
                              className="button is-primary"
                            >
                              Add Operation
                            </button>
                            <FilterByCurrency operations={this.state.operations} last={this.state.last}
                                              handleCurrencyFilter={this.handleCurrencyFilter}
                                              handleLastFilter={this.handleLastFilter}
                            />
                          </div>

                        <br />
                        <br />
                        <Modal
                          isOpen={this.state.showModal}
                          style={modalStyles}
                        >
                          <div className="modal is-active">
                            <div className="modal-background" />
                            <div className="modal-card">
                              <header className="modal-card-head">
                                <p className="modal-card-title">Add Operation</p>
                                <button
                                  className="delete"
                                  aria-label="close"
                                  onClick={this.handleCloseModal}
                                />
                              </header>
                              <section className="modal-card-body">
                                <AddOperation addOperation={this.addOperation} />
                              </section>
                            </div>
                          </div>
                        </Modal>
                        <OperationsList operations={this.state.operations}/>
                      </div>
                    )}
                  />

                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
