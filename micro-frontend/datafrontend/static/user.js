var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var NameForm = function (_React$Component) {
  _inherits(NameForm, _React$Component);

  function NameForm(props) {
    _classCallCheck(this, NameForm);

    var _this = _possibleConstructorReturn(this, (NameForm.__proto__ || Object.getPrototypeOf(NameForm)).call(this, props));

    _this.handleChange = function (event) {
      _this.setState(_defineProperty({}, event.target.name, event.target.value));
    };

    _this.handleSubmit = function (event) {
      fetch('http://localhost:5000/api/users/1', {
        method: 'POST',
        // We convert the React state to JSON and send it as the POST body
        body: JSON.stringify(_this.state)
      }).then(function (response) {
        console.log(response);
        return response.json();
      });

      event.preventDefault();
    };

    _this.state = { name: 'sausage', email: '' };
    return _this;
  }

  _createClass(NameForm, [{
    key: 'fetchData',
    value: function fetchData() {
      var _this2 = this;

      fetch('http://localhost:5000/api/users/1').then(function (response) {
        return response.json();
      }).then(function (data) {
        console.log(data);
        _this2.setState({
          name: 'asdasd',
          email: data.email
        });
        console.log(_this2.state);
      }).catch(function (error) {
        console.log(error);
      });
    }
  }, {
    key: 'componentDidMount',
    value: function componentDidMount() {
      this.fetchData();
    }
  }, {
    key: 'render',
    value: function render() {
      return React.createElement(
        'form',
        { onSubmit: this.handleSubmit },
        React.createElement(
          'label',
          null,
          'Name:',
          React.createElement('input', { type: 'text', value: this.state.name, name: 'name', onChange: this.handleChange })
        ),
        React.createElement(
          'label',
          null,
          'Email:',
          React.createElement('input', { type: 'text', value: this.state.email, name: 'email', onChange: this.handleChange })
        ),
        React.createElement('input', { type: 'submit', value: 'Submit' })
      );
    }
  }]);

  return NameForm;
}(React.Component);

var domContainer = document.querySelector('#user_edit_form');
ReactDOM.render(React.createElement(NameForm), domContainer);