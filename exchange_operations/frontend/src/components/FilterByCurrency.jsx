import React from "react";
import PropTypes from "prop-types";


class FilterByCurrency extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        currencies: [],
        last: "",
        value: ""
    };
    this.handleCurrencyFilter = this.handleCurrencyFilter.bind(this);
    this.handleLastFilter = this.handleLastFilter.bind(this);

  }

  handleCurrencyFilter(event) {
    this.props.handleCurrencyFilter(event.target.value);
  }

  handleLastFilter(event) {
    this.props.handleLastFilter(event.target.value);
  }

  componentDidUpdate(prevProps, prevState) {
      if (this.props.operations !== prevProps.operations) {
        console.log('operaton');
        let currencies = this.props.operations.map((operation)=>{
            return operation.currency;
        });
        this.setState({currencies:currencies});
      }
      if (this.props.last !== prevProps.last || this.state.last === "") {
          this.setState({last:this.props.last});
      }
  }

  render() {
    return (
       <div>
      <form>
          <div className="field is-grouped">
                    <div className="field">
                        <div className="control is-expanded">
                            <div className="select is-primary">
                                <select onChange={this.handleCurrencyFilter}>
                                    <option value="">Filter by currency</option>
                                    {
                                       Array.from(new Set(this.state.currencies)).map(function(currency, index) {
                                         return (
                                            <option key={index} value={currency}>{currency}</option>

                                         )
                                       })
                                     }
                                </select>
                            </div>
                        </div>
                    </div>
                    <div className="field">
                        <div className="control">
                            {console.log(this.state)}
                            <input name="amount" className="input is-primary" type="text" value={this.state.last} onChange={this.handleLastFilter} />
                        </div>
                    </div>
          </div>
      </form>
    </div>
    );
  }
}

FilterByCurrency.propTypes = {
  handleCurrencyFilter: PropTypes.func.isRequired,
  handleLastFilter: PropTypes.func.isRequired,
  operations: PropTypes.array.isRequired,
};

export default FilterByCurrency;
