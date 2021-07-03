var _jsxFileName = 'js-src/people.jsx';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Person = function (_React$Component) {
  _inherits(Person, _React$Component);

  function Person() {
    _classCallCheck(this, Person);

    return _possibleConstructorReturn(this, (Person.__proto__ || Object.getPrototypeOf(Person)).apply(this, arguments));
  }

  _createClass(Person, [{
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          },
          __self: this
        },
        this.props.name,
        ' (',
        this.props.email,
        ')'
      );
    }
  }]);

  return Person;
}(React.Component);

var People = function (_React$Component2) {
  _inherits(People, _React$Component2);

  function People() {
    _classCallCheck(this, People);

    return _possibleConstructorReturn(this, (People.__proto__ || Object.getPrototypeOf(People)).apply(this, arguments));
  }

  _createClass(People, [{
    key: 'render',
    value: function render() {
      var peopleNodes = this.props.data.map(function (person) {
        return React.createElement(Person, {
          key: person.email,
          name: person.name,
          email: person.email,
          __source: {
            fileName: _jsxFileName,
            lineNumber: 15
          },
          __self: this
        });
      });
      return React.createElement(
        'div',
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 23
          },
          __self: this
        },
        peopleNodes
      );
    }
  }]);

  return People;
}(React.Component);

var PeopleBox = function (_React$Component3) {
  _inherits(PeopleBox, _React$Component3);

  function PeopleBox(props) {
    _classCallCheck(this, PeopleBox);

    var _this3 = _possibleConstructorReturn(this, (PeopleBox.__proto__ || Object.getPrototypeOf(PeopleBox)).call(this, props));

    _this3.state = { data: [] };
    return _this3;
  }

  _createClass(PeopleBox, [{
    key: 'loadPeopleFromServer',
    value: function loadPeopleFromServer() {
      var _this4 = this;

      fetch('http://localhost:5000/api/users').then(function (response) {
        return response.json();
      }).then(function (data) {
        console.log(data);
        _this4.setState({
          data: data
        });
        console.log(_this4.state);
      }).catch(function (error) {
        console.log(error);
      });
    }
  }, {
    key: 'componentDidMount',
    value: function componentDidMount() {
      this.loadPeopleFromServer();
    }
  }, {
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 55
          },
          __self: this
        },
        React.createElement(
          'h2',
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 56
            },
            __self: this
          },
          'People'
        ),
        React.createElement(People, { data: this.state.data, __source: {
            fileName: _jsxFileName,
            lineNumber: 57
          },
          __self: this
        })
      );
    }
  }]);

  return PeopleBox;
}(React.Component);

var domContainer = document.querySelector('#people_list');
ReactDOM.render(React.createElement(PeopleBox), domContainer);