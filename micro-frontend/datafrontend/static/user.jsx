class NameForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = { name: '' };
    }
  
    handleChange = (event) => {
      this.setState({[event.target.name]: event.target.value});
    }
  
    handleSubmit = (event) => {
      alert('A form was submitted: ' + this.state);
  
      fetch('http://localhost:5000/api/users/1', {
          method: 'POST',
          // We convert the React state to JSON and send it as the POST body
          body: JSON.stringify(this.state)
        }).then(function(response) {
          console.log(response)
          return response.json();
        });
  
      event.preventDefault();
  }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Name:
            <input type="text" value={this.state.value} name="name" onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
      );
    }
  }


const domContainer = document.querySelector('#user_edit_form');
ReactDOM.render(React.createElement(NameForm), domContainer);