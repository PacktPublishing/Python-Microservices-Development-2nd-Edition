class Person extends React.Component {
  render() {
    return /*#__PURE__*/React.createElement("div", null, this.props.name, " (", this.props.email, ")");
  }

}

class People extends React.Component {
  render() {
    var peopleNodes = this.props.data.map(function (person) {
      return /*#__PURE__*/React.createElement(Person, {
        key: person.email,
        name: person.name,
        email: person.email
      });
    });
    return /*#__PURE__*/React.createElement("div", null, peopleNodes);
  }

}

class PeopleBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  loadPeopleFromServer() {
    fetch('http://localhost:5000/api/users').then(response => response.json()).then(data => {
      console.log(data);
      this.setState({
        data: data
      });
      console.log(this.state);
    }).catch(function (error) {
      console.log(error);
    });
  }

  componentDidMount() {
    this.loadPeopleFromServer();
  }

  render() {
    return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", null, "People"), /*#__PURE__*/React.createElement(People, {
      data: this.state.data
    }));
  }

}

const domContainer = document.querySelector('#people_list');
ReactDOM.render(React.createElement(PeopleBox), domContainer);