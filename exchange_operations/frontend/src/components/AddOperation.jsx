import React from "react";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

import "./form.css";

const AddOperation = props => (
  <Formik
    initialValues={{
      currency_code: "",
      amount: "",
    }}
    onSubmit={(values, { setSubmitting, resetForm }) => {
      props.addOperation(values);
      resetForm();
      setSubmitting(false);
    }}
    validationSchema={Yup.object().shape({
      currency_code: Yup.string()
        .required("Currency is required."),
      amount: Yup.string()
        .required("Amount is required."),
    })}
  >
    {props => {
      const {
        values,
        touched,
        errors,
        isSubmitting,
        handleChange,
        handleBlur,
        handleSubmit
      } = props;
      return (
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label className="label" htmlFor="input-currency_code">
              Currency
            </label>
            <input
              name="currency_code"
              id="input-currency_code"
              className={
                errors.currency_code && touched.currency_code ? "input error" : "input"
              }
              type="text"
              placeholder="Choose currency"
              value={values.currency_code}
              onChange={handleChange}
              onBlur={handleBlur}
            />
            {errors.currency_code && touched.currency_code && (
              <div className="input-feedback">{errors.currency_code}</div>
            )}
          </div>
          <div className="field">
            <label className="label" htmlFor="input-amount">
              Amount
            </label>
            <input
              name="amount"
              id="input-amount"
              className={
                errors.amount && touched.amount ? "input error" : "input"
              }
              type="text"
              placeholder="Enter value to multiply"
              value={values.amount}
              onChange={handleChange}
              onBlur={handleBlur}
            />
            {errors.amount && touched.amount && (
              <div className="input-feedback">{errors.amount}</div>
            )}
          </div>
          <input
            type="submit"
            className="button is-primary"
            value="Submit"
            disabled={isSubmitting}
          />
        </form>
      );
    }}
  </Formik>
);

AddOperation.propTypes = {
  addOperation: PropTypes.func.isRequired
};

export default AddOperation;
