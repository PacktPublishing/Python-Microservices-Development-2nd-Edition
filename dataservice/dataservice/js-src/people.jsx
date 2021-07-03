

class Person extends React.Component {
  render() {
    return (
      <div>{this.props.name} ({this.props.email})</div>
    );
  }
}

class People extends React.Component {
  render() {
    var peopleNodes = this.props.data.map(function (person) {
      return (
        <Person
          key={person.email}
          name={person.name}
          email={person.email}
        />
      );
    });
    return (
      <div>
        {peopleNodes}
      </div>
    );
  }
}

class PeopleBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  loadPeopleFromServer() {
    fetch('http://localhost:5000/api/users')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      this.setState({
        data: data,
      });
      console.log(this.state);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  componentDidMount() {
    this.loadPeopleFromServer();
  }
  render() { 
    return ( 
      <div> 
        <h2>People</h2> 
        <People data= {this.state.data}  /> 
      </div> 
    ); 
  } 
}

const domContainer = document.querySelector('#people_list');
ReactDOM.render(React.createElement(PeopleBox), domContainer);