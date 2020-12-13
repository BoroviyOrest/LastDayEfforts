import React, {Component} from 'react';
import {Login} from '../../components/Login';


export class LoginContainer extends Component {
    onSubmit = (values) => {
        console.log(values);
    };

    render() {
        return (
            <Login onSubmit={this.onSubmit}/>
        )
    }
}
