
class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { name: 'sausage', email: '' };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  handleSubmit = (event) => {
    fetch('http://localhost:5000/api/users/1', {
      method: 'POST',
      // We convert the React state to JSON and send it as the POST body
      body: JSON.stringify(this.state)
    }).then(function (response) {
      console.log(response)
      return response.json();
    });

    event.preventDefault();
  }

  fetchData() {
    fetch('http://localhost:5000/api/users/1')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      this.setState({
        name: 'asdasd',
        email: data.email
      });
      console.log(this.state);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  componentDidMount() {
    this.fetchData();
  }
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Name:
            <input type="text" value={this.state.name} name="name" onChange={this.handleChange} />
        </label>
        <label>
          Email:
            <input type="text" value={this.state.email} name="email" onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}


const domContainer = document.querySelector('#user_edit_form');
ReactDOM.render(React.createElement(NameForm), domContainer);